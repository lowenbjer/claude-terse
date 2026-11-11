# Fable 5.2

Run on 2026-11-11 with Claude Code 2.1.322, model id `claude-fable-5-2`, effort high, one run per prompt, terse 1.2.2. Every reply reported `claude-fable-5-2` as the model. The runs used no setting sources, so no user settings, no CLAUDE.md and no other plugins applied. The judge read each chat reply three times. Judge rows are the mean of the three passes.

| | vanilla | terse | change |
|---|---|---|---|
| Words, 10 chat replies | 3,762 | 1,649 | -56% |
| Median reply | 396 words | 177 words | -55% |
| Output tokens, 12 runs | 12,852 | 13,926 | +8% |
| Thinking tokens, 12 runs | 1,338 | 8,292 | |
| List-price cost, 12 runs | $2.15 | $2.60 | +21% |
| Em or en dashes, 12 replies | 2 | 0 | -100% |
| First person per 1k words | 2.66 | 0.0 | -100% |
| Bold lead-ins, 10 chat replies | 73 | 0 | -100% |
| Label lines, 10 chat replies | 9 | 2 | -78% |
| Headers, 10 chat replies | 14 | 0 | -100% |
| Judge violations per 1k words | 12.0 | 2.6 | -78% |
| Metaphor per 1k | 5.85 | 0.61 | -90% |
| "X, not Y" reframes per 1k | 1.59 | 0.0 | -100% |
| Slogans per 1k | 0.35 | 0.20 | -43% |
| Cadence per 1k | 0.53 | 0.0 | -100% |
| Bloat per 1k | 2.84 | 1.21 | -57% |
| Closers per 1k | 0.53 | 0.0 | -100% |

Words per prompt, vanilla to terse: 272 to 182, 337 to 148, 402 to 181, 562 to 183, 417 to 167, 135 to 90, 390 to 187, 678 to 229, 425 to 173, 144 to 109. Documents: 80 to 60 and 1,149 to 513.

Findings:

- The three judge passes counted 4, 5 and 4 violations in the 10 terse replies. The same rule text on Fable 5.1 on the same day gave 12, 11 and 13.
- Metaphor falls to 1 hit in 1,649 words. No rule text had moved Fable 5.1 below 3.3 per 1,000 words. The one hit is the heading word "Bites", which repeats the prompt's own wording.
- One of the judged violations is "(opinion)", which rule 11 asks for.
- Thinking rises from 1,338 to 8,292 tokens over 12 runs. Visible output on the 10 chat prompts falls from 7,949 to 3,521 tokens. Billed output tokens rise 8%.
- Cost per single-prompt session rises 21%. The plugin adds about 2,000 cache-write tokens to each fresh session, and the extra thinking is billed as output.
- 7 of 10 terse replies run over the 150-word cap. The longest is 229 words.
- Vanilla Fable 5.2 writes the same length as vanilla Fable 5.1 on this set, 3,762 against 3,770 words. It writes 14 headers where Fable 5.1 writes 1.

## Second run and effort medium

The 10 chat prompts ran a second time at effort high and once at effort medium, with one judge pass each.

| | high, vanilla | high, terse | change | medium, vanilla | medium, terse | change |
|---|---|---|---|---|---|---|
| Words, 10 chat replies | 3,768 | 1,599 | -58% | 3,515 | 1,687 | -52% |
| Median reply | 399 words | 168 words | -58% | 375 words | 164 words | -56% |
| Thinking tokens, 10 runs | 732 | 4,847 | | 145 | 3,508 | |
| List-price cost, 10 runs | $1.60 | $1.91 | +19% | $1.56 | $1.87 | +20% |
| First person per 1k words | 3.18 | 0.0 | -100% | 2.56 | 0.0 | -100% |
| Bold lead-ins | 77 | 0 | -100% | 68 | 0 | -100% |
| Label lines | 5 | 4 | | 10 | 5 | |
| Judge violations per 1k words | 11.1 | 3.1 | -72% | 10.2 | 3.0 | -71% |

Chat words with terse were 1,649, 1,599 and 1,687 across the three runs. Effort medium lowers thinking by 28% and leaves length and violations level.

## 10-turn conversation

The conversation from [docs/benchmark.md](../benchmark.md#multi-turn-check) ran once without the plugin and once with terse 1.2.2, effort high.

| | vanilla | terse | change |
|---|---|---|---|
| Words, 10 replies | 3,622 | 1,835 | -49% |
| Median reply | 333 words | 165 words | -51% |
| Bold lead-ins | 81 | 0 | -100% |
| Label lines | 2 | 0 | -100% |
| Headers | 15 | 0 | -100% |
| First-person words | 15 | 1 | -93% |
| Judge violations | 18 | 8 | -56% |
| Judge metaphor hits | 7 | 0 | -100% |
| Thinking tokens | 19,298 | 8,608 | -55% |
| List-price cost, whole conversation | $3.54 | $2.02 | -43% |

Cost falls in the conversation because each later turn pays for the shorter earlier replies as context. 7 of the 8 violations left are bloat.

Not measured: the 40-prompt private set, subagent output, and sessions with real tool work.
