# CV assistant continued-pretraining starter data

Current collection: eight UTF-8 text documents, 3,066 words by whitespace count. This is a small starter corpus, not a complete Phase 2 submission. Token count must be measured with your chosen tokenizer.

## Update your existing repository

This update ZIP contains five NEW text files and replacement documentation. It relies on the three original text files already in your repository.

1. Extract this ZIP.
2. Open your repository root on GitHub, select Add file > Upload files, and drag in the contents of this folder (not its outer folder or ZIP).
3. Upload the data folder and all .md/.json files. The matching documentation paths replace the earlier starter documents. The three existing .txt files stay in place; the five new ones are added.
4. Commit with: Add five cleaned CV guidance transcripts.
5. Check data/cpt/documents/ contains eight .txt files.

## Next steps

Review DATA_REVIEW.md for source limitations. Prepare independent evaluation questions before looking at model outputs. Finalize the training corpus, then split approximately 90/10 by whole document, avoiding near-duplicate explanations across splits. No split is assigned yet. Use only data/cpt/documents/*.txt for continued pretraining; documentation and metadata are not training text.

SFT needs a separate 300–1,000 checked Q&A dataset, excluding test questions and paraphrases. It is not included in this package. This small collection can support a pipeline smoke test; evaluate coverage and diversity before deciding whether to add another source.

## Provenance

Source book: https://resumecatalogue.pressbooks.tru.ca/
Transcript chapter: https://resumecatalogue.pressbooks.tru.ca/chapter/resume-sections-explained/
Full credit and licence notes: ATTRIBUTION.md. Document paths, page numbers, word counts and hashes: source_manifest.json.
