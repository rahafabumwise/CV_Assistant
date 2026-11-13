"""Run the three models on the 30 test questions and score them.

Three steps, so two people can grade independently:

  1) python score.py generate
       - asks base, cpt and sft the 30 questions through ONE function
         (src.modeling.generate_answer) with the same greedy settings
       - measures held-out perplexity of each model on the CPT held-out document
       - writes results/answers_<model>.csv and blank grading sheets
         results/grading/<model>_grader1.csv and _grader2.csv

  2) Each grader fills the `score` column of THEIR sheet (1 / 0.5 / 0) without
     looking at the other sheet. Then:
     python score.py agree
       - reports how often the two graders agreed at first
       - writes results/grading/<model>_final.csv with agreed scores filled in and
         disagreements left blank to settle together (+ error_category for the SFT model)

  3) Fill the blanks in the *_final.csv files, then:
     python score.py summarize --show 6,16,28
       - writes results/results_<model>.csv (question, expected, answer, score, note)
       - writes results/summary.json and results/scoreboard_rows.md
       - prints the SFT error-analysis counts and 3 questions side by side

For the demo video:
     python score.py ask "Should I list my newest or oldest job first?"
       - prints the answer of all three models to one question (same function, same settings)

Options: --models base,cpt  (subset)   --force  (overwrite filled grading sheets)
Every step also copies results/ to <paths.output_dir>/results on Google Drive.
"""
from __future__ import annotations

import csv
import gc
import json
from collections import Counter
from pathlib import Path

import torch

from src.chat_template import ChatTemplate
from src.config import base_arg_parser, load_config, project_path, resolve_model, results_dirs
from src.data import load_cpt_split, load_test_questions, normalize, read_documents
from src.modeling import generate_answer, get_device, heldout_perplexity, load_model, set_seed

MODEL_KEYS = ["base", "cpt", "sft"]
VALID_SCORES = {"0", "0.5", "1"}
ERROR_CATEGORIES = ["format_failure", "hallucination", "knowledge_missing", "refusal_error", "test_case_problem"]
GRADE_FIELDS = ["id", "question", "expected_answer", "should_refuse", "model_answer", "score", "note"]


def read_csv(path: Path) -> list[dict]:
    # utf-8-sig also accepts files saved by Excel / Google Sheets
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig so Excel shows quotes and accents correctly
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def has_scores(path: Path) -> bool:
    return path.exists() and any(r.get("score", "").strip() for r in read_csv(path))


def mirror_results(cfg) -> None:
    """Copy results/ to the backup folder on Drive (skipped if it is the same folder)."""
    import shutil
    src, backup = results_dirs(cfg)
    try:
        if backup.resolve() != src.resolve():
            shutil.copytree(src, backup, dirs_exist_ok=True)
    except OSError as e:
        print(f"(Could not copy results to {backup}: {e})")


# ------------------------------------------------------------------ generate
def cmd_generate(cfg, keys, force):
    set_seed(cfg["seed"])
    device = get_device()
    template = ChatTemplate(cfg)
    tests = load_test_questions(cfg)
    heldout = read_documents(load_cpt_split(cfg)["validation"])
    exact_ids = {str(i) for i in cfg.get("scoring", {}).get("exact_match_ids", [])}
    results = project_path(cfg["paths"]["results_dir"])
    ppl_path = results / "perplexity.json"
    ppl_all = json.loads(ppl_path.read_text()) if ppl_path.exists() else {}

    for key in keys:
        name = resolve_model(cfg, key)
        print(f"\n=== {key}: {name}")
        model, tokenizer = load_model(name, device)
        ppl = heldout_perplexity(model, tokenizer, heldout, cfg["cpt"]["eval_context"], cfg["cpt"]["eval_stride"])
        ppl_all[key] = {"model": name, **ppl}
        print(f"held-out perplexity {ppl['perplexity']:.2f}")

        rows = []
        for t in tests:
            answer, raw, secs = generate_answer(model, tokenizer, template, t["question"], cfg["generation"])
            em = normalize(answer) == normalize(t["expected_answer"])
            rows.append({
                "id": t["id"], "question": t["question"], "expected_answer": t["expected_answer"],
                "should_refuse": int(t["should_refuse"]), "model_answer": answer, "raw_generation": raw,
                "latency_s": f"{secs:.3f}", "exact_match": int(em),
                # Short exact answers (listed in config scoring.exact_match_ids) are scored automatically.
                "score": (("1" if em else "0") if t["id"] in exact_ids else ""), "note": "",
            })
            print(f"  [{t['id']:>2}] {secs:5.2f}s  {answer[:90]!r}")
        write_csv(results / f"answers_{key}.csv", rows,
                  ["id", "question", "expected_answer", "should_refuse", "model_answer",
                   "raw_generation", "latency_s", "exact_match"])
        for g in ("grader1", "grader2"):
            sheet = results / "grading" / f"{key}_{g}.csv"
            if has_scores(sheet) and not force:
                print(f"  kept {sheet.name} (already has scores; use --force to overwrite)")
            else:
                write_csv(sheet, rows, GRADE_FIELDS)

        del model, tokenizer
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    ppl_path.write_text(json.dumps(ppl_all, indent=2))
    meta = {"generation": cfg["generation"], "chat_template": cfg["chat_template"],
            "models": {k: ppl_all[k]["model"] for k in keys}, "device": device, "seed": cfg["seed"]}
    (results / "score_settings.json").write_text(json.dumps(meta, indent=2))
    mirror_results(cfg)
    print("\nNext: two graders fill results/grading/<model>_grader1.csv / _grader2.csv, then run: python score.py agree")


