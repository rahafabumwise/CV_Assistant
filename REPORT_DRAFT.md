# CV Assistant — Phase 2 Report

## 1. Team and roles
| Member | Phase 2 role |
|---|---|
| Rahaf Abu Muwais | Product lead & Data lead |
| Mariam Al-Tibi | Engineering lead & Evaluation lead |
| Raja Ibrahim | Documentation & Presentation support |

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
  - Next-token objective on 512-token blocks, learning rate 5e-5, batch 2, up to 3 epochs.
  - Held-out loss is measured after every epoch, and training stops when it rises.
  - **Held-out perplexity: 21.05 (base) → 19.37 (best CPT checkpoint).** Held-out perplexity improved by 1.68 points on the unseen CV documents.
  - *Figure 1:* [أدرجي هنا صورة cpt_loss_curve.png]
- **SFT:**
  - Starts from the selected CPT checkpoint.
  - Chat template `<|user|>\n{question}\n<|assistant|>\n{answer}<|end|>`, with the 3 markers added as special tokens.
  - Loss on the answer tokens and `<|end|>` only; question and padding tokens are masked with -100.
  - Learning rate 1e-4, batch 8, 3 epochs; we keep the epoch with the lowest validation loss.
  - **Held-out perplexity after SFT:** 39.54 (rises on raw document text as SFT shifts the output distribution toward concise Q&A responses ending in `<|end|>`).
  - *Figure 2:* [أدرجي هنا صورة sft_loss_curve.png]

## 4. Scoring
- **Setup:** all three models answer the 30 test questions through the same function in `score.py`, with greedy decoding and at most 128 new tokens.
- **Grading:** every expected answer is an explanation rather than a single word, so all answers were graded by hand (1 correct, 0.5 partly correct, 0 wrong). For IDs 28–30 an answer is correct only if the model declines.
- **Graders:** Rahaf Abu Muwais (Grader 1) and Mariam Al-Tibi (Grader 2) graded independently, and then settled disagreements together.
- **Initial agreement:** base 100% (30/30), CPT 100% (30/30), SFT 73% (22/30) (`results/grader_agreement.json`). The 8 disagreed SFT items (IDs 1, 9, 10, 11, 17, 24, 25, 29) were resolved jointly.
- **Refusal accuracy** = the share of IDs 28–30 scored 1.

## 5. Results
| Version | Held-out perplexity | Accuracy | Refusal accuracy | Avg. latency (s) |
|---|---|---|---|---|
| Base GPT-2 small | 21.05 | 0.0% | 0% (0/3) | 1.25 |
| + continued pretraining | 19.37 | 0.0% | 0% (0/3) | 1.25 |
| + SFT | 39.54 | 23.3% | 33% (1/3) | 0.20 |

**The same 3 test questions** (from `python score.py summarize --show 6,16,28`):

| | Q6 (easy): *Which verb tense should I use for a job I already left?* | Q16 (medium): *cafe → office internship* | Q28 (refuse): *exact internship deadline* |
|---|---|---|---|
| Base | Repeats the question verbatim (*"Which verb tense should I use for a job I already left?"*). | *(Empty output)* | Repeats the question verbatim. |
| CPT | Repeats the question in a loop separated by `<|career|>` markers. | Outputs repetitive role tags (`<|manager|>`, `<|employee|>`). | Repeats the question with `<|student|>` and `<|workplace|>` tags. |
| SFT | *"Use the same verb tense for both tasks."* | *"Use the application portal to find a suitable job posting."* | *"I can't predict the exact application deadline. Check the application portal or the job board..."* |

## 6. Error analysis and reflection
**SFT failures by cause (out of 27 answers scored below 1):** format failure 4, hallucination 12, knowledge missing 9, refusal error 2, test-case problem 0.

Examples (real cases from `results/grading/sft_final.csv`):
- *ID 6:* expected *"Use past tense for a previous role."*; the model said *"Use the same verb tense for both tasks."* Classified as **hallucination** because it followed the Q&A format fluently but invented incorrect CV advice.
- *ID 3:* expected *"Yes. Save a copy so you can tailor your CV..."*; the model said *"No. Keep the job description clear and concise..."* Classified as **knowledge missing** because this rule comes from the held-out Open Oregon document excluded from training.
- *ID 11:* expected two distinct action verbs; the model wrote *"Use action verbs in the bullet, such as 'listened' or 'listened.'"* Classified as **format failure** due to token-level repetition.

**1. What did continued pretraining change?** Held-out perplexity fell from 21.05 to 19.37. The sample completions moved from general web text to CV vocabulary (sections, bullets, "resume", role markers), but they still repeat themselves and mix up advice. CPT taught the model what CV text *sounds like*, not reliable facts: 16k tokens is far too little to learn and retain specific rules.

**2. What did SFT change?** The base and CPT models ignore the `<|user|>`/`<|assistant|>` format and keep generating text until hitting the 128-token limit (1.25s latency). After SFT, the model answers concisely in the chat format and stops cleanly with `<|end|>` (dropping latency to 0.20s), and correctly refuses out-of-scope questions like ID 28. Accuracy changed from 0.0% to 23.3%, and refusal accuracy from 0% to 33%. SFT mainly changed the *behaviour* (format, length, refusals); most remaining errors are wrong or invented content.

**3. Why does the small model still make so many mistakes?** A 124M model trained on 16k tokens has very little capacity and almost no exposure to our domain. Pretraining at scale uses trillions of tokens, which is what lets large models store facts and follow instructions robustly. Our run shows that this knowledge cannot be added cheaply: we can teach a style and a format, but not reliable facts.

**4. What should RAG fix in Phase 3?** "Knowledge missing" (9 cases) and "hallucination" (12 cases) errors: with retrieval, a stronger model can read the relevant guide passage (for example the TRU font-size rule in ID 13, or the held-out Oregon advice behind IDs 3 and 26) and cite it. RAG will not fix format failures of the small model. Refusal errors (IDs 29–30) need retrieval plus an explicit "answer only from the retrieved text" rule.

## 7. Decision log
- Corpus expanded from 11 to 20 documents after the instructor's feedback; 2,484 Kaggle CVs considered but not used (experienced professionals rather than students, a style mismatch, and a license still to check).
- Fixed a repository mix-up in which the SFT split had overwritten the CPT split.
- 11-document CPT runs: 19.84 → 18.91 / 18.97 (epoch 2; overfitting at epoch 3), so we kept early stopping.
- Added 15 on-topic "I don't have that information" SFT pairs because the original refusals were all off-topic.
- SFT learning rate 1e-4 instead of 5e-5 so the new template tokens are learned; best epoch chosen by validation loss.

**Contributions.** **Rahaf Abu Muwais:** Collected and cleaned the 20 CV documents, created the 335 SFT pairs, implemented the training and evaluation scripts (`train_cpt.py`, `train_sft.py`, `score.py`), and completed Grader 1 scoring. **Mariam Al-Tibi:** Configured and executed the GPU training and evaluation pipeline, performed Grader 2 scoring, resolved grading disagreements and SFT error categorization, and compiled the final results. **Raja Ibrahim:** Assisted with formatting the final report.

**Contributions.** [Name]: […]. [Name]: […].
