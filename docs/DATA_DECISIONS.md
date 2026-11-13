# Dataset review before training

Version: reviewed-v2. Review date: 2026-11-09. User reports instructor permits test-set changes. No model output was used to revise expected answers.

- tru_modern_resume_formatting: Removed unconditional two-page rule; retained contextual length discussion in Oregon.
- tru_modern_resume_formatting: Removed references from optional-section list to resolve conflict with Oregon separate-reference-sheet guidance.
- tru_overall_format: Excluded optional decorative-graphic advice for the initial general/ATS-readable CV scope.
- oregon_resume_formats: Removed subjective claim that hybrid is best.
- oregon_resume_formats: Removed unsupported format-superiority claim; format definitions and contextual use cases remain.
- oregon_resume_sections_and_guidelines: Excluded ambiguous header/address advice; TRU contact-block guidance remains.
- oregon_resume_sections_and_guidelines: Removed source-specific GPA threshold; TRU retains relevance and grading-scale context.
- oregon_resume_sections_and_guidelines: Removed inflexible full-page recommendation.
- oregon_resume_sections_and_guidelines: Removed weakly attributed page-per-decade heuristic.
- oregon_resume_sections_and_guidelines: Removed blanket objective-statement dismissal, inconsistent with adjacent graduate headline example.
- oregon_resume_sections_and_guidelines: Excluded ranking of referees as unnecessary for initial first-CV guidance.

Test-set changes: IDs 3, 14, 23, 26 replaced; details in tests/README.md. Original PDFs are unchanged. Corpus edits are selected-text omissions, not claims that the source authors agreed.

## Reviewed-v3 (2026-11-13): corpus expanded from 11 to 20 documents

The instructor noted that 11 documents (7,927 GPT-2 tokens) is small for continued pretraining. Nine documents were added from four OpenStax textbooks (CC BY-NC-SA 4.0, the same licence family as the TRU book). The corpus is now 20 documents and 16,654 GPT-2 tokens.

- Only résumé-related sections were taken: college résumés and online profiles, gaining experience, transferable skills, self-assessment, portfolios and recommendation letters, résumé keywords, persuasive résumés, and résumé presentation.
- Applying the same rules as reviewed-v2: a fixed page-length rule was removed; a universal "every résumé needs a career goal" claim was made conditional; cover-letter material, US-specific legal text, named personality tests, an uncited statistic, activities, figures and footnotes were excluded. Each change is listed per document in `data/source_manifest.json`.
- Checked against all 30 test questions: no new document contradicts an expected answer.
- No 15-word sequence is shared between any two of the 20 documents.

CPT split (frozen 2026-11-13, before training on the 20-document corpus): 18 training documents (14,646 tokens) and 2 held out (2,008 tokens, 12%): `oregon_cv_preparation.txt` (kept from the earlier split) and `openstax_cs_portfolio_and_recommendations.txt`. See data/cpt/split.json.

Earlier split, kept for the decision log: 10 training documents and 1 held out (`oregon_cv_preparation.txt`), used for the two 11-document CPT runs on 2026-11-09.
