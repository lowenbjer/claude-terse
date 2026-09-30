# Add a model to the catalog

One run of the 12 public prompts per setup, one pull request. Cost is about $1 per run on Opus 5.5 at list price, more on larger models.

1. Install the plugin: `/plugin marketplace add lowenbjer/claude-terse` and `/plugin install terse@terse`.
2. Run the terse setup: `python3 bench/run.py <model-id> <label>`.
3. Run vanilla: `python3 bench/run.py <model-id> <label>-vanilla --vanilla`.
4. Optional judge pass, about $0.07 per chat reply: add `--judge` to both.
5. Open `bench/out/<label>/summary.json` and `row.md` for both runs.
6. Create `docs/models/<model>.md` with the date, Claude Code version, effort, the model id every reply reported (`models_reported` in summary.json), a table of vanilla against terse, and 2 to 5 findings from reading the replies.
7. Add one row per setup to the table in `docs/models/README.md`.
8. Open a pull request with the two `summary.json` files pasted in the body.

Rules for a row: one run per prompt, effort stated, the model id checked in `models_reported`. A run where the reported model differs from the requested one is not a row. Replies stay out of the repository except for quotes under 40 words in the findings.

The prompts are in [bench/showcase_prompts.json](../../bench/showcase_prompts.json). Change nothing in them, so rows compare.
