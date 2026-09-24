# terse

A Claude Code plugin that cuts reply length in half and removes mannered prose. **Fable 5.1: 46% fewer words, 51% lower cost. Opus 5.5: 51% fewer words, 36% lower cost. [Measured](docs/benchmark.md) on 20 prompts against a real codebase.** The writing rules apply to replies, documents, commits and subagents. A context meter for the status line comes with it.

Terms used in the numbers below:

- **Vanilla**: Claude Code with no CLAUDE.md, no plugins and no custom instructions.
- **Style violation**: a sentence that breaks one of the rules. An Opus 5 judge counts them by reading each reply against the rule list. Counts are per 1,000 words, so long and short replies compare.
- **Metaphor**: figurative wording where a literal phrase exists. "A 3,000-line merge gets a skim and a prayer" instead of "a 3,000-line merge gets a 10-minute read and no line-by-line review".
- **"X, not Y" reframe**: a contrast used as a label instead of an explanation. "This is intent, not behavior" instead of "the docstring says X, the code does Y".
- **Slogan**: a short line that sounds like a principle and states no mechanism. "The decision is the feature."
- **Cadence**: rhythm built for effect, such as triads and punchline endings.
- **Bloat**: sentences that add no fact, including narration like "I'll look at the code now".
- **Output tokens**: what the model wrote. Output tokens are priced about five times higher than input tokens on Opus and Fable.

Measured on 12 public prompts, vanilla Claude Code against terse. Opus 5.5, effort high, one run each.

| | vanilla | terse | change |
|---|---|---|---|
| Words, 10 chat replies | 5,959 | 1,876 | -69% |
| Median reply | 636 words | 177 words | -72% |
| Output tokens, 12 runs | 19,310 | 8,596 | -55% |
| Style violations per 1k words (Opus judge) | 11.1 | 2.7 | -76% |
| "X, not Y" reframes per 1k | 0.84 | 0.0 | -100% |
| Slogans per 1k | 1.17 | 0.0 | -100% |
| Metaphor per 1k | 3.69 | 1.07 | -71% |

Tables for Fable 5.1, and for Opus 5.5 at effort medium: [docs/models](docs/models/README.md). Method, prompts and the judge rubric: [docs/benchmark.md](docs/benchmark.md).

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

Prompt, run once with each setup on Opus 5.5: "We have a Flask API with a Postgres database. Requests time out under load once a day around 09:00. Where would you look first and why?"

**Vanilla, 636 words:**

> # Where I'd look first for the 09:00 timeouts
>
> The 09:00 timing is the most useful clue. Before looking at any code, find out which of these two things is happening:
>
> 1. **Traffic goes up at 09:00.** The start of the workday brings logins, dashboards and syncs. That's a capacity problem.
> 2. **Traffic stays flat but something else runs at 09:00.** That's contention from a scheduled job.
>
> Compare your request-rate graph at 09:00 with other hours. That one check tells you which half of the problem you're in.
>
> ## 1. Check what runs at 09:00
>
> Look at crontabs, `pg_cron`, Celery beat, Kubernetes CronJobs, backups (`pg_dump`), ETL and report jobs, and `REFRESH MATERIALIZED VIEW`. Also check for cache entries that all expire at the same moment, because that sends every request to the database at once.
>
> Be careful with timezones. 09:00 local might be 07:00 UTC in the scheduler config, so grep for both.
>
> Common problems:
> - A `REFRESH MATERIALIZED VIEW` without `CONCURRENTLY`, a bulk `UPDATE`, or a migration. Each of these takes locks that API queries then wait behind.
> - A backup or batch job using up disk I/O.
>
> ## 2. Capture what Postgres is doing during the window
>
> This gives you the fastest real answer. Snapshot `pg_stat_activity` every 10–15 seconds from 08:55 to 09:15:
>
> ```sql
> SELECT now(), state, wait_event_type, wait_event,
>        now() - xact_start AS xact_age, left(query, 120) AS query, application_name
> FROM pg_stat_activity
> WHERE datname = current_database()
> ORDER BY xact_start NULLS LAST;
> ```
>
> Read the results like this:
> - **Lots of `wait_event_type = 'Lock'`:** something is holding locks. Join with `pg_locks` (or use `pg_blocking_pids()`) to find the blocking session. It's usually the scheduled job from step 1.
> - **Lots of `idle in transaction`:** the app opens transactions and doesn't close them quickly. That holds connections and locks.
> - **Many `active` sessions running the same query:** one query is slow at scale, often a missing index or a stale plan. Check `pg_stat_statements` for that window.
> - **Session count close to `max_connections`:** you're running out of connections (see step 3).
>
> Also set `log_min_duration_statement` (e.g. 500ms) and `log_lock_waits = on` so the next occurrence leaves a record.
>
> ## 3. Check for app-side connection pool exhaustion
>
> This is the most common cause of timeouts in Flask + SQLAlchemy apps. Search the app logs around 09:00 for:
>
> ```
> QueuePool limit of size 5 overflow 10 reached, connection timed out
> ```
>
> Then do the arithmetic: gunicorn workers × threads × (`pool_size` + `max_overflow`) × number of instances, compared with Postgres `max_connections`. When traffic jumps, requests queue for a pooled connection until they time out. Postgres can look almost idle while this happens.
>
> Also check for sessions that aren't returned to the pool. The usual causes are a missing `db.session.remove()` or teardown handler, or slow external HTTP calls made inside a transaction.
>
> ## 4. Find out which timeout is firing
>
> The load balancer (often 60s), gunicorn `--timeout` (30s by default) and SQLAlchemy `pool_timeout` (30s by default) each point to a different place:
> - Gunicorn `WORKER TIMEOUT` messages mean the workers are blocked. They're either waiting on the database or there are too few sync workers.
> - A 504 from the load balancer with no gunicorn error means requests are queuing before they reach a worker.
>
> ## My recommendation
>
> Run the `pg_stat_activity` snapshot loop at tomorrow's 09:00. At the same time, grep the app logs for the pool error and list every scheduled job near 09:00. That will very likely narrow it to one of two causes: a job holding locks, or pool exhaustion under the morning traffic. The fix is very different for each: move or rewrite the job, or resize the pool and add a connection pooler such as PgBouncer.
>
> If you share the scheduler config, the SQLAlchemy engine settings and the gunicorn command, I can check the connection arithmetic for you.

