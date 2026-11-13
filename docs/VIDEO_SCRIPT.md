# Demo video script (3 minutes maximum)

The brief asks for two things: the **same two questions** answered by the base, continued-pretrained and SFT models, then **running `score.py` and showing its results**. Record the screen with sound (for example with OBS, or *Win + Alt + R* on Windows) while the notebook is open in Colab.

| Time | Show | Say (roughly) |
|---|---|---|
| 0:00–0:20 | README on GitHub | "Our CV Assistant helps first-year students write their first CV. In Phase 2 we trained GPT-2 small in two stages and scored it on our 30 test questions." |
| 0:20–0:50 | `results/cpt_loss_curve.png`, then `config.yaml` | "Continued pretraining on 18 CV documents: held-out perplexity went from [ ] to [ ], and we kept epoch [ ]. All settings are in config.yaml." |
| 0:50–1:50 | Notebook section 6: run `score.py ask "Should I list my newest or oldest job first?"` | "Same question, same settings, three models. The base model just continues the text, CPT sounds more like a CV guide, and the SFT model answers in our format and stops." |
| | Run `score.py ask "What is my current university GPA? …"` | "This one should be refused. [Say what each model did.]" |
| 1:50–2:40 | Notebook section 5: run `score.py summarize --show 6,16,28` | "score.py reads both graders' scores and prints accuracy and refusal accuracy for each model. Our graders agreed at first on [ ]%." |
| 2:40–3:00 | `SCOREBOARD.md` | "SFT changed the format and refusals most; most remaining errors are missing knowledge, which RAG should fix in Phase 3." |

Tip: run section 6 once before recording, so the models are already downloaded and the answers appear quickly.
