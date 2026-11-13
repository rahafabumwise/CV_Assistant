# CV Assistant: helping first-year students write their first CV

Team project for *Building LLM Systems: From Models to Production*.

**User:** first-year university students writing their first CV.
**Task:** answer their CV-writing questions correctly, and say "I don't have that information" when the answer cannot be known.

**Phase 2:** train our own small model (GPT-2 small, 124M parameters) in two stages, continued pretraining (CPT) and supervised fine-tuning (SFT), then score the base, CPT and SFT models on our 30 test questions.

- Results: [SCOREBOARD.md](SCOREBOARD.md)
- What we tried and decided: [docs/PHASE2_DECISION_LOG.md](docs/PHASE2_DECISION_LOG.md)
- Team checklist: [HANDOFF.md](HANDOFF.md)

## Quick start (Google Colab, free T4 GPU)

Open **[CV_Assistant_Phase2.ipynb](CV_Assistant_Phase2.ipynb)** in Colab, choose *Runtime → Change runtime type → T4 GPU*, then *Runtime → Run all* (about 15 minutes). It runs the three scripts below in order and explains the grading steps.

Or run the scripts yourself:

```bash
git clone https://github.com/rahafabumwise/CV_Assistant.git && cd CV_Assistant
pip install -r requirements.txt
python train_cpt.py            # Step 1: continued pretraining
python train_sft.py            # Step 2: supervised fine-tuning
python score.py generate       # Step 3: base, CPT and SFT answer the 30 test questions
# two people grade results/grading/*_grader1.csv and *_grader2.csv (score 1 / 0.5 / 0)
python score.py agree          # initial grader agreement; writes *_final.csv
# settle disagreements in *_final.csv; set error_category for every SFT answer below 1
python score.py summarize --show 6,16,28   # accuracy, refusal accuracy, scoreboard rows
python score.py ask "Should I list my newest or oldest job first?"   # demo: one question, all 3 models
```

All settings are in [`config.yaml`](config.yaml). To change a setting for one run, use `--set`, e.g. `python train_cpt.py --set cpt.epochs=2`. Outside Colab, also set `paths.output_dir` to a local folder.

## Repository layout

```
README.md                 this file
SCOREBOARD.md             one row per model version (every later phase adds rows)
HANDOFF.md                team checklist for finishing and submitting Phase 2
CV_Assistant_Phase2.ipynb Colab notebook that runs everything
config.yaml               ALL settings: models, training, chat template, generation
requirements.txt          pinned library versions
.env.example              names of secret variables (never commit real keys)
train_cpt.py              Step 1: continued pretraining
train_sft.py              Step 2: supervised fine-tuning
score.py                  runs the 3 models on the 30 test questions and scores them
src/                      shared code: config, data loading, chat template, model calls, plots
data/
  cpt/documents/          20 cleaned CV-guide texts (16,654 GPT-2 tokens)
  cpt/split.json          whole-document split: 18 train / 2 held out
  sft_pairs.jsonl         335 question–answer pairs with source and review metadata
  sft/                    train.jsonl (301), validation.jsonl (34), split.json
  source_manifest.json    source, licence, hash and edits for every document
tests/
  test_questions.csv      the 30 Phase 1 test questions (never used for training)
  README.md               scoring rules
results/                  metrics, loss curves, answers, grading sheets, results per model
docs/                     data review and decisions, SFT dataset notes, decision log, report draft
notebooks/                first CPT runs on the 11-document corpus (record only)
ATTRIBUTION.md            sources and licences
```

## Data

| | Size | Notes |
|---|---|---|
| CPT corpus | 20 documents, about 12,400 words, **16,654 GPT-2 tokens** | 11 from the TRU *Resume Catalogue* and Open Oregon *Technical Writing*; 9 added from four OpenStax textbooks |
| CPT split | **18 train (14,646 tokens) / 2 held out (2,008 tokens)**, by whole document | held out: `oregon_cv_preparation.txt`, `openstax_cs_portfolio_and_recommendations.txt`; no 15-word sequence shared |
| SFT pairs | **335**: 301 train / 34 validation (10%) | validation = 6 whole task families; 50 pairs checked by hand; no test-question overlap |
| Test set | 30 questions: 15 easy, 10 medium, 5 hard; **3 should be refused** (IDs 28–30) | written before any model was trained |

All text is openly licensed (CC BY-NC-SA 4.0 and CC BY 4.0); see [ATTRIBUTION.md](ATTRIBUTION.md). The data contains no personal data.

## Models and settings

| Stage | Starts from | Data | Key settings |
|---|---|---|---|
| Base | `openai-community/gpt2` | — | — |
| CPT | base | 18 documents | 512-token blocks, lr 5e-5, batch 2, up to 3 epochs, early stopping on held-out loss, seed 42 |
| SFT | selected CPT epoch | 301 pairs | template `<\|user\|>` … `<\|assistant\|>` … `<\|end\|>` (3 special tokens), loss on answers only, lr 1e-4, batch 8, 3 epochs, best epoch by validation loss |
| Scoring | — | 30 test questions | greedy decoding, max 128 new tokens, the same function for all 3 models |

## Where the checkpoints are

Checkpoints are **not** in Git. In Colab they are saved to Google Drive:

- CPT: `MyDrive/CV_Assistant/experiments/cpt_<date_time>/checkpoints/epoch_<N>`. The selected epoch is in `results/cpt_metrics.json` (`selected_checkpoint`).
- SFT: `MyDrive/CV_Assistant/experiments/sft_<date_time>/best`. The path is in `results/sft_metrics.json`.
- Shared Drive folder: **TODO: paste the share link here** (Drive → right-click `CV_Assistant` → Share → "Anyone with the link").

`config.yaml` uses `models.cpt: auto` and `models.sft: auto`, which pick the latest selected checkpoints automatically. To upload a checkpoint to the Hugging Face Hub instead, run `python train_cpt.py --push_to_hub <user>/cv-gpt2-cpt` with `HF_TOKEN` set.
