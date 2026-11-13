# CV Assistant: SFT dataset (reviewed-v3)

## Contents and status

335 question–answer pairs: 301 training, 34 validation (10%). Version reviewed-v3 added 35 pairs (sft_301–sft_335) on 2026-11-13; see the last section. The first 50 were reviewed and accepted by a team member on 9 November 2026. The other 285 were drafted and checked with an AI assistant. The Phase 2 FAQ asks for at least 50 pairs checked by hand, which the first 50 meet; reviewing more is still worthwhile (docs/SFT_REVIEW_051_300.md and docs/SFT_REVIEW_301_335.md).

The 30 test questions (tests/test_questions.csv) are separate and are never used for SFT.

## Files

- data/sft_pairs.jsonl: all 335 examples, including source and review metadata.
- data/sft/train.jsonl: the 301 training examples.
- data/sft/validation.jsonl: the 34 held-out SFT examples (6 whole task families).
- data/sft/split.json: immutable ID lists and grouping decisions for this version.
- docs/SFT_AUDIT.json: counts, checks, test-file hash and limitations.
- docs/SFT_SCOPE.md: explicit scope policy for refusal and clarification examples.
- docs/SFT_REVIEW_051_300.md and docs/SFT_REVIEW_301_335.md: readable examples with sources, for the team's hand review.

## Training integration

Load only data/sft/train.jsonl for optimization. Use only data/sft/validation.jsonl for SFT validation. Never train on data/sft_pairs.jsonl wholesale: it includes validation examples. The training script must serialize ONLY question and answer, not source, reviewer, status or other metadata. Add the chat markers as special tokens and compute loss on the answer plus its end marker; mask the prompt and padding. train_sft.py implements this.

Begin SFT from the selected CPT epoch-2 checkpoint. Keep the CPT held-out document untouched for the common perplexity comparison across base, CPT and SFT. No text from that held-out document was used for this dataset.

## Split rationale

Related task families and exact duplicate answers are kept together. Five whole families were selected explicitly before SFT to obtain exactly 30 validation pairs: 22 editing examples and 8 advice/reference examples. Validation groups: concrete_tools, equipment_specificity, industry_expectations, pronoun_edit, reference_consent_family. This is a conservative grouped split, not random row shuffling; training should use seed 42. It tests transfer to held-out task families and is not representative of every behavior in the complete set, which should be reported. In particular, refusal examples remain in training and are assessed by the separate test set. Do not silently reshuffle after viewing performance.

## Quality and limitations

Source snippets were checked against the supplied training files, whose hashes match the manifest. New questions and answers use a conversational style without naming sources. Normalized exact question matches against the 30 tests were checked and none were found. The assistant also reviewed task intent and avoided direct test questions and apparent paraphrases. This is AI review, not a semantic guarantee.

The test set includes broad CV concepts, so many SFT examples instead apply writing principles to fictional supplied content. For instance, correcting supplied sentence grammar is different from answering which tense belongs to a previous role; drafting a specific bullet is different from defining an accomplishment statement. A human instructor may interpret some overlap more broadly. Review flagged cases if necessary; remove or replace ambiguous SFT examples, rather than changing tests to improve results.

This is a small synthetic dataset with repeated practice of task families. It contains 335 pairs, not 335 independent facts. It is intentionally weighted toward editing, concrete wording and formatting, with 15 off-topic refusals, 15 clarification/boundary examples and 15 unknowable-fact refusals. That emphasis can affect which behaviors improve after SFT. The source material is US/Canadian-oriented and does not establish universal country-specific CV rules. Do not claim guaranteed accuracy or grade outcomes.

## Reviewed-v3 additions (sft_301–sft_335)

- **15 `decline_unknown_fact` policy pairs.** The original 15 refusal pairs only covered off-topic requests (weather, recipes). Test IDs 28–30 check a different behaviour: declining CV-related questions whose answer the assistant cannot know. The new pairs cover employer-specific, personal and future facts (pay, applicant numbers, interview questions, contact details, live postings). None mentions deadlines, ATS scores or grades, so none copies or paraphrases a test question.
- **16 training pairs** from the new OpenStax training documents (online profiles, upload readability, letterhead consistency, strengths, KSAs, experience journals, keywords, outside review).
- **1 new held-out validation family, `career_goal_statement` (4 pairs).** The validation set stays at about 10% and still consists of whole task families.
- No pair uses either held-out CPT document. Checks: no exact question match, no shared 6- or 8-word sequence with any test question, and every `source_excerpt` appears verbatim in its source document.
- These 35 pairs are AI-authored and still need a hand check; use `docs/SFT_REVIEW_301_335.md`. The Phase 2 FAQ requires at least 50 pairs checked by hand; the first 50 already are.
