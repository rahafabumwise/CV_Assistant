# CV assistant continued-pretraining starter data

This package converts the uploaded ResumeCatalogue.pdf into UTF-8 plain-text documents for Phase 2 continued pretraining. It is a cleaned starter corpus, not a complete Phase 2 submission.

## Contents and size

- Three chapter-level text files in data/cpt/documents/.
- 1,565 words by whitespace count. This is not a tokenizer count. Count tokens with your chosen model's tokenizer before reporting corpus size.
- source_manifest.json maps each file to its source URL, physical PDF pages, printed pages, word count, and checksum.
- MISSING_CONTENT.md records content linked from the PDF but absent from it.
- ATTRIBUTION.md preserves source credit, licence, and editing details.

## How to use

1. Unzip this folder on your computer and inspect the three text files.
2. Add the missing section transcripts or another checked source before freezing the dataset. This book alone has limited text and topic coverage; do not multiply or pad it to meet a target.
3. Keep each chapter as one document. Split approximately 90%/10% by whole document after collection is complete. Do not split paragraphs from a chapter across train and validation. Detect duplicates across sources first.
4. Upload the folder to Colab/Kaggle, or place data/cpt/documents/ in your project repository together with attribution.
5. Load only the .txt files in data/cpt/documents/ for continued pretraining. Do not train on this README, the manifest, attribution, or missing-content notes.
6. Prepare 300–1,000 checked SFT question-answer pairs separately, using training documents; keep 10% for SFT validation. Keep test questions and paraphrases out of those pairs.

## Split status

No final split is supplied: only three uneven chapters are present, one mainly a verb list. Holding out that list would give an unrepresentative validation set. Splitting a chapter into many files would not create independent documents. Finalize the document split after adding enough material. No training or model evaluation has been run.

## Cleaning and limitations

Removed repeated tables of contents, page footers, image credits for excluded images, QR instructions, and empty interactive/video placeholders. Kept original instructional wording and examples, normalised PDF line wrapping, and converted bullet markers to plain text. The action-verb table is flattened into a list; it has no category labels to preserve. This is text preparation, not a rewrite or independent verification of the author's advice.

The book's two-page recommendation and optional references section are source-specific Canadian guidance, not universal rules. Preserve this context in future Q&A. The example work histories are instructional examples, not facts about the user. Do not train the assistant to invent experience.

No SFT pairs or test questions are included. Freeze your separate evaluation questions before inspecting model outputs.
