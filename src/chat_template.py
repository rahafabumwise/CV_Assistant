"""The single chat template used for SFT training and for scoring all models.

    <|user|>
    {question}
    <|assistant|>
    {answer}<|end|>

GPT-2 has no chat template, so the three markers are added as special tokens
(train_sft.py). The base and CPT models do not know these tokens: for them the
markers are ordinary text, which is expected — the base model is the starting point.
"""
from __future__ import annotations


class ChatTemplate:
    def __init__(self, cfg: dict):
        t = cfg["chat_template"]
        self.user = t["user"]
        self.assistant = t["assistant"]
        self.end = t["end"]

    @property
    def special_tokens(self) -> list[str]:
        return [self.user, self.assistant, self.end]

    def prompt(self, question: str) -> str:
        """Everything the model sees before it starts answering."""
        return f"{self.user}\n{question.strip()}\n{self.assistant}\n"

    def completion(self, answer: str) -> str:
        """The part the model is trained to produce (loss is computed only here)."""
        return f"{answer.strip()}{self.end}"

    def clean_output(self, text: str, eos_text: str = "<|endoftext|>") -> str:
        """Cut generated text at the first stop marker."""
        cut = len(text)
        for marker in (self.end, self.user, self.assistant, eos_text):
            i = text.find(marker)
            if i != -1:
                cut = min(cut, i)
        return text[:cut].strip()


def add_chat_tokens(tokenizer, model, template: ChatTemplate) -> int:
    """Register the template markers as special tokens and resize embeddings.

    Safe to call on a model that already has them (adds nothing)."""
    added = tokenizer.add_special_tokens(
        {"additional_special_tokens": template.special_tokens}
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    if added:
        model.resize_token_embeddings(len(tokenizer))
    model.config.pad_token_id = tokenizer.pad_token_id
    if getattr(model, "generation_config", None) is not None:
        model.generation_config.pad_token_id = tokenizer.pad_token_id
    return added
