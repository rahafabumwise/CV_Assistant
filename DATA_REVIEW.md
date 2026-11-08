# Data review

Eight documents; 3,066 whitespace-counted words. Five new transcripts add 1,501 words. Token count has not been measured with a model tokenizer.

Cleaning removes timestamps, Narrator labels, page counters and separator lines. Each narration segment becomes a paragraph. A validation check confirms all narration words remain in source order after whitespace normalisation. Original transcript wording and examples are retained; no facts were added.

Repeated topics: overall layout overlaps with the formatting chapter; experience bullets overlap with accomplishment guidance; volunteering overlaps with transferable skills. These are different explanations, not duplicate documents. Exact ten-word sequence matches across documents: [{"a": "tru_action_verbs", "b": "tru_transferable_skills", "shared_10_word_sequences": 5}]. This check does not rule out semantic overlap.

Source tensions requiring care in later Q&A:
- The formatting chapter discourages images; the overall-format transcript allows a small graphic depending on sector. Qualify visual-design advice by sector and ATS needs.
- The book's two-page advice is Canadian source guidance, not a universal student-CV requirement.
- Hobbies (three to six items), employment bullets (three to five) and capitalization are source recommendations, not universal rules.
- The example 25% engagement increase is an illustration, never a result to invent for a user.
- Narration segments occasionally continue a sentence across paragraphs. All text is preserved.

No model training, tokenization, SFT generation, or final split has occurred. Preserve whole documents when splitting; assess overlapping chapters together before selecting held-out material. This small, single-source corpus is appropriate for an initial pipeline experiment; it does not guarantee a useful assistant or enough diversity for 300 strong Q&A pairs.
