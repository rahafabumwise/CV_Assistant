# CV Assistant — Phase 2 report (draft)

> How to use this draft: replace every `[ ]` with the real value from `results/` after the final run. Rewrite anything the results contradict, and keep the whole report to 4 pages or fewer. The reflection text describes what we *expect*; change it to match what you actually see.

## 1. Team and roles
| Member | Phase 2 role |
|---|---|
| [name] | Product lead |
| [name] | Data lead |
| [name] | Evaluation lead |
| [name] | Engineering lead |

## 2. Data
**Continued-pretraining corpus.**
- **Size:** 20 openly licensed CV-writing documents (about 12,400 words, **16,654 GPT-2 tokens**).
- **Sources:**
  - Thompson Rivers University *Resume Catalogue* (CC BY-NC-SA 4.0): 8 documents.
  - Open Oregon *Technical Writing* §12.1–12.3 (CC BY 4.0): 3 documents.
  - Four OpenStax textbooks (CC BY-NC-SA 4.0): 9 documents, added after the instructor noted that the first 11-document corpus (7,927 tokens) was small.
- **Cleaning:** we kept only CV-related text and removed figures, activities, cover-letter material, country-specific legal text and rules that contradicted other sources (for example, fixed page limits). Every edit is recorded in `data/source_manifest.json`.
- **Split:** by whole document, 18 training documents (14,646 tokens) and 2 held out (2,008 tokens, 12%). No 15-word sequence is shared between any two documents.

**SFT pairs.**
- **Total:** 335 question–answer pairs, 301 for training and 34 for validation (10%). The validation set holds 6 whole task families, so it measures transfer to unseen kinds of questions.
- **How they were made:**
  - 50 were drafted with an LLM from our documents and **checked by hand** by a team member.
  - The rest were AI-authored educational examples grounded in a source excerpt, or written from our scope policy: 15 off-topic refusals, 15 clarifications and 15 "I don't have that information" refusals.
- **How we kept them apart from the test set:**
  - No pair uses a held-out CPT document.
  - Our scripts check for exact question matches and shared 6- or 8-word sequences with the 30 test questions; there are none.
  - We read the most similar test question for every pair by TF-IDF similarity. For the 35 newest pairs the highest was 0.38, and those pairs only share words such as "action verbs". The earlier audit's highest was 0.57, on a different topic.
  - `train_sft.py` refuses to run if any SFT question equals a test question.

## 3. Training
- **Model:** GPT-2 small (124M), full fine-tuning on a free Colab T4 GPU, seed 42, and all settings in `config.yaml`.
- **Continued pretraining:**
  - Next-token objective on 512-token blocks: [ ] blocks, [ ] steps per epoch.
  - Learning rate 5e-5, batch 2, up to 3 epochs.
  - Held-out loss is measured after every epoch, and training stops when it rises.
  - **Held-out perplexity: [ ] (base) → [ ] (epoch [ ]).** [Stopped early at epoch [ ] because held-out loss rose while training loss kept falling. / Held-out loss fell every epoch.]
  - *Figure 1:* `results/cpt_loss_curve.png`.
- **SFT:**
  - Starts from the selected CPT epoch.
  - Chat template `<|user|>\n{question}\n<|assistant|>\n{answer}<|end|>`, with the 3 markers added as special tokens.
  - Loss on the answer tokens and `<|end|>` only; question and padding tokens are masked with -100.
  - Learning rate 1e-4, batch 8, 3 epochs; we keep the epoch with the lowest validation loss.
  - **Validation loss [ ] → [ ] (epoch [ ]).** On the 34 held-out SFT questions, [ ]% of answers end with `<|end|>`.
  - *Figure 2:* `results/sft_loss_curve.png`.

