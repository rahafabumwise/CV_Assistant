# Data review update

Current corpus: 11 documents, 5,968 words by whitespace count. The three Open Oregon documents add 2,902 words. Model token counts must be recalculated; do not reuse the earlier 4,058-token figure.

Selected 12.1 passages add preparation, accurate self-inventory, employer research and job-description analysis. 12.2 adds comparisons between formats. 12.3 adds source-specific section guidance, concrete bullet revisions and writing conventions. Excluded full example CVs; kept explanatory bullet examples.

No complete duplicate documents were found. Topic overlap remains (education, experience, action verbs, formatting); different explanations are retained. This is not a claim that all semantic duplication was removed.

Conflicts and contextual advice:
- Oregon says not to list references on the resume; TRU lists references as optional. Future answers should explain context and employer instructions rather than assert a universal rule.
- Oregon gives a conditional GPA threshold of 3.0 and industry expectations. Do not treat this as a universal threshold across countries or grading systems.
- Oregon discusses one or two pages and discourages a partly filled second page; TRU calls two pages the standard. These are source recommendations, not universal requirements.
- Oregon's table-layout recommendation was excluded because the TRU ATS guidance discourages tables. Other original source text was not rewritten to hide disagreements.
- Functional formats are explained in Oregon; the initial TRU guidance prefers reverse chronological. Describe options with context.
- Source uses header to mean contact block; distinguish it from a word processor's header field.
- Keep numerical achievements in examples labelled as examples; never invent a student's results.

The existing 30 test questions are unchanged. Their topics overlap with the corpus by design, but do not copy test questions or paraphrases into SFT pairs. These documents are instructional text, not SFT examples.

The existing split.json in Colab is now stale. Recount tokens and redefine a whole-document split before full training. Education content now appears in several sources, so reassess the old education-only validation choice and document overlap. No training, token count or final split is supplied in this update.