# ------------------------------------------------------------------ agree
def cmd_agree(cfg, keys, force):
    results = project_path(cfg["paths"]["results_dir"])
    report = {}
    for key in keys:
        g1 = read_csv(results / "grading" / f"{key}_grader1.csv")
        g2 = {r["id"]: r for r in read_csv(results / "grading" / f"{key}_grader2.csv")}
        rows, agree, disagreements = [], 0, []
        for r in g1:
            s1, s2 = r["score"].strip(), g2[r["id"]]["score"].strip()
            for s, who in ((s1, "grader1"), (s2, "grader2")):
                if s not in VALID_SCORES:
                    raise ValueError(f"{key} id {r['id']}: {who} score '{s}' must be 0, 0.5 or 1")
            same = float(s1) == float(s2)
            agree += same
            if not same:
                disagreements.append(r["id"])
            notes = " | ".join(n for n in (r["note"], g2[r["id"]]["note"]) if n.strip())
            rows.append({**r, "grader1": s1, "grader2": s2, "final_score": s1 if same else "",
                         "error_category": "", "note": notes})
        final = results / "grading" / f"{key}_final.csv"
        if final.exists() and not force:
            print(f"{final.name} already exists; not overwritten (use --force to rebuild it)")
        else:
            write_csv(final, rows, ["id", "question", "expected_answer", "should_refuse", "model_answer",
                                    "grader1", "grader2", "final_score", "error_category", "note"])
        report[key] = {"initial_agreement": agree / len(g1), "agreed": agree, "total": len(g1),
                       "disagreements": disagreements}
        print(f"{key}: graders agreed on {agree}/{len(g1)} ({agree / len(g1):.0%}); settle ids {disagreements}")
    (results / "grader_agreement.json").write_text(json.dumps(report, indent=2))
    mirror_results(cfg)
    print("\nFill the blank final_score cells together. For the SFT model also set error_category "
          f"for every answer scored below 1: {', '.join(ERROR_CATEGORIES)}")


