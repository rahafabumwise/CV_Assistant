# Scoreboard

Every row is scored on the same 30 test questions (`tests/test_questions.csv`; 3 should be refused: IDs 28–30). All models use greedy decoding and at most 128 new tokens.
Held-out perplexity is measured on the 2 held-out CPT documents (about 2,000 scored tokens; 512-token window, stride 256).

| Version | Held-out perplexity | Accuracy | Refusal accuracy | Avg. latency (s) | Notes |
|---|---|---|---|---|---|
| Small model, base | [ ] | [ ]% | [ ]% | [ ] | GPT-2 small (124M) |
| + continued pretraining | [ ] | [ ]% | [ ]% | [ ] | [selected epoch] of 3, lr 5e-5, 18 documents (14,646 tokens) |
| + SFT | [ ] | [ ]% | [ ]% | [ ] | 301 training pairs (+34 validation), lr 1e-4, epoch [ ] of 3 |

How to fill it in: run `python score.py summarize`, then copy the rows from `results/scoreboard_rows.md`. The Notes column comes from `results/cpt_metrics.json` and `results/sft_metrics.json`.

Earlier runs on the first 11-document corpus (decision log only; a different held-out set, so the numbers are not comparable with the table above): held-out perplexity 19.84 → 18.91 and 19.84 → 18.97 (epoch 2 of 3 in both). See `results/cpt_runs_11_documents.json`.
