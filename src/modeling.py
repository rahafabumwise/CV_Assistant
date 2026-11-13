"""Model loading, held-out perplexity, and the one generate function every model uses."""
from __future__ import annotations

import math
import random
import time

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_model(name_or_path: str, device: str | None = None):
    """Load any of the three models (HF id, local folder or Hub repo) the same way."""
    device = device or get_device()
    tokenizer = AutoTokenizer.from_pretrained(name_or_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(name_or_path).to(device)
    model.config.pad_token_id = tokenizer.pad_token_id
    if getattr(model, "generation_config", None) is not None:
        model.generation_config.pad_token_id = tokenizer.pad_token_id
    model.eval()
    return model, tokenizer


@torch.no_grad()
def heldout_perplexity(model, tokenizer, texts: list[str], context: int = 512, stride: int = 256) -> dict:
    """Sliding-window perplexity; each token is scored once.
    Same method as the notebook run that produced base 19.84 / CPT 18.91."""
    model.eval()
    device = next(model.parameters()).device
    total_loss, total_tokens = 0.0, 0
    for text in texts:
        ids = tokenizer.encode(text, add_special_tokens=False)
        prev_end = 0
        for start in range(0, len(ids), stride):
            end = min(start + context, len(ids))
            new = end - prev_end
            inputs = torch.tensor([ids[start:end]], device=device)
            labels = inputs.clone()
            labels[:, :-new] = -100
            scored = (labels[:, 1:] != -100).sum().item()
            if scored:
                out = model(input_ids=inputs, labels=labels, use_cache=False)
                total_loss += out.loss.item() * scored
                total_tokens += scored
            prev_end = end
            if end == len(ids):
                break
    loss = total_loss / total_tokens
    return {"loss": loss, "perplexity": math.exp(loss), "scored_tokens": total_tokens,
            "context": context, "stride": stride}


@torch.no_grad()
def complete(model, tokenizer, prompt: str, max_new_tokens: int = 80) -> str:
    """Greedy plain-text continuation (for the 5 before/after CPT prompts)."""
    device = next(model.parameters()).device
    enc = tokenizer(prompt, return_tensors="pt").to(device)
    out = model.generate(**enc, do_sample=False, num_beams=1, max_new_tokens=max_new_tokens,
                         pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True)


@torch.no_grad()
def generate_answer(model, tokenizer, template, question: str, gen_cfg: dict) -> tuple[str, str, float]:
    """THE single function used to ask any model a question.

    Returns (clean_answer, raw_generation, seconds)."""
    device = next(model.parameters()).device
    enc = tokenizer(template.prompt(question), return_tensors="pt").to(device)
    stop_ids = [tokenizer.eos_token_id]
    end_id = tokenizer.convert_tokens_to_ids(template.end)
    if end_id is not None and end_id != tokenizer.unk_token_id and end_id < len(tokenizer):
        stop_ids.append(end_id)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    out = model.generate(
        **enc,
        do_sample=gen_cfg.get("do_sample", False),
        num_beams=gen_cfg.get("num_beams", 1),
        max_new_tokens=gen_cfg.get("max_new_tokens", 128),
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=stop_ids,
    )
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    seconds = time.perf_counter() - t0
    raw = tokenizer.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=False)
    return template.clean_output(raw, tokenizer.eos_token or "<|endoftext|>"), raw, seconds
