# CV assistant project data

Reviewed-v2 dataset: 11 cleaned documents, 5,741 words (whitespace count), and 30 evaluation questions. It contains no model training code or weights.

## Install on GitHub

1. Open data/cpt/documents in your existing repository. Upload all 11 .txt files from this package's matching folder to replace the earlier files.
2. Open tests and upload test_questions.csv plus its README.md. This README belongs inside tests; it does not replace the project README.
3. At the repository root, upload README.md, ATTRIBUTION.md, DATA_REVIEW.md, DECISION_LOG.md, MISSING_CONTENT.md and source_manifest.json.
4. Keep other project files. Commit with: Review corpus consistency and revise evaluation set.

The dataset has 15 easy, 10 medium and 5 hard test cases; three are unanswerable. These are drafted examples, not student interview data. Read tests/README.md for review and scoring instructions. IDs 3, 14, 23 and 26 are revised before training with the instructor's permission as reported by the user.

## Work done

We have completed continued pretraining of GPT-2 on our CV-writing documents and compared its performance before and after training. Epoch 2 performed best, reducing validation perplexity from 19.84 to 18.91. The outputs became more relevant to CV writing, although repetition and incorrect advice remained. We also prepared 300 question–answer pairs for supervised fine-tuning, with 50 manually reviewed. Our next steps are to complete SFT, evaluate the base, CPT, and SFT models on the same 30 test questions, and analyse the results.
