"""Deterministic style scorer for one reply text.

Usage: python3 score.py < reply.txt   (prints JSON)
       or import score_text(text) -> dict

Counts the checkable items from rules/RULES.md.
The judge in judge.py covers metaphor and cadence.
"""
import json
import sys

DASHES = ("—", "–")

# self-labeling / honesty flagging / mannered stock phrases / banned words
PHRASES = [
    "to be honest", "honestly", "let me be honest", "the honest", "i will not pretend",
    "to answer directly", "earns its keep", "worth noting", "worth calling out",
    "stripped of", "under the hood", "at its core", "the key insight", "north star",
    "low-hanging", "double-edged", "elephant in the room", "keeps receipts",
    "significant", "robust", "comprehensive", "precisely", "scoped", "buildable",
    "we would welcome", "leverage", "dial worth", "a dial",
]

# closing offers and recaps
CLOSERS = [
    "let me know", "feel free", "happy to", "hope this helps", "in summary",
    "to summarize", "to recap", "want me to", "shall i", "would you like me",
    "if you'd like", "if you would like", "just say",
]


def sentences(text):
    out, cur = [], []
    for ch in text:
        cur.append(ch)
        if ch in ".!?":
            out.append("".join(cur).strip())
            cur = []
    if cur:
        out.append("".join(cur).strip())
    return [s for s in out if s]


def x_not_y(text):
    """', not <word>' inside a sentence. Excludes number corrections like '11, not 12'."""
    hits = []
    for s in sentences(text):
        low = s.lower()
        i = low.find(", not ")
        while i != -1:
            after = low[i + 6:i + 8]
            before = low[:i].rstrip().split(" ")[-1] if low[:i].strip() else ""
            if not (after[:1].isdigit() or before[:1].isdigit()):
                hits.append(s)
                break
            i = low.find(", not ", i + 6)
    return hits


def score_text(text):
    words = text.split()
    nwords = len(words)
    low = text.lower()
    phrase_hits = [p for p in PHRASES if p in low]
    closer_hits = [c for c in CLOSERS if c in low]
    sents = sentences(text)
    long_sents = [s for s in sents if len(s.split()) > 28]
    xny = x_not_y(text)
    first = sents[0] if sents else ""
    return {
        "words": nwords,
        "sentences": len(sents),
        "dashes": sum(text.count(d) for d in DASHES),
        "parens": text.count("("),
        "phrase_hits": phrase_hits,
        "closer_hits": closer_hits,
        "x_not_y": len(xny),
        "x_not_y_examples": xny[:3],
        "long_sentences": len(long_sents),
        "headers": sum(1 for l in text.splitlines() if l.startswith("#")),
        "first_sentence_words": len(first.split()),
        "first_sentence_is_question_or_meta": first.lower().startswith(("let me", "i'll", "i will", "great", "sure", "good question")),
    }


if __name__ == "__main__":
    print(json.dumps(score_text(sys.stdin.read()), indent=1, ensure_ascii=False))