# ------------------------------------------------------------------ summarize
def cmd_summarize(cfg, keys, show):
    results = project_path(cfg["paths"]["results_dir"])
    ppl = json.loads((results / "perplexity.json").read_text())
    agreement = json.loads((results / "grader_agreement.json").read_text()) \
        if (results / "grader_agreement.json").exists() else {}
    summary, answers_by_key = {}, {}
    for key in keys:
        final = read_csv(results / "grading" / f"{key}_final.csv")
        answers = {r["id"]: r for r in read_csv(results / f"answers_{key}.csv")}
        answers_by_key[key] = answers
        missing = [r["id"] for r in final if r["final_score"].strip() not in VALID_SCORES]
        if missing:
            raise ValueError(f"{key}: final_score missing/invalid for ids {missing}")
        scores = [float(r["final_score"]) for r in final]
        refuse = [r for r in final if r["should_refuse"] in ("1", "True", "true")]
        refusal_ok = sum(float(r["final_score"]) == 1 for r in refuse)
        latency = sum(float(a["latency_s"]) for a in answers.values()) / len(answers)

        errors = Counter()
        if key == "sft":
            for r in final:
                if float(r["final_score"]) < 1:
                    cat = r["error_category"].strip()
                    if cat not in ERROR_CATEGORIES:
                        raise ValueError(f"sft id {r['id']}: error_category '{cat}' must be one of {ERROR_CATEGORIES}")
                    errors[cat] += 1

        write_csv(results / f"results_{key}.csv",
                  [{"id": r["id"], "question": r["question"], "expected_answer": r["expected_answer"],
                    "model_answer": r["model_answer"], "score": r["final_score"],
                    "error_category": r.get("error_category", ""), "note": r["note"]} for r in final],
                  ["id", "question", "expected_answer", "model_answer", "score", "error_category", "note"])
        summary[key] = {
            "model": ppl.get(key, {}).get("model", cfg["models"][key]),
            "heldout_perplexity": ppl.get(key, {}).get("perplexity"),
            "accuracy_pct": 100 * sum(scores) / len(scores),
            "refusal_accuracy_pct": 100 * refusal_ok / len(refuse) if refuse else None,
            "refusals_correct": f"{refusal_ok}/{len(refuse)}",
            "avg_latency_s": latency,
            "initial_grader_agreement": agreement.get(key, {}).get("initial_agreement"),
            "error_counts": dict(errors) if key == "sft" else None,
        }

    (results / "summary.json").write_text(json.dumps(summary, indent=2))
    labels = {"base": "Small model, base", "cpt": "+ continued pretraining", "sft": "+ SFT"}
    lines = ["| Version | Held-out perplexity | Accuracy | Refusal accuracy | Avg. latency (s) | Notes |",
             "|---|---|---|---|---|---|"]
    for key, s in summary.items():
        p = f"{s['heldout_perplexity']:.2f}" if s["heldout_perplexity"] else "—"
        r = f"{s['refusal_accuracy_pct']:.0f}% ({s['refusals_correct']})" if s["refusal_accuracy_pct"] is not None else "—"
        lines.append(f"| {labels[key]} | {p} | {s['accuracy_pct']:.1f}% | {r} | {s['avg_latency_s']:.2f} | |")
    table = "\n".join(lines)
    (results / "scoreboard_rows.md").write_text(table + "\n")
    mirror_results(cfg)
    print(table)
    if "sft" in summary:
        print("\nSFT error analysis:", summary["sft"]["error_counts"])

    for qid in show:
        print(f"\n--- Test {qid}: {answers_by_key[keys[0]][qid]['question']}")
        print(f"Expected: {answers_by_key[keys[0]][qid]['expected_answer']}")
        for key in keys:
            print(f"[{key}] {answers_by_key[key][qid]['model_answer'][:400]}")


# ------------------------------------------------------------------ ask (demo)
def cmd_ask(cfg, keys, question):
    set_seed(cfg["seed"])
    device = get_device()
    template = ChatTemplate(cfg)
    print(f"Question: {question}")
    for key in keys:
        model, tokenizer = load_model(resolve_model(cfg, key), device)
        answer, _, secs = generate_answer(model, tokenizer, template, question, cfg["generation"])
        print(f"\n[{key}] ({secs:.2f}s)\n{answer}")
        del model, tokenizer
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def main():
    parser = base_arg_parser(__doc__)
    parser.add_argument("step", choices=["generate", "agree", "summarize", "ask"])
    parser.add_argument("question", nargs="?", default=None, help="Only for 'ask': the question to send")
    parser.add_argument("--models", default=",".join(MODEL_KEYS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--show", default="", help="Comma-separated test ids to print side by side")
    args = parser.parse_args()
    cfg = load_config(args.config, args.overrides)
    keys = [k.strip() for k in args.models.split(",") if k.strip()]
    if args.step == "generate":
        cmd_generate(cfg, keys, args.force)
    elif args.step == "ask":
        if not args.question:
            parser.error('ask needs a question, e.g. python score.py ask "Do I need a hobbies section?"')
        cmd_ask(cfg, keys, args.question)
    elif args.step == "agree":
        cmd_agree(cfg, keys, args.force)
    else:
        cmd_summarize(cfg, keys, [s.strip() for s in args.show.split(",") if s.strip()])


if __name__ == "__main__":
    main()
