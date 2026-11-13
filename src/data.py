"""Data loading: CPT documents, SFT pairs and test questions."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import torch
from torch.utils.data import Dataset

from .config import project_path


# ---------- Continued pretraining ----------

def load_cpt_split(cfg: dict) -> dict:
    split = json.loads(project_path(cfg["paths"]["cpt_split"]).read_text(encoding="utf-8"))
    for key in ("train", "validation"):
        for rel in split[key]:
            if not rel.endswith(".txt") or not project_path(rel).exists():
                raise FileNotFoundError(
                    f"{cfg['paths']['cpt_split']} lists '{rel}', which is not a CPT document. "
                    "This file must list .txt paths under data/cpt/documents/."
                )
    overlap = set(split["train"]) & set(split["validation"])
    assert not overlap, f"Documents in both train and validation: {overlap}"
    return split


def read_documents(paths: list[str]) -> list[str]:
    return [project_path(p).read_text(encoding="utf-8") for p in paths]


class CPTBlocks(Dataset):
    """Concatenate training documents (EOS between them) and cut into fixed blocks.
    Padding in the last block is masked out of the loss."""

    def __init__(self, texts: list[str], tokenizer, block_size: int = 512):
        ids: list[int] = []
        for text in texts:
            ids.extend(tokenizer.encode(text, add_special_tokens=False))
            ids.append(tokenizer.eos_token_id)
        self.n_tokens = len(ids)
        self.examples = []
        for start in range(0, len(ids), block_size):
            chunk = ids[start:start + block_size]
            pad = block_size - len(chunk)
            self.examples.append({
                "input_ids": torch.tensor(chunk + [tokenizer.pad_token_id] * pad),
                "attention_mask": torch.tensor([1] * len(chunk) + [0] * pad),
                "labels": torch.tensor(chunk + [-100] * pad),
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]


# ---------- SFT ----------

def load_jsonl(path) -> list[dict]:
    with open(project_path(path), encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


class SFTDataset(Dataset):
    """Question–answer pairs in the chat template, with loss on the answer only.

    Only `question` and `answer` are used; metadata (source, reviewer, ...) is ignored."""

    def __init__(self, rows: list[dict], tokenizer, template, max_length: int = 256):
        self.examples = []
        self.truncated = 0
        for row in rows:
            prompt_ids = tokenizer.encode(template.prompt(row["question"]), add_special_tokens=False)
            answer_ids = tokenizer.encode(template.completion(row["answer"]), add_special_tokens=False)
            ids = prompt_ids + answer_ids
            labels = [-100] * len(prompt_ids) + answer_ids  # mask the question
            if len(ids) > max_length:
                self.truncated += 1
                ids, labels = ids[:max_length], labels[:max_length]
            self.examples.append({"input_ids": ids, "labels": labels})

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]


def sft_collate(pad_token_id: int):
    def collate(batch):
        width = max(len(b["input_ids"]) for b in batch)
        input_ids, attention, labels = [], [], []
        for b in batch:
            pad = width - len(b["input_ids"])
            input_ids.append(b["input_ids"] + [pad_token_id] * pad)
            attention.append([1] * len(b["input_ids"]) + [0] * pad)
            labels.append(b["labels"] + [-100] * pad)  # padding never counts
        return {
            "input_ids": torch.tensor(input_ids),
            "attention_mask": torch.tensor(attention),
            "labels": torch.tensor(labels),
        }
    return collate


# ---------- Test questions ----------

def load_test_questions(cfg: dict) -> list[dict]:
    with open(project_path(cfg["paths"]["test_questions"]), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["should_refuse"] = r["source"].strip().upper().startswith("UNANSWERABLE")
    return rows


def normalize(text: str) -> str:
    """Lower-case, drop punctuation, collapse spaces (used for exact match)."""
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def check_no_test_overlap(sft_rows: list[dict], tests: list[dict], ngram: int = 8) -> list[str]:
    """Fail on exact question matches; warn on shared 8-word sequences.
    This is a lexical check only — the team must still read the pairs."""
    test_q = {normalize(t["question"]): t["id"] for t in tests}
    exact = [r["id"] for r in sft_rows if normalize(r["question"]) in test_q]
    if exact:
        raise ValueError(f"SFT questions identical to test questions: {exact}")

    def grams(text):
        w = normalize(text).split()
        return {tuple(w[i:i + ngram]) for i in range(len(w) - ngram + 1)}

    test_grams = {}
    for t in tests:
        for g in grams(t["question"] + " " + t["expected_answer"]):
            test_grams.setdefault(g, t["id"])
    warnings = []
    for r in sft_rows:
        hits = {test_grams[g] for g in grams(r["question"] + " " + r["answer"]) if g in test_grams}
        if hits:
            warnings.append(f"{r['id']} shares an {ngram}-word sequence with test id(s) {sorted(hits)}")
    return warnings
