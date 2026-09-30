# Benchmark

Two prompt sets ran through the same runner, scorer and judge. Each prompt ran once through `claude -p`, September 2026. The public set reruns with [bench/run.py](../bench/run.py), one command per setup, see [docs/models/CONTRIBUTING.md](models/CONTRIBUTING.md).

## Public set

12 prompts in [bench/showcase_prompts.json](../bench/showcase_prompts.json): 10 engineering questions, 2 short documents. `{OUT}` in the two document prompts is the output directory the runner substituted. Run in an empty directory with no CLAUDE.md and no other plugins.

Results per model are in [docs/models](models/README.md): [Opus 5.5](models/opus-5-5.md) at effort high and medium, [Fable 5.1](models/fable-5-1.md) at effort high.

## Private set

40 prompts adapted from real sessions against a private codebase with its own CLAUDE.md: 20 analysis questions, 10 documents, 10 tasks that force a subagent. Effort high on both models. Only aggregates are published.

The baseline differs by model. The Fable 5.1 baseline, run 2026-09-22, is the setup in daily use at the time. It had a 1,886-word user CLAUDE.md holding the writing rules, a memory index, nine plugins and hooks. The Opus 5.5 baseline, run 2026-09-24, puts the same 1,886-word rules in the project CLAUDE.md and enables the same nine plugins. It has no memory index and no hooks. On Fable that arrangement wrote 9,606 chat words against the 10,094 of the setup in daily use.

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

- Every configuration kept the concrete bans: 0 dashes in 120 chat replies and 57 documents.
- Rule placement and wording move the judged categories by 15 to 50 percent. Reframes drop 50 percent and cadence 60 percent. Metaphor did not move in any configuration.
- Disabling other plugins had no style effect and saved 5.7k context tokens per call.
- Subagent dashes depend on the subagent model. Forcing Fable removed them at 28 percent higher cost per agent run. Giving Opus 5 subagents the rule text did not. Opus 5.5 subagents wrote 3 dashes in 7,735 words without the rules and 0 in 5,494 words with them.

## Multi-turn check

Both prompt sets run one prompt per fresh session. The 1.2.0 text was checked in a 10-turn conversation instead. The 10 prompts ask about this repository: a walkthrough, a review with findings, a comparison, a plan, an opinion, a redo, a status update, a PR description. They ran one after another with `claude -p --resume`, once with the 1.1.0 text and once with the reply shape plus rules 21 and 22 added. Effort high, 2026-09-30.

| | Fable 5.1, 1.1.0 | Fable 5.1, with shape and rules 21, 22 | Opus 5.5, 1.1.0 | Opus 5.5, with shape and rules 21, 22 |
|---|---|---|---|---|
| Words, 10 replies | 2,256 | 2,452 | 2,330 | 1,989 |
| Median reply | 237 | 276 | 209 | 186 |
| Bold lead-ins | 20 | 0 | 36 | 0 |
| Label lines | 10 | 4 | 8 | 0 |
| First-person words | 0 | 0 | 4 | 2 |
| ", not" sentences | 2 | 1 | 4 | 4 |
| Em or en dashes | 1 | 0 | 0 | 0 |
| Judge violations per 1k words | 6.8 | 7.1 | 7.0 | 8.6 |
| Judge metaphor hits | 6 | 7 | 3 | 6 |

The two forms the new rules name went to 0 on both models. Metaphor, cadence and bloat as the judge counts them did not move. The 6 first-person words on Opus 5.5 are self-corrections and opinion markers ("Correction to my last reply", "my pick (opinion)"). Rewriting the other rules in instruction form came after this check and has no run of its own.

The Flask prompt from the README ran 4 times on Opus 5.5 with the shipped 1.2.0 text. Word counts: 148, 176, 180 and 189. Bold lead-ins appeared in 2 of the 4 replies.

## Daily use

A scan of one user's sessions from 2026-09-04 to 2026-09-29, all Fable 5.1 final replies, grouped by how the rules reached the model. Three CLAUDE.md texts came before the plugin. Dashes were 0 in every group.

| | Style text in CLAUDE.md | Voice text in CLAUDE.md | 18 rules in CLAUDE.md | Plugin 1.0.0 | Plugin 1.1.0 |
|---|---|---|---|---|---|
| Replies | 50 | 121 | 54 | 586 | 102 |
| Median words | 307 | 223 | 159 | 138 | 150 |
| Over 150 words | 80% | 65% | 52% | 47% | 49% |
| ", not" per 1k words | 0.73 | 1.17 | 1.38 | 0.95 | 0.37 |
| Replies with a closing offer | 4% | 3% | 0% | 2% | 1% |
| First person per 1k words | 5.9 | 5.0 | 7.6 | 5.7 | 5.2 |
| Replies with first person | 80% | 70% | 61% | 51% | 31% |

Length moved with each rewrite of the text. First person per 1,000 words stayed between 5.0 and 7.6 under every text, including the two that ban it. The share of replies with any first person fell from 80% to 31%. The remaining hits are the agent describing its own next action ("I'll tell you when the compile finishes"). Single-prompt runs and the 10-turn check above produced 0 to 4 such words in 10 replies. The form appears in interactive sessions with real tool work, which no benchmark here reproduces.

## Scorer and judge

[bench/score.py](../bench/score.py) counts the checkable items: dashes, first-person words ("I", "me", "my", "let me"), banned phrases, closing offers, parentheses and words. It also counts ", not" sentences, excluding numeric corrections such as "11, not 12".

[bench/judge.py](../bench/judge.py) sends each reply to Opus 5 with a nine-item rubric and asks for quotes and a count. The items: metaphor, reframes, self-labeling, reader grading, cadence, closers, bloat, formal register, slogans. One judge call per reply. Judge cost was about $0.07 per reply at list price.

Both scripts are in [bench/](../bench).
