"""Loss-curve plots saved to results/."""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_losses(step_losses, epoch_rows, baseline_val, title, path, steps_per_epoch, selected_epoch=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    if step_losses:
        xs = [(i + 1) / steps_per_epoch for i in range(len(step_losses))]
        ax.plot(xs, step_losses, alpha=0.35, label="Training loss (per step)")
    ax.plot([r["epoch"] for r in epoch_rows], [r["train_loss"] for r in epoch_rows],
            marker="o", label="Training loss (epoch mean)")
    val_x = [r["epoch"] for r in epoch_rows]
    val_y = [r["val_loss"] for r in epoch_rows]
    if baseline_val is not None:
        val_x, val_y = [0] + val_x, [baseline_val] + val_y
    ax.plot(val_x, val_y, marker="o", label="Validation loss")
    if selected_epoch is not None:
        row = next(r for r in epoch_rows if r["epoch"] == selected_epoch)
        ax.scatter([selected_epoch], [row["val_loss"]], s=140, facecolors="none",
                   edgecolors="green", linewidths=2, label=f"Selected: epoch {selected_epoch}")
    ax.set(xlabel="Epoch (0 = before training)", ylabel="Loss", title=title)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)
