# CV assistant project data

Reviewed-v2 dataset: 11 cleaned documents, 5,741 words (whitespace count), and 30 evaluation questions. GPT-2 token counts must be recomputed. This package replaces the earlier data files at the SAME paths. It contains no model training code or weights.

## Install on GitHub

1. Open data/cpt/documents in your existing repository. Upload all 11 .txt files from this package's matching folder to replace the earlier files.
2. Open tests and upload test_questions.csv plus its README.md. This README belongs inside tests; it does not replace the project README.
3. At the repository root, upload README.md, ATTRIBUTION.md, DATA_REVIEW.md, DECISION_LOG.md, MISSING_CONTENT.md and source_manifest.json.
4. Keep other project files. Commit with: Review corpus consistency and revise evaluation set.

The dataset has 15 easy, 10 medium and 5 hard test cases; three are unanswerable. These are drafted examples, not student interview data. Read tests/README.md for review and scoring instructions. IDs 3, 14, 23 and 26 are revised before training with the instructor's permission as reported by the user.

## Next

Review as a team and freeze the test version. Refresh Colab from GitHub, re-discover the 11 .txt files, count tokens, and select a whole-document approximately 90/10 split with overlap checks. Do not rerun the old seven-document split. Record seed, actual split proportions and selected filenames in the training configuration. Only read data/cpt/documents/*.txt into continued pretraining. Never train on test_questions.csv or documentation. SFT pairs must be separate and must not copy or paraphrase test questions.

Data selection and removals are documented in DECISION_LOG.md; exact provenance and hashes are in source_manifest.json. Canadian and US sources are used; recommendations are not universal country-specific rules. Original source documents are not included in this ZIP. No training or model evaluation has been run for this update.