**terse, 158 words:**

> I would look first at `pg_stat_activity` during the 08:55 to 09:15 window. A fixed daily time usually means a scheduled job or a login surge, and that view separates the two:
>
> - **Scheduled jobs:** Check cron, pg_cron, Celery beat and backup schedules for anything set to 09:00. Common culprits are `pg_dump`, `REFRESH MATERIALIZED VIEW`, a manual `VACUUM` and ETL or report queries. These hold locks or saturate disk IO. In `pg_stat_activity`, look for rows with `wait_event_type = 'Lock'` or `'IO'`.
> - **Connection pool exhaustion:** SQLAlchemy defaults to `pool_size=5`, `max_overflow=10` and `pool_timeout=30`. A morning spike queues requests for 30 seconds, then they fail. Compare gunicorn workers × pool size against Postgres `max_connections` (default 100).
> - **Cache stampede:** Keys with a 24-hour TTL, set at 09:00 once, all expire together each day. Every request then hits Postgres at the same moment.
> - **Slow queries:** Enable `pg_stat_statements` and set `log_min_duration_statement = 500ms`. This names the queries that slow down at 09:00.

Both replies name scheduled jobs, pool exhaustion and cache expiry. The vanilla one adds four headers, a recommendation section that repeats steps 1 to 3, and an offer to check the config. The terse one gives the pool defaults, the connection arithmetic and the two settings to enable.

## Measured limits

- **Measured with Opus 5.5 and Fable 5.1 as the main agent.** Opus 5 and Sonnet 5 ran only as subagents. With the rules in context, Opus 5 kept 13 em dashes per 1k words and Sonnet put a dash in 1 reply of 5. No numbers exist for either as the main model. Per-model tables: [docs/models](docs/models/README.md).
- **Metaphor drops by two thirds on Opus 5.5 and by half on Fable 5.1.** 3.7 to 1.1 per 1k words on Opus 5.5, 7.2 to 3.3 on Fable 5.1. No rule text tested moved it further.
- **The 150-word cap shortens replies without enforcing the limit.** Chat words fell 46 to 69 percent across two prompt sets and two models. Long analysis questions still run over.
- **Subagent output changed with the subagent model and did not change with the rules.** In a Fable 5.1 session, Explore-type subagents ran Opus 5 and kept 13 em dashes per 1k words with the rules in their context. Fable subagents produced 0.1 per 1k without any rules. In an Opus 5.5 session, the subagents ran Opus 5.5 and wrote 0.4 per 1k without the rules and 0 with them. To control it, set `CLAUDE_CODE_SUBAGENT_MODEL` to your main model, or ask for general-purpose subagents, which inherit it.
- **Cost.** Output tokens fell 42 to 55 percent. Context tokens are most of the cost per call. Total cost fell 9 to 12 percent on the short public set. On 20 chat prompts against a real codebase with a large CLAUDE.md it fell 51 percent on Fable 5.1 and 36 percent on Opus 5.5.

## Uninstall

```
/plugin uninstall terse@terse
```

Remove the `statusLine` entry from `~/.claude/settings.json` if you installed the meter.

## License

MIT.
