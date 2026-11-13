"""Step 2 — supervised fine-tuning (SFT) of the continued-pretrained model.

    python train_sft.py                         # starts from models.cpt in config.yaml
    python train_sft.py --set sft.epochs=2      # override a setting for one run

What it does
  * starts from the CPT checkpoint (models.cpt; "auto" = the one train_cpt.py selected)
  * adds <|user|>, <|assistant|>, <|end|> as special tokens (src/chat_template.py)
  * trains on data/sft/train.jsonl (301 pairs); validates on data/sft/validation.jsonl (34)
  * loss on the answer tokens and <|end|> only — question and padding are masked with -100
  * refuses to run if an SFT question is identical to a test question
  * saves a checkpoint per epoch and keeps the one with the lowest validation loss

Checkpoints: <paths.output_dir>/sft_<timestamp>/epoch_N and .../best   (Google Drive, NOT Git)
Results (results/ and a copy in <paths.output_dir>/results/):
    sft_metrics.json, sft_step_losses.json, sft_loss_curve.png,
    sft_format_check.json (does the model answer in the format and stop with <|end|>
    on the 34 held-out SFT questions? — these are NOT test questions)
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from transformers import get_linear_schedule_with_warmup

from src.chat_template import ChatTemplate, add_chat_tokens
from src.config import base_arg_parser, load_config, project_path, resolve_model, save_result
from src.data import (SFTDataset, check_no_test_overlap, load_jsonl, load_test_questions,
                      sft_collate)
from src.modeling import generate_answer, get_device, load_model, set_seed
from src.plotting import plot_losses


@torch.no_grad()
def answer_only_loss(model, loader, device) -> float:
    model.eval()
    tot, n = 0.0, 0
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        loss = model(**batch, use_cache=False).loss
        scored = (batch["labels"][:, 1:] != -100).sum().item()
        tot += loss.item() * scored
        n += scored
    return tot / n


def main():
    parser = base_arg_parser(__doc__)
    parser.add_argument("--push_to_hub", default=None,
                        help="Optional Hugging Face repo id to upload the best SFT checkpoint. Needs HF_TOKEN.")
    args = parser.parse_args()
    cfg = load_config(args.config, args.overrides)
    s = cfg["sft"]
    set_seed(cfg["seed"])
    device = get_device()
    template = ChatTemplate(cfg)
    print(f"Device: {device}")

    run_dir = Path(cfg["paths"]["output_dir"]) / datetime.now(timezone.utc).strftime("sft_%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "config_used.json").write_text(json.dumps(cfg, indent=2))
    print(f"Run folder: {run_dir}")

    # ---- data + safety checks ----
    train_rows = load_jsonl(cfg["paths"]["sft_train"])
    val_rows = load_jsonl(cfg["paths"]["sft_validation"])
    shared = {r["id"] for r in train_rows} & {r["id"] for r in val_rows}
    assert not shared, f"Pairs in both SFT train and validation: {shared}"
    tests = load_test_questions(cfg)
    warnings = check_no_test_overlap(train_rows + val_rows, tests)   # raises on exact matches
    print(f"Test-overlap check: no exact matches; {len(warnings)} shared 8-word sequences")
    for w in warnings:
        print("  CHECK BY HAND:", w)

    # ---- model: start from the continued-pretrained checkpoint ----
    start_from = resolve_model(cfg, "cpt")
    print(f"Starting from CPT checkpoint: {start_from}")
    model, tokenizer = load_model(start_from, device)
    added = add_chat_tokens(tokenizer, model, template)
    print(f"Added {added} special tokens: {template.special_tokens} (vocabulary now {len(tokenizer)})")

    train_ds = SFTDataset(train_rows, tokenizer, template, int(s["max_length"]))
    val_ds = SFTDataset(val_rows, tokenizer, template, int(s["max_length"]))
    if train_ds.truncated or val_ds.truncated:
        print(f"WARNING: {train_ds.truncated + val_ds.truncated} pairs were truncated; raise sft.max_length")
    collate = sft_collate(tokenizer.pad_token_id)
    train_loader = DataLoader(train_ds, batch_size=int(s["batch_size"]), shuffle=True,
                              collate_fn=collate, generator=torch.Generator().manual_seed(cfg["seed"]))
    val_loader = DataLoader(val_ds, batch_size=int(s["batch_size"]), collate_fn=collate)
    print(f"SFT pairs: {len(train_ds)} train, {len(val_ds)} validation; {len(train_loader)} steps per epoch")

    # Show one example so everyone can see that the loss is on the answer only.
    ex = train_ds[0]
    trained = [t for t, l in zip(ex["input_ids"], ex["labels"]) if l != -100]
    print("\nExample — what the model reads:  ", repr(tokenizer.decode(ex["input_ids"])))
    print("Example — tokens that get a loss:", repr(tokenizer.decode(trained)), "\n")

    optimizer = torch.optim.AdamW(model.parameters(), lr=float(s["learning_rate"]),
                                  weight_decay=float(s["weight_decay"]))
    total_steps = len(train_loader) * int(s["epochs"])
    scheduler = get_linear_schedule_with_warmup(
        optimizer, math.ceil(total_steps * float(s["warmup_ratio"])), total_steps)

    val_before = answer_only_loss(model, val_loader, device)
    print(f"Validation loss (answers only) before SFT: {val_before:.4f}")

    epochs, step_losses = [], []
    best = {"epoch": None, "val_loss": float("inf")}
    for epoch in range(1, int(s["epochs"]) + 1):
        model.train()
        tot, n = 0.0, 0
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad(set_to_none=True)
            loss = model(**batch, use_cache=False).loss
            if not torch.isfinite(loss):
                raise RuntimeError("Loss became NaN/inf — stop and inspect.")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), float(s["max_grad_norm"]))
            optimizer.step()
            scheduler.step()
            scored = (batch["labels"][:, 1:] != -100).sum().item()
            tot += loss.item() * scored
            n += scored
            step_losses.append(loss.item())
        val = answer_only_loss(model, val_loader, device)
        ckpt = run_dir / f"epoch_{epoch}"
        model.save_pretrained(ckpt, safe_serialization=True)
        tokenizer.save_pretrained(ckpt)
        row = {"epoch": epoch, "train_loss": tot / n, "val_loss": val, "checkpoint": str(ckpt)}
        epochs.append(row)
        print(f"Epoch {epoch}: train loss {row['train_loss']:.4f} | validation loss {val:.4f}")
        if val < best["val_loss"]:
            best = {"epoch": epoch, "val_loss": val}
            model.save_pretrained(run_dir / "best", safe_serialization=True)
            tokenizer.save_pretrained(run_dir / "best")

    # ---- format check on the 34 held-out SFT questions (NOT the test set) ----
    del model, optimizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer = load_model(str(run_dir / "best"), device)
    checks = []
    for r in val_rows:
        answer, raw, _ = generate_answer(model, tokenizer, template, r["question"], cfg["generation"])
        checks.append({"id": r["id"], "question": r["question"], "reference": r["answer"],
                       "model_answer": answer, "stopped_with_end_token": template.end in raw})
    stop_rate = sum(c["stopped_with_end_token"] for c in checks) / len(checks)

    metrics = {
        "run": run_dir.name,
        "start_checkpoint": start_from,
        "device": device,
        "seed": cfg["seed"],
        "settings": s,
        "chat_template": {"prompt": template.prompt("{question}"), "completion": template.completion("{answer}"),
                          "special_tokens_added": added},
        "n_train_pairs": len(train_rows), "n_validation_pairs": len(val_rows),
        "steps_per_epoch": len(train_loader),
        "test_overlap_warnings": warnings,
        "val_loss_before": val_before,
        "epochs": epochs,
        "selected_epoch": best["epoch"],
        "selected_checkpoint": str(run_dir / "best"),
        "format_stop_rate_on_sft_validation": stop_rate,
    }
    save_result(cfg, "sft_metrics.json", metrics)
    save_result(cfg, "sft_step_losses.json", step_losses)
    save_result(cfg, "sft_format_check.json", {"stopped_with_end_token_rate": stop_rate, "examples": checks})
    curve = project_path(cfg["paths"]["results_dir"]) / "sft_loss_curve.png"
    plot_losses(step_losses, epochs, val_before, "Supervised fine-tuning (loss on answers only)",
                curve, len(train_loader), best["epoch"])
    save_result(cfg, "sft_loss_curve.png", curve.read_bytes())
    (run_dir / "sft_metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"\nSelected epoch {best['epoch']} (validation loss {best['val_loss']:.4f})")
    print(f"Answers ending with {template.end}: {stop_rate:.0%} of the 34 held-out SFT questions")
    for c in checks[:3]:
        print(f"\nQ: {c['question']}\nA: {c['model_answer'][:300]}")
    print(f"\nSelected checkpoint: {run_dir / 'best'}")

    if args.push_to_hub:
        model.push_to_hub(args.push_to_hub, private=True)
        tokenizer.push_to_hub(args.push_to_hub, private=True)
        print(f"Uploaded to https://huggingface.co/{args.push_to_hub}")


if __name__ == "__main__":
    main()
