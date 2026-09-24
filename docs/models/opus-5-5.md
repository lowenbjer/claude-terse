# Opus 5.5

Run on 2026-09-23 with Claude Code 2.1.280, model id `claude-opus-5-5`, one run per prompt at effort high and one at effort medium. Every API message reported `claude-opus-5-5` as the model. Judge cost $3.02 for 40 chat replies.

| | high, vanilla | high, terse | change | medium, vanilla | medium, terse | change |
|---|---|---|---|---|---|---|
| Words, 10 chat replies | 5,959 | 1,876 | -69% | 5,524 | 1,911 | -65% |
| Median reply | 636 words | 177 words | -72% | 580 words | 181 words | -69% |
| Output tokens, 12 runs | 19,310 | 8,596 | -55% | 16,053 | 7,720 | -52% |
| Thinking tokens, 12 runs | 2,280 | 2,150 | | 369 | 1,158 | |
| List-price cost, 12 runs | $0.84 | $0.74 | -12% | $0.78 | $0.71 | -9% |
| Em or en dashes, 12 replies | 6 | 0 | -100% | 5 | 0 | -100% |
| Judge violations per 1k words | 11.1 | 2.7 | -76% | 10.1 | 2.6 | -74% |
| Metaphor per 1k | 3.69 | 1.07 | -71% | 3.26 | 1.05 | -68% |
| "X, not Y" reframes per 1k | 0.84 | 0.0 | -100% | 0.72 | 0.0 | -100% |
| Slogans per 1k | 1.17 | 0.0 | -100% | 0.54 | 0.0 | -100% |
| Cadence per 1k | 1.34 | 0.0 | -100% | 1.09 | 0.0 | -100% |
| Bloat per 1k | 3.02 | 1.07 | -65% | 3.62 | 1.57 | -57% |
| Closers per 1k | 1.17 | 0.53 | -55% | 1.09 | 0.0 | -100% |

Words per prompt at effort high, vanilla to terse: 489 to 167, 636 to 158, 569 to 175, 1,020 to 179, 723 to 230, 136 to 102, 779 to 192, 721 to 342, 636 to 190, 250 to 141. Documents: 167 to 84 and 317 to 205.

Findings:

- Vanilla Opus 5.5 ends 7 of 10 chat replies with an "In short:" paragraph or an offer such as "If you share the script, I can point to the exact lines." Terse ends 1 of 10 with a summary sentence.
- The 6 vanilla dashes are en dashes inside numeric ranges, 10 to 15 seconds and 10 to 100 times with a dash between the numbers. Terse writes "10 to 15 seconds".
- The 3 metaphors the judge found in terse replies at effort high: "reads cleanly in git log", "Common culprits are", "the TTL remains as a backstop".
- Effort changes length by 7% in vanilla and 2% in terse. The 150-word cap in the rules decides the length at either effort.
- Vanilla Opus 5.5 writes 29% more words than vanilla Fable 5.1 on the same prompts and has 40% fewer judged violations per 1,000 words. Terse replies on Opus 5.5 are 12% shorter than terse replies on Fable 5.1 and have 38% of their violation rate.

## Private set

Run on 2026-09-24, effort high, 40 prompts against a private codebase, see [docs/benchmark.md](../benchmark.md) for the prompt mix and the baseline definition. The baseline has the 1,886-word rule text in the project CLAUDE.md and nine other plugins enabled. The terse run has the plugin and nothing else.

| | baseline | terse | change |
|---|---|---|---|
| Chat words, 20 prompts | 9,705 | 4,782 | -51% |
| Median reply | 501 words | 211 words | -58% |
| Output tokens, 20 prompts | 75,718 | 44,057 | -42% |
| List-price cost, 20 prompts | $8.4 | $5.4 | -36% |
| Judge violations per 1k words | 9.9 | 6.3 | -36% |
| Metaphor per 1k | 3.09 | 1.88 | -39% |
| "X, not Y" reframes per 1k (judge) | 1.13 | 0.21 | -81% |
| Slogans per 1k | 0.52 | 0.21 | -60% |
| Cadence per 1k | 1.24 | 0.42 | -66% |
| Bloat per 1k | 3.50 | 3.35 | -4% |
| Subagent report dashes per 1k, 10 agent prompts | 0.4 | 0.0 | -100% |
| List-price cost, 10 agent prompts | $5.8 | $4.8 | -17% |

Claude Code chose Opus 5.5 for the Explore subagents in this session, where a Fable 5.1 session had used Opus 5. Bloat stays near 3.4 per 1k because the replies still open with a line about what the model is about to check.

Not measured: repeated runs of the same prompt.

Before and after for the Flask prompt, vanilla 636 words and terse 158 words, are in the [README](../../README.md#before-and-after).
