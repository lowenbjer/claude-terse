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
- Metaphor drops from 7.16 to 3.29 per 1,000 words. None of the eight rule texts tested on the private set moved it below 3.29.
- The 40-prompt private set on Fable 5.1: 10,094 to 5,453 chat words and $24.3 to $11.8 at list price, see [docs/benchmark.md](../benchmark.md).
- Explore-type subagents ran Opus 5 and kept 13 em dashes per 1,000 words with the rules in their context. Fable subagents wrote 0.1 per 1,000 without any rules.

## Version 1.2.2 rerun

Run on 2026-11-11 with Claude Code 2.1.322, effort high, same 12 prompts, terse 1.2.2. The runs used no setting sources, so no user settings and no other plugins applied. Judge rows are the mean of three passes.

| | vanilla | terse 1.2.2 | change |
|---|---|---|---|
| Words, 10 chat replies | 3,770 | 1,772 | -53% |
| Median reply | 399 words | 186 words | -54% |
| Output tokens, 12 runs | 10,433 | 6,035 | -42% |
| Thinking tokens, 12 runs | 278 | 0 | |
| List-price cost, 12 runs | $2.67 | $2.94 | +10% |
| Em or en dashes, 12 replies | 0 | 0 | |
| First person per 1k words | 1.59 | 0.0 | -100% |
| Bold lead-ins, 10 chat replies | 71 | 0 | -100% |
| Label lines, 10 chat replies | 7 | 8 | |
| Judge violations per 1k words | 17.6 | 6.8 | -61% |
| Metaphor per 1k | 6.63 | 3.76 | -43% |
| "X, not Y" reframes per 1k | 1.68 | 0.0 | -100% |
| Slogans per 1k | 1.15 | 0.0 | -100% |
| Cadence per 1k | 2.56 | 1.13 | -56% |
| Bloat per 1k | 4.95 | 1.69 | -66% |

Words per prompt, vanilla to terse: 335 to 175, 356 to 176, 442 to 185, 480 to 192, 530 to 194, 141 to 114, 500 to 186, 496 to 216, 343 to 214, 147 to 120. Documents: 81 to 60 and 878 to 696.

- Metaphor stays at 3.76 per 1,000 words, 6 to 7 hits in each judge pass. Three of them: "lock waits name the job", "earns its own column", "The branch wins only if".
- First person and bold lead-ins are 0 in the 10 chat replies. Label lines stay at 8.
- Output tokens fall 42% and cost rises 10%. The plugin adds about 1,900 cache-write tokens to each fresh session.
- In the 10-turn conversation with the 1.2.2 text, Fable 5.1 wrote 1,745 words, 2 bold lead-ins, 6 label lines and 11 judged violations, see [docs/benchmark.md](../benchmark.md#multi-turn-check).
