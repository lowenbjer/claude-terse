"""Opus judge for pattern-level rules the scorer cannot count.

Usage: python3 judge.py <text-file> [repeats]   -> prints JSON
Runs claude -p with no setting sources.
"""
import json
import subprocess
import sys

RUBRIC = """You grade one piece of text against a writing standard. Return JSON only.

The standard bans:
1. Mannered prose: metaphor or flourish where a literal phrase exists ("a dial worth turning", "earns its keep", "keeps receipts", "north star").
2. Contrastive reframes "X, not Y" used as a label instead of stating the mechanism ("intent-stating, not behavior"). A numeric correction ("11, not 12") is allowed.
3. Self-labeling and honesty flags ("to be honest", "let me be direct", "the honest answer", "I will not pretend").
4. Reader grading ("good question", "your instinct is right", "thoughtful list").
5. Crafted cadence: triads built for rhythm, punchline endings, trailing fragments, reduplication.
6. Closing offers and recaps ("let me know if", "happy to", "in summary").
7. Bloat: sentences that add no fact, hedge paragraphs, restating the question, narrating what you are about to do.
8. Formal-polite register ("we would welcome", "precisely so").
9. Slogans: short declarative taglines that sound like a principle but state no mechanism ("The decision is the feature.", "Built to audit, not to trust.", "Context is a nicety."). Includes docstrings, comments and headings.

Return this JSON and nothing else:
{"mannered": [quotes], "reframes": [quotes], "self_label": [quotes], "grading": [quotes], "cadence": [quotes], "closers": [quotes], "bloat": [quotes], "formal": [quotes], "slogans": [quotes], "total_violations": <int>, "words_removable_pct": <0-100 estimate of words that could go with no fact lost>}

Quote at most 12 words per item. Be strict about 1, 2, 7 and 9. Do not invent items.

TEXT START
"""


def judge(text, repeats=1):
    outs = []
    for _ in range(repeats):
        prompt = RUBRIC + text[:12000] + "\nTEXT END"
        r = subprocess.run(["claude", "-p", prompt, "--output-format", "json", "--setting-sources", "",
                            "--model", "claude-opus-5", "--no-session-persistence", "--max-turns", "1"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
        try:
            res = json.loads(r.stdout)
            body = res.get("result", "")
            start, end = body.find("{"), body.rfind("}")
            parsed = json.loads(body[start:end + 1])
            parsed["_cost"] = res.get("total_cost_usd")
            outs.append(parsed)
        except Exception as e:
            outs.append({"_error": str(e), "_raw": r.stdout[:300]})
    return outs


if __name__ == "__main__":
    text = open(sys.argv[1], errors="ignore").read()
    reps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    print(json.dumps(judge(text, reps), indent=1, ensure_ascii=False))
