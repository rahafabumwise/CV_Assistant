# Phase 2 decision log

The report's "Decision log" section comes from here. Fill in the `[ ]` values after the final run.

## Data
- **Test set.** Test IDs 3, 14, 23 and 26 were replaced before any model was trained. All expected answers were written before any model output was seen.
- **First corpus (reviewed-v2):** 11 documents, 7,927 GPT-2 tokens, split 10 train / 1 held out (`oregon_cv_preparation.txt`, 889 scored tokens).
- **Problem found:** the SFT split files had been uploaded into `data/cpt/`, overwriting the CPT split. **Decision:** move them to `data/sft/`, restore the CPT split, and make the loader reject a CPT split that does not list `.txt` documents.
- **Instructor feedback:** the corpus is small. **Decision:** add 9 documents from four OpenStax textbooks (CC BY-NC-SA 4.0), taking only CV-related sections and applying the same cleaning rules as before. The corpus is now **20 documents and 16,654 tokens (2.1×)**.
  - We considered adding 2,484 real CVs from a Kaggle dataset. We decided against it for Phase 2: the CVs belong to experienced professionals, not first-year students; the license needed checking; and they would add a style mismatch rather than advice. Kept as an option for later.
- **New CPT split:** 18 train (14,646 tokens) / 2 held out (2,008 tokens, 12%), by whole document. We kept `oregon_cv_preparation.txt` and added `openstax_cs_portfolio_and_recommendations.txt`, which is not the source of any test answer and of no SFT pair. No 15-word sequence is shared between any two documents.
- **SFT data:** 300 pairs, of which 50 were checked by hand. The refusal examples only covered off-topic requests (weather, recipes), but test IDs 28–30 check CV-related questions that cannot be answered. **Decision:** add 15 "decline unknown fact" pairs that are clearly different from the test questions, plus 20 pairs from the new documents (4 of them a new held-out validation family). Total **335 pairs: 301 train / 34 validation**.
  - Checks: no exact matches with the test set, no shared 6- or 8-word sequences, and the most similar test question per pair was read by hand.

## Continued pretraining
- **11-document corpus, two runs on 2026-11-09:**
  - Run 1: held-out perplexity 19.84 → 19.18 → **18.91** → 19.17.
  - Run 2: 19.84 → 19.33 → **18.97** → 19.25.
  - In both runs, held-out loss rose at epoch 3 while training loss kept falling (overfitting). We stopped and kept epoch 2.
  - After training the completions used CV vocabulary but repeated themselves, for example "include your resume in your resume".
- **20-document corpus (final):** base [ ] → epoch 1 [ ] → epoch 2 [ ] → epoch 3 [ ]. Selected epoch [ ]; stopped early: [yes/no].
- Settings stayed the same (512-token blocks, lr 5e-5, batch 2, up to 3 epochs), so the only change between runs is the data.

## SFT
- **Template:** `<|user|>\n{question}\n<|assistant|>\n{answer}<|end|>`. The 3 markers are added as special tokens. Loss is computed on the answer and `<|end|>` only.
- **Learning rate 1e-4** (higher than CPT), because the 3 new token embeddings start untrained and the model must learn to stop with `<|end|>`. We keep the epoch with the lowest validation loss.
- **Final run:** validation loss [ ] → [ ] (epoch [ ] of 3). Answers ending with `<|end|>` on the 34 held-out SFT questions: [ ]%.
- [ ] If the stop rate is low, try 1 more epoch, record the result here, and keep whichever is better on validation.

## Scoring
- Graders: [name] and [name]. Initial agreement: base [ ]%, CPT [ ]%, SFT [ ]%.
- Disagreements were settled together, and the main reasons were: [ ].
- Test-case problems found: [none / list them; fix in the dev set only, and note each change here].
