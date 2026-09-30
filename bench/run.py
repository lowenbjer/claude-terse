"""Run the 12 public prompts through Claude Code and score the replies.

Usage:
  python3 bench/run.py <model> <label> [--vanilla] [--effort <level>] [--judge]

  <model>     model id, for example claude-opus-5-5
  <label>     name of the output folder under bench/out/
  --vanilla   disable the terse plugin for the run (settings override)
  --effort    effort level passed to claude, default high
  --judge     also run judge.py on each chat reply (about $0.07 per reply)
  --ids       comma-separated prompt ids to run, for example s01,s12

Each prompt runs once in a fresh empty directory with `claude -p`, so no
CLAUDE.md and no project settings apply. Results land in bench/out/<label>/:
one .json and one .txt per prompt, summary.json, and row.md with a table row
for docs/models/. The plugin must be installed as terse@terse for the
non-vanilla run. Cost: about $1 per run at list price on Opus 5.5.
"""
import json
import os
import statistics
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from score import score_text  # noqa: E402


def run_prompt(prompt, model, effort, settings_path, out_dir):
    workdir = tempfile.mkdtemp(prefix="terse-bench-")
    before = set(os.listdir(out_dir))
    text = prompt.replace("{OUT}", out_dir)
    cmd = ["claude", "-p", "--output-format", "json", "--model", model, "--effort", effort]
    if settings_path:
        cmd += ["--settings", settings_path]
    cmd.append(text)
    res = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=900)
    new_files = [f for f in os.listdir(out_dir) if f not in before and f.endswith(".md")]
    doc_words = sum(len(open(os.path.join(out_dir, f), errors="ignore").read().split()) for f in new_files)
    try:
        out = json.loads(res.stdout)
    except json.JSONDecodeError:
        out = {"result": "", "error": res.stderr[-500:], "total_cost_usd": 0, "usage": {}}
    out["_doc_words"] = doc_words
    return out


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    model, label = args[0], args[1]
    vanilla = "--vanilla" in args
    judge_on = "--judge" in args
    effort = args[args.index("--effort") + 1] if "--effort" in args else "high"
    out_dir = os.path.join(HERE, "out", label)
    os.makedirs(out_dir, exist_ok=True)
    settings_path = None
    if vanilla:
        settings_path = os.path.join(out_dir, "settings-vanilla.json")
        with open(settings_path, "w") as f:
            json.dump({"enabledPlugins": {"terse@terse": False}}, f)
    prompts = json.load(open(os.path.join(HERE, "showcase_prompts.json")))
    if "--ids" in args:
        wanted = args[args.index("--ids") + 1].split(",")
        prompts = [p for p in prompts if p["id"] in wanted]
    rows = []
    for p in prompts:
        res = run_prompt(p["prompt"], model, effort, settings_path, out_dir)
        text = str(res.get("result") or "")
        usage = res.get("usage") or {}
        models = list((res.get("modelUsage") or {}).keys())
        row = {
            "id": p["id"], "kind": p["kind"], "words": len(text.split()), "doc_words": res.get("_doc_words", 0),
            "cost": res.get("total_cost_usd") or 0,
            "output_tokens": usage.get("output_tokens", 0),
            "model_reported": models,
            "score": score_text(text),
        }
        if judge_on and p["kind"] == "chat" and text:
            from judge import judge
            row["judge"] = judge(text)[0]
        rows.append(row)
        with open(os.path.join(out_dir, p["id"] + ".json"), "w") as f:
            json.dump({"prompt": p, "response": res, "row": row}, f, indent=1)
        with open(os.path.join(out_dir, p["id"] + ".txt"), "w") as f:
            f.write(text)
        print(p["id"], p["kind"], row["words"], "words", row["doc_words"], "doc words", "$%.3f" % row["cost"], models, flush=True)
    chat = [r for r in rows if r["kind"] == "chat"]
    summary = {
        "model": model, "label": label, "vanilla": vanilla, "effort": effort,
        "chat_words": sum(r["words"] for r in chat),
        "median_chat_words": statistics.median(r["words"] for r in chat) if chat else 0,
        "doc_words": sum(r["doc_words"] for r in rows if r["kind"] == "doc"),
        "output_tokens": sum(r["output_tokens"] for r in rows),
        "cost": round(sum(r["cost"] for r in rows), 3),
        "dashes": sum(r["score"]["dashes"] for r in rows),
        "first_person": sum(r["score"]["first_person"] for r in rows),
        "x_not_y": sum(r["score"]["x_not_y"] for r in rows),
        "bold_lead_ins": sum(r["score"]["bold_lead_ins"] for r in rows),
        "label_lines": sum(r["score"]["label_lines"] for r in rows),
        "models_reported": sorted({m for r in rows for m in r["model_reported"]}),
    }
    if judge_on:
        judged = [r for r in chat if "judge" in r and "total_violations" in r["judge"]]
        words = sum(r["words"] for r in judged) or 1
        summary["judge_violations_per_1k"] = round(sum(r["judge"]["total_violations"] for r in judged) / words * 1000, 1)
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    row_md = "| %s | %s | %s | %d | %d | %d | $%.2f | %d | %d | %d | %d |" % (
        model, "vanilla" if vanilla else "terse", effort, summary["chat_words"],
        summary["median_chat_words"], summary["output_tokens"], summary["cost"],
        summary["dashes"], summary["first_person"], summary["bold_lead_ins"], summary["label_lines"])
    with open(os.path.join(out_dir, "row.md"), "w") as f:
        f.write("| model | setup | effort | chat words | median | output tokens | cost | dashes | first person | bold lead-ins | label lines |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n" + row_md + "\n")
    print(json.dumps(summary, indent=1))
    print(row_md)


if __name__ == "__main__":
    main()