## 4. Scoring
- **Setup:** all three models answer the 30 test questions through the same function in `score.py`, with greedy decoding and at most 128 new tokens.
- **Grading:** every expected answer is an explanation rather than a single word, so all answers were graded by hand (1 correct, 0.5 partly correct, 0 wrong). For IDs 28–30 an answer is correct only if the model declines.
- **Graders:** [name] and [name] graded independently, and then settled disagreements together.
- **Initial agreement:** base [ ]%, CPT [ ]%, SFT [ ]% (`results/grader_agreement.json`).
- **Refusal accuracy** = the share of IDs 28–30 scored 1.

## 5. Results
| Version | Held-out perplexity | Accuracy | Refusal accuracy | Avg. latency (s) |
|---|---|---|---|---|
| Base GPT-2 small | [ ] | [ ]% | [ ]% | [ ] |
| + continued pretraining | [ ] | [ ]% | [ ]% | [ ] |
| + SFT | [ ] | [ ]% | [ ]% | [ ] |

**The same 3 test questions** (from `python score.py summarize --show 6,16,28`):

| | Q6 (easy): *Which verb tense should I use for a job I already left?* | Q16 (medium): *cafe → office internship* | Q28 (refuse): *exact internship deadline* |
|---|---|---|---|
| Base | [ ] | [ ] | [ ] |
| CPT | [ ] | [ ] | [ ] |
| SFT | [ ] | [ ] | [ ] |

## 6. Error analysis and reflection
**SFT failures by cause (out of [ ] answers scored below 1):** format failure [ ], hallucination [ ], knowledge missing [ ], refusal error [ ], test-case problem [ ].

Examples (2–3 real ones from `results/results_sft.csv`):
- *ID [ ]:* expected "[ ]"; the model said "[ ]". Classified as [ ] because [ ].
- *ID [ ]:* …

**1. What did continued pretraining change?** Held-out perplexity fell from [ ] to [ ]. The sample completions moved from general web text to CV vocabulary (sections, bullets, "resume"), but they still repeat themselves and mix up advice. CPT taught the model what CV text *sounds like*, not reliable facts: 16k tokens over [ ] optimizer steps is far too little to learn and keep specific rules. [Overfitting appeared after epoch [ ].]

**2. What did SFT change?** The base and CPT models ignore the `<|user|>`/`<|assistant|>` format and keep generating text. After SFT the model [answers in the format and stops with `<|end|>` in [ ]% of cases], produces short, CV-style answers and [sometimes] declines unknowable questions. Accuracy changed from [ ]% to [ ]%. SFT mainly changed the *behaviour* (format, length, refusals); most remaining errors are wrong or invented content.

**3. Why does the small model still make so many mistakes?** A 124M model trained on 16k tokens has very little capacity and almost no exposure to our domain. Pretraining at scale uses trillions of tokens, which is what lets large models store facts and follow instructions robustly. Our run shows that this knowledge cannot be added cheaply: we can teach a style and a format, but not reliable facts.

**4. What should RAG fix in Phase 3?** "Knowledge missing" and "hallucination" errors: with retrieval, a stronger model can read the relevant guide passage (for example the TRU font-size rule, or the held-out Oregon advice behind IDs 3 and 26) and cite it. RAG will not fix format failures of the small model. Refusal errors need retrieval plus an explicit "answer only from the retrieved text" rule.

## 7. Decision log
- Corpus expanded from 11 to 20 documents after the instructor's feedback; 2,484 Kaggle CVs considered but not used (experienced professionals rather than students, a style mismatch, and a license still to check).
- Fixed a repository mix-up in which the SFT split had overwritten the CPT split.
- 11-document CPT runs: 19.84 → 18.91 / 18.97 (epoch 2; overfitting at epoch 3), so we kept early stopping.
- Added 15 on-topic "I don't have that information" SFT pairs because the original refusals were all off-topic.
- SFT learning rate 1e-4 instead of 5e-5 so the new template tokens are learned; best epoch chosen by validation loss.
- [Anything else you try: what changed in the numbers, and what you decided.]

**Contributions.** [Name]: […]. [Name]: […].
