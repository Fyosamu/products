"""Content sanity check: first 3 and last 1 prompt of each pack."""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
FILES = [
    "ai-video-reels-script-prompts.txt",
    "cold-outreach-sales-prompt-prompts.txt",
    "job-search-resume-interview-prompts.txt",
]
HEADING = re.compile(r"^### (P\d{3}) — (.+)$", re.M)


def blocks(text: str):
    ms = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[m.end():end]
        fence = body.find("```", body.find("```") + 3)  # closing fence
        if fence != -1:
            body = body[:fence + 3]
        out.append((m.group(1), m.group(2), body.strip()))
    return out


for name in FILES:
    text = (BASE / name).read_text(encoding="utf-8")
    bs = blocks(text)
    picks = [("FIRST", b) for b in bs[:3]] + [("LAST", bs[-1])]
    print("=" * 78)
    print(f"{name}  ({len(bs)} prompts)")
    print("=" * 78)
    for label, (pid, title, body) in picks:
        print(f"\n[{label}] ### {pid} - {title}\n{body}\n")
