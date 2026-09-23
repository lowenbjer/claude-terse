# Benchmark

Two prompt sets ran through the same runner, scorer and judge. Each prompt ran once through `claude -p` with `--output-format stream-json`, September 2026.

## Public set

12 prompts in [bench/showcase_prompts.json](../bench/showcase_prompts.json): 10 engineering questions, 2 short documents. `{OUT}` in the two document prompts is the output directory the runner substituted. Run in an empty directory with no CLAUDE.md and no other plugins.

Results per model are in [docs/models](models/README.md): [Opus 5.5](models/opus-5-5.md) at effort high and medium, [Fable 5.1](models/fable-5-1.md) at effort high.

## Private set

40 prompts adapted from real sessions against a private codebase with its own CLAUDE.md: 20 analysis questions, 10 documents, 10 tasks that force a subagent. Fable 5.1 at effort high. Only aggregates are published. Live setup against the plugin:

| | live setup | terse |
|---|---|---|
| Chat words, 20 prompts | 10,094 | 5,453 |
| Output tokens | 109,751 | 50,182 |
| List-price cost | $24.3 | $11.8 |
| "X, not Y" per 1k (scorer) | 1.29 | 0.18 |
| Judge violations per 1k | 14.3 | 10.5 |
| Subagent report dashes per 1k (Opus subagents) | 12.7 | 13.6 |

The same set ran against eight rule texts and placements before the plugin text was fixed. Findings:

- Concrete bans hold in every configuration: 0 dashes in 120 chat replies and 57 documents.
- Rule placement and wording move the judged categories by 15 to 50 percent. Reframes halve, cadence drops 60 percent. Metaphor did not move in any configuration.
- Disabling other plugins had no style effect and saved 5.7k context tokens per call.
- Subagent dashes depend on the subagent model. Forcing Fable removed them at 28 percent higher cost per agent run. Giving Opus subagents the rule text did not.

## Scorer and judge

[bench/score.py](../bench/score.py) counts the items a script can check: dashes, a banned phrase list, ", not" sentences excluding numeric corrections, parentheses, closing offers, words.

[bench/judge.py](../bench/judge.py) sends each reply to Opus 5 with a nine-item rubric and asks for quotes and a count. The items: metaphor, reframes, self-labeling, reader grading, cadence, closers, bloat, formal register, slogans. One judge call per reply. Judge cost was about $0.07 per reply at list price.

Both scripts are included so the numbers can be reproduced on your own prompts.
