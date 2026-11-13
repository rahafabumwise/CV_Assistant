"""Step 1 — continued pretraining of GPT-2 small on the CV documents.

    python train_cpt.py                      # uses config.yaml
    python train_cpt.py --set cpt.epochs=1   # override a setting for one run

What it does
  * trains on the 18 training documents in data/cpt/split.json (next-token objective,
    512-token blocks); the 2 held-out documents are never trained on
  * measures held-out perplexity before training and after every epoch
  * saves a checkpoint after every epoch and stops early when held-out loss rises
  * keeps the epoch with the lowest held-out loss

Checkpoints: <paths.output_dir>/cpt_<timestamp>/checkpoints/epoch_N   (Google Drive, NOT Git)
Results (results/ and a copy in <paths.output_dir>/results/):
    cpt_metrics.json       perplexity before/after, per-epoch losses, selected checkpoint
    cpt_step_losses.json   training loss at every optimizer step
    cpt_completions.json   the same 5 prompts before and after training
    cpt_loss_curve.png
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from src.config import base_arg_parser, load_config, project_path, save_result
from src.data import CPTBlocks, load_cpt_split, read_documents
from src.modeling import complete, get_device, heldout_perplexity, load_model, set_seed
from src.plotting import plot_losses


def main():
    parser = base_arg_parser(__doc__)
    parser.add_argument("--push_to_hub", default=None,
                        help="Optional Hugging Face repo id (e.g. team/cv-gpt2-cpt) to upload the selected checkpoint. Needs HF_TOKEN.")
    args = parser.parse_args()
    cfg = load_config(args.config, args.overrides)
    c = cfg["cpt"]
    set_seed(cfg["seed"])
    device = get_device()
    print(f"Device: {device}")

    run_dir = Path(cfg["paths"]["output_dir"]) / datetime.now(timezone.utc).strftime("cpt_%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "config_used.json").write_text(json.dumps(cfg, indent=2))
    print(f"Run folder: {run_dir}")

    split = load_cpt_split(cfg)
    train_texts = read_documents(split["train"])
    val_texts = read_documents(split["validation"])
    print(f"Documents: {len(split['train'])} train, {len(split['validation'])} held out")

    model, tokenizer = load_model(cfg["models"]["base"], device)

    def ppl():
        return heldout_perplexity(model, tokenizer, val_texts, c["eval_context"], c["eval_stride"])

    # ---- before training ----
    base_eval = ppl()
    before = [complete(model, tokenizer, p, c["completion_max_new_tokens"]) for p in c["completion_prompts"]]
    print(f"Base model: held-out loss {base_eval['loss']:.4f}, perplexity {base_eval['perplexity']:.2f} "
          f"({base_eval['scored_tokens']} tokens)")

    # ---- training data ----
    train_ds = CPTBlocks(train_texts, tokenizer, int(c["block_size"]))
    loader = DataLoader(train_ds, batch_size=int(c["batch_size"]), shuffle=True,
                        generator=torch.Generator().manual_seed(cfg["seed"]))
    print(f"Training: {train_ds.n_tokens:,} tokens → {len(train_ds)} blocks of {c['block_size']} "
          f"→ {len(loader)} steps per epoch")

    optimizer = torch.optim.AdamW(model.parameters(), lr=float(c["learning_rate"]),
                                  weight_decay=float(c["weight_decay"]))

    epochs, step_losses = [], []
    prev_val = base_eval["loss"]
    best = {"epoch": None, "val_loss": float("inf"), "path": None}
    stopped_early = False

    for epoch in range(1, int(c["epochs"]) + 1):
        model.train()
        tot, n = 0.0, 0
        for batch in loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad(set_to_none=True)
            loss = model(**batch, use_cache=False).loss
            if not torch.isfinite(loss):
                raise RuntimeError("Loss became NaN/inf — stop and inspect.")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), float(c["max_grad_norm"]))
            optimizer.step()
            scored = (batch["labels"][:, 1:] != -100).sum().item()
            tot += loss.item() * scored
            n += scored
            step_losses.append(loss.item())

        val = ppl()
        ckpt = run_dir / "checkpoints" / f"epoch_{epoch}"
        model.save_pretrained(ckpt, safe_serialization=True)
        tokenizer.save_pretrained(ckpt)
        row = {"epoch": epoch, "train_loss": tot / n, "val_loss": val["loss"],
               "val_perplexity": val["perplexity"], "checkpoint": str(ckpt)}
        epochs.append(row)
        print(f"Epoch {epoch}: train loss {row['train_loss']:.4f} | held-out loss {row['val_loss']:.4f} "
              f"| perplexity {row['val_perplexity']:.2f}")

        if val["loss"] < best["val_loss"]:
            best = {"epoch": epoch, "val_loss": val["loss"], "path": str(ckpt)}
        if c.get("early_stopping", True) and val["loss"] > prev_val:
            print("Held-out loss went up → stopping early (overfitting).")
            stopped_early = True
            break
        prev_val = val["loss"]

    # ---- after training: reload the SELECTED checkpoint and measure it the same way ----
    del model, optimizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer = load_model(best["path"], device)
    best_eval = ppl()
    after = [complete(model, tokenizer, p, c["completion_max_new_tokens"]) for p in c["completion_prompts"]]

    metrics = {
        "run": run_dir.name,
        "model": cfg["models"]["base"],
        "device": device,
        "seed": cfg["seed"],
        "settings": c,
        "split": {"train_documents": len(split["train"]), "heldout_documents": split["validation"],
                  "train_tokens_with_separators": train_ds.n_tokens,
                  "train_blocks": len(train_ds), "steps_per_epoch": len(loader),
                  "heldout_scored_tokens": base_eval["scored_tokens"]},
        "heldout_before": base_eval,
        "heldout_after": best_eval,
        "epochs": epochs,
        "stopped_early": stopped_early,
        "selected_epoch": best["epoch"],
        "selected_checkpoint": best["path"],
    }
    save_result(cfg, "cpt_metrics.json", metrics)
    save_result(cfg, "cpt_step_losses.json", step_losses)
    save_result(cfg, "cpt_completions.json",
                [{"prompt": p, "before": b, "after": a} for p, b, a in zip(c["completion_prompts"], before, after)])
    curve = project_path(cfg["paths"]["results_dir"]) / "cpt_loss_curve.png"
    plot_losses(step_losses, epochs, base_eval["loss"], "Continued pretraining (GPT-2 small, 18 documents)",
                curve, len(loader), best["epoch"])
    save_result(cfg, "cpt_loss_curve.png", curve.read_bytes())
    (run_dir / "cpt_metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"\nHeld-out perplexity: {base_eval['perplexity']:.2f} (base) → {best_eval['perplexity']:.2f} "
          f"(epoch {best['epoch']})")
    for p, b, a in zip(c["completion_prompts"], before, after):
        print(f"\n▶ {p}\n  BEFORE: {b[:200]!r}\n  AFTER : {a[:200]!r}")
    print(f"\nSelected checkpoint: {best['path']}")

    if args.push_to_hub:
        model.push_to_hub(args.push_to_hub, private=True)
        tokenizer.push_to_hub(args.push_to_hub, private=True)
        print(f"Uploaded to https://huggingface.co/{args.push_to_hub}")


if __name__ == "__main__":
    main()
