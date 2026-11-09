# CV Assistant: SFT dataset v1

## Contents and status

300 question–answer pairs: 270 training, 30 validation. The first 50 retain their original IDs and user-approved wording. The remaining 250 are AI-authored and AI-checked; they are not labelled as human reviewed. Approval was recorded from the project owner's two chat messages on 9 November 2026. The wording of the first 50 was not changed.

The original 30 test questions are separate and unchanged. This package does not replace tests/test_questions.csv, CPT documents, the CPT split, or the epoch-2 model checkpoint.

## Upload to GitHub

Copy this package's data and docs contents into the matching locations in the repository. Keep SFT_README.md and SFT_ATTRIBUTION.md at the repository root. Do not overwrite your project's existing README.md or ATTRIBUTION.md with these files. No model weights or secrets are included.

- data/sft_pairs.jsonl: all 300 examples, including source and review metadata.
- data/sft/train.jsonl: the 270 training examples.
- data/sft/validation.jsonl: the 30 held-out SFT examples.
- data/sft/split.json: immutable ID lists and grouping decisions for this version.
- docs/SFT_AUDIT.json: counts, checks, test-file hash and limitations.
- docs/SFT_SCOPE.md: explicit scope policy for refusal and clarification examples.
- docs/SFT_REVIEW_051_300.md: readable new examples with sources for optional additional review.

## Training integration

Load only data/sft/train.jsonl for optimization. Use only data/sft/validation.jsonl for SFT validation. Never train on data/sft_pairs.jsonl wholesale: it includes validation examples. The training script must serialize ONLY question and answer, not source, reviewer, status or other metadata. Add the chat markers as special tokens and compute loss on the answer plus its end marker; mask the prompt and padding. These files do not themselves implement SFT training.

Begin SFT from the selected CPT epoch-2 checkpoint. Keep the CPT held-out document untouched for the common perplexity comparison across base, CPT and SFT. No text from that held-out document was used for this dataset.

## Split rationale

Related task families and exact duplicate answers are kept together. Five whole families were selected explicitly before SFT to obtain exactly 30 validation pairs: 22 editing examples and 8 advice/reference examples. Validation groups: concrete_tools, equipment_specificity, industry_expectations, pronoun_edit, reference_consent_family. This is a conservative grouped split, not random row shuffling; training should use seed 42. It tests transfer to held-out task families and is not representative of every behavior in the complete set, which should be reported. In particular, refusal examples remain in training and are assessed by the separate test set. Do not silently reshuffle after viewing performance.

## Quality and limitations

Source snippets were checked against the supplied training files, whose hashes match the manifest. New questions and answers use a conversational style without naming sources. Normalized exact question matches against the 30 tests were checked and none were found. The assistant also reviewed task intent and avoided direct test questions and apparent paraphrases. This is AI review, not a semantic guarantee.

The test set includes broad CV concepts, so many SFT examples instead apply writing principles to fictional supplied content. For instance, correcting supplied sentence grammar is different from answering which tense belongs to a previous role; drafting a specific bullet is different from defining an accomplishment statement. A human instructor may interpret some overlap more broadly. Review flagged cases if necessary; remove or replace ambiguous SFT examples, rather than changing tests to improve results.

This is a small synthetic dataset with repeated practice of task families. It contains 300 pairs, not 300 independent facts. It is intentionally weighted toward editing, concrete wording and formatting, with 15 explicit out-of-scope refusals and 15 clarification/boundary examples. That emphasis can affect which behaviors improve after SFT. The source material is US/Canadian-oriented and does not establish universal country-specific CV rules. Do not claim guaranteed accuracy or grade outcomes.

## Next step

Check the counts after upload. Then build train_sft.py and config.yaml to enforce the chat template, answer-only loss and split above. Run a short smoke test before the full 2–3 epochs. Preserve the three-model comparison and score all versions through the same score.py settings.
