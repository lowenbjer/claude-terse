# Fable 5.1

Run on 2026-09-22 with Claude Code 2.1.278, model id `claude-fable-5-1`, effort high, one run per prompt.

| | vanilla | terse | change |
|---|---|---|---|
| Words, 10 chat replies | 4,610 | 2,125 | -54% |
| Median reply | 500 words | 196 words | -61% |
| Output tokens, 12 runs | 13,453 | 7,661 | -43% |
| Thinking tokens, 12 runs | 398 | 37 | |
| List-price cost, 12 runs | $1.93 | $1.75 | -9% |
| Em or en dashes, 12 replies | 0 | 0 | |
| Judge violations per 1k words | 18.4 | 7.1 | -61% |
| Metaphor per 1k | 7.16 | 3.29 | -54% |
| "X, not Y" reframes per 1k | 1.95 | 0.0 | -100% |
| Slogans per 1k | 1.52 | 0.0 | -100% |
| Cadence per 1k | 3.69 | 1.41 | -62% |
| Bloat per 1k | 3.90 | 2.35 | -40% |
| Closers per 1k | 0.22 | 0.0 | -100% |

Words per prompt, vanilla to terse: 363 to 191, 427 to 196, 489 to 185, 804 to 252, 608 to 261, 142 to 103, 500 to 218, 537 to 395, 530 to 177, 210 to 147. Documents: 85 to 107 and 199 to 106.

Findings:

- Vanilla Fable 5.1 writes 0 dashes on this set. The dash rule changes nothing here and holds on the private set too.
- Metaphor drops from 7.16 to 3.29 per 1,000 words and no further. None of the eight rule texts tested on the private set moved it below that.
- The 40-prompt private set ran on Fable 5.1 only: 10,094 to 5,453 chat words and $24.3 to $11.8 at list price, see [docs/benchmark.md](../benchmark.md).
- Explore-type subagents ran Opus 5 and kept 13 em dashes per 1,000 words with the rules in their context. Fable subagents wrote 0.1 per 1,000 without any rules.
