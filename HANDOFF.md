# Phase 2: team checklist

**Due:** Saturday. Submit 1 PDF report (max 4 pages), 1 demo video (max 3 min) and the GitHub repository tagged `phase-2`.

## Already done (in the repository)
- [x] Data: 20 cleaned, openly licensed documents (16,654 tokens) with a whole-document 18 / 2 split. Sources, licences and every edit are recorded.
- [x] 30 test questions, frozen (3 should be refused).
- [x] 335 SFT pairs (301 / 34), checked against the test set. 50 were checked by hand.
- [x] `train_cpt.py`, `train_sft.py`, `score.py`, `config.yaml`, `src/`, all tested end to end.
- [x] The Colab notebook `CV_Assistant_Phase2.ipynb` runs everything.
- [x] README, decision log, report draft (`docs/REPORT_DRAFT.md`) and video script (`docs/VIDEO_SCRIPT.md`).

## To do, in order

| # | Task | Who | Time |
|---|---|---|---|
| 1 | Open `CV_Assistant_Phase2.ipynb` in Colab (T4 GPU) → **Run all**, then upload the downloaded `phase2_results.zip` contents to `results/` on GitHub | 1 person | 20 min |
| 2 | Share the Drive folder `MyDrive/CV_Assistant` with the team, and paste the link in README → "Where the checkpoints are" | same person | 2 min |
| 3 | **Grade.** Grader 1 fills `*_grader1.csv`, grader 2 fills `*_grader2.csv` (Drive → `experiments/results/grading`), separately, 1 / 0.5 / 0 | 2 people | 45 min each |
| 4 | Notebook section 5, first cell (`score.py agree`), then settle disagreements together in the 3 `*_final.csv` files and fill `error_category` for every SFT answer below 1 | together | 30 min |
| 5 | Notebook section 5, last cell (`score.py summarize`), then upload the final results ZIP contents to `results/` | 1 person | 10 min |
| 6 | Copy the rows from `results/scoreboard_rows.md` into `SCOREBOARD.md`, and fill the `[ ]` values in `docs/PHASE2_DECISION_LOG.md` | 1 person | 15 min |
| 7 | Finish `docs/REPORT_DRAFT.md`: fill the `[ ]` values, add 2–3 real error examples, add both loss curves, and export as PDF (max 4 pages) | 1–2 people | 1.5 h |
| 8 | Record the video using `docs/VIDEO_SCRIPT.md` | 1 person | 30 min |
| 9 | Tag the repository `phase-2` (GitHub → Releases → Draft a new release → tag `phase-2`) and submit the PDF, video link and repo link | 1 person | 5 min |

Optional, if there is time: hand-check more SFT pairs (`docs/SFT_REVIEW_301_335.md`, `docs/SFT_REVIEW_051_300.md`) and mark them `accepted` in `data/sft_pairs.jsonl`.

## Things to say in the report (they are not mistakes, but explain them)
- Test IDs 3 and 26 come from `oregon_cv_preparation.txt`, which is held out, so the model never trains on it. Wrong answers there are "knowledge missing" by design.
- Refusal accuracy is based on only 3 questions, so it can only be 0%, 33%, 67% or 100%.
- The base model does not follow the question–answer format. That is expected; it is the starting point.
- Held-out perplexity on the 20-document corpus cannot be compared with the 11-document runs, because the held-out set changed.

## Contribution statement (one line per member, at the end of the report)
- Ashraf: [data collection and cleaning, CPT runs, SFT data, …]
- [Teammate]: [ … ]
