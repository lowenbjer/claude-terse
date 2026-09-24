# Benchmark

Two prompt sets ran through the same runner, scorer and judge. Each prompt ran once through `claude -p` with `--output-format stream-json`, September 2026.

## Public set

12 prompts in [bench/showcase_prompts.json](../bench/showcase_prompts.json): 10 engineering questions, 2 short documents. `{OUT}` in the two document prompts is the output directory the runner substituted. Run in an empty directory with no CLAUDE.md and no other plugins.

Results per model are in [docs/models](models/README.md): [Opus 5.5](models/opus-5-5.md) at effort high and medium, [Fable 5.1](models/fable-5-1.md) at effort high.

## Private set

40 prompts adapted from real sessions against a private codebase with its own CLAUDE.md: 20 analysis questions, 10 documents, 10 tasks that force a subagent. Effort high on both models. Only aggregates are published.

The baseline differs by model. The Fable 5.1 baseline, run 2026-09-22, is the setup in daily use at the time: a 1,886-word user CLAUDE.md holding the writing rules, a memory index, nine plugins and hooks. The Opus 5.5 baseline, run 2026-09-24, puts the same 1,886-word rules in the project CLAUDE.md and enables the same nine plugins. It has no memory index and no hooks. On Fable that arrangement wrote 9,606 chat words against the 10,094 of the setup in daily use.

| | Fable 5.1 baseline | Fable 5.1 terse 1.0.0 | Opus 5.5 baseline | Opus 5.5 terse 1.0.0 | Opus 5.5 terse 1.1.0 |
|---|---|---|---|---|---|
| Chat words, 20 prompts | 10,094 | 5,453 (-46%) | 9,705 | 4,782 (-51%) | 4,468 (-54%) |
| Median reply | 530 words | 220 words | 501 words | 211 words | 193 words |
| Output tokens, 20 prompts | 109,751 | 50,182 (-54%) | 75,718 | 44,057 (-42%) | 43,747 (-42%) |
| List-price cost, 20 prompts | $24.3 | $11.8 (-51%) | $8.4 | $5.4 (-36%) | $5.7 (-32%) |
| "X, not Y" per 1k (scorer) | 1.29 | 0.18 | 1.65 | 0.63 | 0.22 |
| First person per 1k (scorer) | 3.96 | 3.48 | 5.15 | 4.18 | 1.57 |
| Judge violations per 1k | 14.3 | 10.5 (-27%) | 9.9 | 6.3 (-36%) | 4.3 (-57%) |
| Judge metaphor per 1k | 3.57 | 3.67 | 3.09 | 1.88 | 1.57 |
| Judge reframes per 1k | 1.29 | 0.92 | 1.13 | 0.21 | 0.0 |
| Judge slogans per 1k | 1.29 | 1.28 | 0.52 | 0.21 | 0.45 |
| Judge cadence per 1k | 2.58 | 1.28 | 1.24 | 0.42 | 0.22 |
| Judge bloat per 1k | 5.25 | 3.48 | 3.50 | 3.35 | 2.01 |
| Subagent model chosen by Claude Code | Opus 5 | Opus 5 | Opus 5.5 | Opus 5.5 | Opus 5.5 |
| Subagent report dashes per 1k, 10 agent prompts | 12.7 | 13.6 | 0.4 | 0.0 | 0.0 |
| List-price cost, 10 agent prompts | $15.3 | $8.4 | $5.8 | $4.8 | $4.4 |

Document prompts run with a 14-turn budget. The Opus 5.5 baseline hit it in 4 of 10 document runs and terse in 1 of 10, so document words are not compared.

The 7 first-person hits left in the 1.1.0 chat replies are all inside quoted user phrases such as "my pipeline". The 1.1.0 agent-prompt replies have 0.

The same set ran against eight rule texts and placements before the plugin text was chosen. Findings:

- Concrete bans hold in every configuration: 0 dashes in 120 chat replies and 57 documents.
- Rule placement and wording move the judged categories by 15 to 50 percent. Reframes drop 50 percent and cadence 60 percent. Metaphor did not move in any configuration.
- Disabling other plugins had no style effect and saved 5.7k context tokens per call.
- Subagent dashes depend on the subagent model. Forcing Fable removed them at 28 percent higher cost per agent run. Giving Opus 5 subagents the rule text did not. Opus 5.5 subagents wrote 3 dashes in 7,735 words without the rules and 0 in 5,494 words with them.

## Scorer and judge

[bench/score.py](../bench/score.py) counts the checkable items: dashes, first-person words ("I", "me", "my", "let me"), banned phrases, closing offers, parentheses and words. It also counts ", not" sentences, excluding numeric corrections such as "11, not 12".

[bench/judge.py](../bench/judge.py) sends each reply to Opus 5 with a nine-item rubric and asks for quotes and a count. The items: metaphor, reframes, self-labeling, reader grading, cadence, closers, bloat, formal register, slogans. One judge call per reply. Judge cost was about $0.07 per reply at list price.

Both scripts are in [bench/](../bench).
