# CV assistant continued-pretraining data

11 cleaned text documents from TRU Resume Catalogue and selected Open Oregon Technical Writing sections. Total: 5,968 whitespace-counted words. Token counts require the chosen tokenizer. This remains a small educational experiment, not a production-ready assistant.

## Files

- data/cpt/documents/: eight original TRU texts plus three new Oregon texts.
- tests/test_questions.csv: existing 30 evaluation questions; unchanged by this update.
- source_manifest.json: source paths, PDF pages, licences, word counts and checksums for all 11 documents.
- ATTRIBUTION.md: credit and licence details.
- DATA_REVIEW.md: selection decisions, conflicting recommendations and limitations.
- MISSING_CONTENT.md: original TRU interactive-content collection status.

## Install this update

This ZIP is an addition to your existing repository, not a complete replacement. Upload its three .txt files directly inside the EXISTING data/cpt/documents folder. Upload README.md, ATTRIBUTION.md, DATA_REVIEW.md and source_manifest.json at the repository root to replace those files. Keep all eight earlier .txt files, MISSING_CONTENT.md and tests/test_questions.csv.

## Continue in Colab

Refresh the repository using git pull before rerunning file discovery and token counting. The earlier split.json is provisional and stale; do not use it for training until it has been regenerated and checked. Only tokenize .txt files in data/cpt/documents. Do not train on documentation or test questions.

Choose and record a whole-document split after checking cross-source repetition. Use approximately 90/10 and report actual document and token proportions. Prepare 300–1,000 separate checked SFT pairs, with test questions and paraphrases excluded. No training scripts, final split or SFT pairs are included yet.

## Scope

English first-CV guidance for students and recent graduates. Sources use Canadian and US conventions; answers must not treat their recommendations as universal country-specific rules. See DATA_REVIEW.md.
