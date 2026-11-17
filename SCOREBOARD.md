# Scoreboard

Every row is scored on the same 30 test questions (`tests/test_questions.csv`; 3 should be refused: IDs 28–30). All models use greedy decoding and at most 128 new tokens.
Held-out perplexity is measured on the 2 held-out CPT documents (about 2,000 scored tokens; 512-token window, stride 256).

| Version | Held-out perplexity | Accuracy | Refusal accuracy | Avg. latency (s) | Notes |
|---|---|---|---|---|---|
| Small model, base | 21.05 | 0.0% | 0% (0/3) | 1.25 | GPT-2 small (124M) |
| + continued pretraining | 19.37 | 0.0% | 0% (0/3) | 1.25 | best epoch of 3, lr 5e-5, 18 documents (14,646 tokens) |
| + SFT | 39.54 | 23.3% | 33% (1/3) | 0.20 | 301 training pairs (+34 validation), lr 1e-4, answers-only loss |

Earlier runs on the first 11-document corpus (decision log only; a different held-out set, so the numbers are not comparable with the table above): held-out perplexity 19.84 → 18.91 and 19.84 → 18.97 (epoch 2 of 3 in both). See `results/cpt_runs_11_documents.json`.