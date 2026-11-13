# Reviewed data

11 whole documents, 5,741 whitespace-counted words. Token counts need to be recalculated. No exact full-document duplicates. Fifteen-word normalized phrase overlaps: []. This check does not detect all paraphrases; common topics remain intentionally covered across sources. Cross-split leakage cannot be certified until a split is chosen.

The overlapping topics are education, experience, skills, accomplishment statements and formatting. Similar domain facts are expected; duplicate passages and near-copy examples should not cross training/validation. Original chapter boundaries are retained.

Known conflicting recommendations were addressed through the documented omissions in DECISION_LOG.md. The initial scope is readable, general English first-CV guidance for internships/entry-level applications. It does not cover every country's or industry's CV rules. Source-specific numerical suggestions (e.g. bullet counts) are suggestions, not universal requirements. Format descriptions are alternatives, not a promise that one format is best for everyone.

Reference-sheet advice is now selected from Oregon; unconditional two-page advice was removed from TRU, leaving contextual Oregon length guidance. GPA relevance and grading-scale context remain without an arbitrary universal cutoff. Optional graphic advice was excluded for the first version. Sources are not rewritten to imply consensus.

The corpus remains small. This review does not guarantee model accuracy or a grade. The 30 revised evaluation items need team review before freezing. Test questions are excluded from corpus files. No final train/validation split or 300-pair SFT dataset is included.

**Update (Phase 2):** the whole-document CPT split is now frozen (data/cpt/split.json), and a 300-pair SFT dataset has been added (data/sft/, docs/SFT_DATASET.md).

**Update (reviewed-v3, 2026-11-13):** 9 OpenStax documents added; the corpus is now 20 documents and 16,654 GPT-2 tokens. Token counts and the 15-word overlap check were rerun on all 20 documents (no shared sequences). See DATA_DECISIONS.md.
