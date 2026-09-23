# terse

A Claude Code plugin that cuts reply length in half and removes mannered prose. **46% fewer words, 51% lower cost, [measured](docs/benchmark.md).** The writing rules apply to replies, documents, commits and subagents. A context meter for the status line comes with it.

Terms used in the numbers below:

- **Vanilla**: Claude Code with no CLAUDE.md, no plugins and no custom instructions.
- **Style violation**: a sentence that breaks one of the rules. An Opus 5 judge counts them by reading each reply against the rule list. Counts are per 1,000 words, so long and short replies compare.
- **Metaphor**: figurative wording where a literal phrase exists. "A 3,000-line merge gets a skim and a prayer" instead of "a 3,000-line merge gets a 10-minute read and no line-by-line review".
- **"X, not Y" reframe**: a contrast used as a label instead of an explanation. "This is intent, not behavior" instead of "the docstring says X, the code does Y".
- **Slogan**: a short line that sounds like a principle and states no mechanism. "The decision is the feature."
- **Cadence**: rhythm built for effect, such as triads and punchline endings.
- **Bloat**: sentences that add no fact, including narration like "I'll look at the code now".
- **Output tokens**: what the model wrote. Output tokens are priced about five times higher than input tokens on Opus and Fable.

Measured on 12 public prompts, vanilla Claude Code against terse. Fable 5.1, effort high, one run each.

| | vanilla | terse | change |
|---|---|---|---|
| Words, 10 chat replies | 4,610 | 2,125 | -54% |
| Median reply | 500 words | 196 words | -61% |
| Output tokens, 12 runs | 13,453 | 7,661 | -43% |
| Style violations per 1k words (Opus judge) | 18.4 | 7.1 | -61% |
| "X, not Y" reframes per 1k | 1.95 | 0.0 | -100% |
| Slogans per 1k | 1.52 | 0.0 | -100% |
| Metaphor per 1k | 7.16 | 3.29 | -54% |

Method, prompts and the judge rubric: [docs/benchmark.md](docs/benchmark.md).

## Install

```
/plugin marketplace add lowenbjer/claude-terse
/plugin install terse@terse
```

The writing rules apply to every new session, after `/clear`, and to an existing session you exit and resume with `claude --resume`.

For the context meter, run `/terse:install-meter` once. It adds one `statusLine` entry to your `~/.claude/settings.json` and takes effect on save.

## What you get

**The rules.** 18 rules and 10 before/after pairs, 487 words. First sentence is the answer you are looking for. One idea per sentence. No em dashes, no slogans, no "X, not Y" framing, no self-labeling, no closing offers, no narration of what is about to happen. Chat replies capped at 150 words unless you ask for a document or a walkthrough. Full text: [rules/RULES.md](rules/RULES.md).

**Delivery.** The rules ship as an output style. It applies while the plugin is enabled and sits in the main agent's system prompt. Subagents run their own system prompt, so a `SubagentStart` hook hands them the same text. No hook rewrites or blocks anything.

**The meter.** Model name and context fill as a percentage. Green below 37%, yellow from 37%, orange from 49%, skull from 60%. The thresholds are set below the usual 50, 65 and 80 percent. Three studies show retrieval quality dropping well before a large window fills:

- Chroma's [Context Rot](https://www.trychroma.com/research/context-rot) report: 18 models, degradation from 50k tokens on a 200k window.
- [NoLiMa](https://arxiv.org/abs/2502.05167): 11 of 13 models at half their baseline by 32k tokens.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172): content in the middle of a long context gets less attention than the start and end.

The thresholds are the three numbers near the top of [statusline/context-meter.js](statusline/context-meter.js).

## Before and after

Prompt, run once with each setup: "We have a Flask API with a Postgres database. Requests time out under load once a day around 09:00. Where would you look first and why?"

**Vanilla, 427 words:**

> Start with the Postgres connection pool and what is scheduled at 09:00. A failure that recurs at the same clock time every day is almost never a code bug in the request path. It is a periodic external event colliding with your morning traffic peak.
>
> First things to check, in order:
>
> - **Scheduled jobs at or just before 09:00.** Look at cron, Celery beat, Kubernetes CronJobs, and any BI or reporting tool that runs a morning extract. A heavy report query, a nightly ETL running late, or a backup or VACUUM that overlaps with the traffic ramp will hold locks and saturate I/O. Cross-check the database logs and the job scheduler for anything landing in the 08:45 to 09:15 window.
>
> - **Connection pool exhaustion.** Flask with gunicorn or uwsgi typically runs many workers, each holding its own SQLAlchemy pool. At the 09:00 login spike the total connections can exceed Postgres max_connections, or the pool can hit its pool_size plus max_overflow and requests block on checkout until pool_timeout. That looks exactly like a request timeout. Check `pg_stat_activity` at 09:00 for connection counts and for sessions stuck in `idle in transaction` or waiting on locks.
>
> - **Lock contention.** Query `pg_locks` joined to `pg_stat_activity` during the incident. One long transaction from a batch job blocking a hot table will stall every web request that touches it. Enable log_lock_waits so the database records blocked queries for you.
>
> - **Cache expiry or cold state.** If a cache layer or materialized view refreshes on a daily schedule, 09:00 traffic may be hitting an empty cache and stampeding the database. Check TTLs and refresh schedules.
>
> - **Autovacuum and checkpoints.** Less likely to be clock-aligned, but check whether the traffic burst triggers a checkpoint spike or an autovacuum on a large table at the same time.
>
> Why the pool and the scheduler come first: they explain both halves of the symptom. The scheduler explains the time of day. The pool explains why the failure mode is a timeout rather than an error, since blocked connection checkouts fail silently and slowly.
>
> To confirm quickly, capture `pg_stat_activity`, `pg_locks`, and gunicorn worker status every minute from 08:50 to 09:20 tomorrow. Enable log_min_duration_statement at around one second and log_lock_waits so tomorrow's incident produces evidence. Compare the slow queries against what is normal at 14:00. Whatever differs is your culprit.
>
> If none of those show anything, then look at infrastructure: a shared database host with another tenant's morning job, a load balancer health check change, or an autoscaler that scales the app tier faster than the database can accept connections.

**terse, 196 words:**

> Cron and scheduled jobs first. A daily 09:00 timeout points to a clock-driven event, and the two usual sources are a batch job that holds Postgres locks or saturates the connection pool, and the morning login surge.
>
> Check in this order:
>
> 1. **Postgres activity at 09:00.** Query `pg_stat_activity` for long-running or `idle in transaction` sessions, and `pg_locks` for waiters. A nightly VACUUM, backup, report or ETL job that overruns into 09:00 explains lock waits and I/O saturation.
> 2. **Connection pool.** Compare Flask worker count times pool size against `max_connections`. If a batch job consumes 20 connections, the API queues on pool checkout and times out.
> 3. **Traffic and worker saturation.** Plot request rate and gunicorn/uwsgi busy workers at 08:55 to 09:15. If workers max out with normal DB latency, the fix is more workers or async I/O.
> 4. **Slow query log.** Enable `log_min_duration_statement` at 500 ms for one morning. Slow queries at 09:00 with fast ones at 10:00 confirm contention.
> 5. **Autovacuum and checkpoints.** Check `pg_stat_bgwriter` for checkpoint spikes and `pg_stat_user_tables` for autovacuum runs near 09:00.
>
> Correlate one thing: the `crontab -l`, systemd timers and any scheduler (Celery beat, Airflow) for entries between 08:00 and 09:00.

Both replies name the same causes. The vanilla one adds "fail silently and slowly", "Whatever differs is your culprit", and a closing paragraph on what to do if nothing shows. The terse one gives the queries to run and the numbers to compare.

## Measured limits

- **Measured with Fable 5.1 as the main agent only.** Opus 5 and Sonnet 5 ran only as subagents. With the rules in context, Opus kept 13 em dashes per 1k words and Sonnet put a dash in 1 reply of 5. No numbers exist for either as the main model.
- **Metaphor drops by half.** 7.2 to 3.3 per 1k words on the public set. No rule text tested moved it further.
- **The 150-word cap shortens replies without enforcing the limit.** Replies got 46 to 54 percent shorter across two prompt sets. Long analysis questions still run over.
- **Subagent output changed with the subagent model and did not change with the rules.** Explore-type subagents run Opus and kept 13 em dashes per 1k words with the rules in their context. Fable subagents produced 0.1 per 1k without any rules. To control it, set `CLAUDE_CODE_SUBAGENT_MODEL` to your main model, or ask for general-purpose subagents, which inherit it.
- **Cost.** Output tokens fell 43 to 54 percent. Context tokens are most of the cost per call. Total cost fell 9 percent on the short public set. It fell 51 percent on a 40-prompt benchmark against a real codebase with a large CLAUDE.md.

## Uninstall

```
/plugin uninstall terse@terse
```

Remove the `statusLine` entry from `~/.claude/settings.json` if you installed the meter.

## License

MIT.
