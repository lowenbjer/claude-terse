# Model catalog

One file per model tested as the main agent. Each file reports the public set: 12 prompts in [bench/showcase_prompts.json](../../bench/showcase_prompts.json), vanilla Claude Code against terse, one run per prompt, empty directory, no CLAUDE.md, no other plugins. [bench/score.py](../../bench/score.py) counts words, dashes and reframes. [bench/judge.py](../../bench/judge.py) sends each chat reply to Opus 5 with a nine-item rubric. Models get a file when someone runs the set on them.

| Model | Effort | Chat words, vanilla | Chat words, terse | Words | Judge violations per 1k, vanilla | Judge violations per 1k, terse | Violations | List cost, 12 runs | Date |
|---|---|---|---|---|---|---|---|---|---|
| [Opus 5.5](opus-5-5.md) | high | 5,959 | 1,876 | -69% | 11.1 | 2.7 | -76% | -12% | 2026-09-23 |
| [Opus 5.5](opus-5-5.md) | medium | 5,524 | 1,911 | -65% | 10.1 | 2.6 | -74% | -9% | 2026-09-23 |
| [Fable 5.1](fable-5-1.md) | high | 4,610 | 2,125 | -54% | 18.4 | 7.1 | -61% | -9% | 2026-09-22 |

Cost on this set moves less than words because the 12 runs read about 230,000 cached context tokens and write 8,000 to 19,000 output tokens. The 40-prompt private set in [docs/benchmark.md](../benchmark.md) measures long sessions and shows the 51% figure. It exists for Fable 5.1 only.

Subagents: the rules reach subagents through the SubagentStart hook. Subagent output was measured on the private set with Opus 5 and Sonnet 5 subagents, see [docs/benchmark.md](../benchmark.md). No subagent numbers exist for Opus 5.5.
