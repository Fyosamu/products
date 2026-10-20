"""pack_all.py - validate the three prompt packs, build the mega file, print a summary.

Run:  python pack_all.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

LICENCE = (
    "Licensed to the original purchaser. Reselling or redistributing this file "
    "is not permitted."
)

PACKS = [
    ("ai-video-reels-script-prompts.txt", 150),
    ("cold-outreach-sales-prompt-prompts.txt", 120),
    ("job-search-resume-interview-prompts.txt", 120),
]

MEGA = "mega-prompt-pack-390.txt"

# Pack 2 requires four personalization slots + a hard constraint in every prompt.
S2_SLOTS = ("[COMPANY]", "[TRIGGER_EVENT]", "[PAIN]", "[PROOF]")
S2_CONSTRAINT = re.compile(
    r"(maximum \d+ words|max \d+ words|\d+ words maximum|\d+ words or fewer|"
    r"no adjectives|no exclamation marks|characters maximum|word count)",
    re.I,
)

HEADING = re.compile(r"^### (P\d{3}) — (.+)$", re.M)


def load(name: str) -> str:
    raw = (BASE / name).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"{name}: file has a UTF-8 BOM")
    text = raw.decode("utf-8")
    if "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        (BASE / name).write_bytes(text.encode("utf-8"))
        print(f"  ! normalized line endings in {name}")
    return text


def prompt_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return [(id, title, body)] for every '### Pxxx' heading."""
    matches = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((m.group(1), m.group(2), text[m.end():end]))
    return out


def validate(name: str, expected: int) -> dict:
    text = load(name)
    blocks = prompt_blocks(text)
    ids = [b[0] for b in blocks]

    assert len(blocks) == expected, (
        f"{name}: expected {expected} prompts, found {len(blocks)}"
    )
    want = [f"P{n:03d}" for n in range(1, expected + 1)]
    assert ids == want, f"{name}: numbering is not sequential 1..{expected}"

    assert text.rstrip().endswith(LICENCE), f"{name}: missing licence line at EOF"
    assert text.startswith("# "), f"{name}: missing top-level title"
    assert "## How to use" in text, f"{name}: missing How to use section"
    assert "## Fill-in variables" in text, f"{name}: missing Fill-in variables legend"

    sections = re.findall(r"^## (Section .+)$", text, re.M)
    per_section: dict[str, int] = {}
    for sec_title in sections:
        start = text.index(sec_title)
        nxt = text.find("\n## Section ", start + 1)
        chunk = text[start:nxt if nxt != -1 else len(text)]
        per_section[sec_title] = len(HEADING.findall(chunk))
    counts = set(per_section.values())
    assert len(counts) == 1, f"{name}: uneven sections: {per_section}"

    if name.startswith("cold-outreach"):
        for pid, title, body in blocks:
            missing = [s for s in S2_SLOTS if s not in body]
            assert not missing, f"{name} {pid}: missing slots {missing} ({title})"
            assert S2_CONSTRAINT.search(body), (
                f"{name} {pid}: no hard constraint found ({title})"
            )

    return {
        "file": name,
        "prompts": len(blocks),
        "bytes": len(text.encode("utf-8")),
        "sections": len(sections),
        "per_section": next(iter(counts)),
        "blocks": blocks,
        "text": text,
    }


def build_mega(results: list[dict]) -> None:
    lines = ["MEGA PROMPT PACK - 390 PROMPTS (3 VAULTS)", ""]
    lines.append("Three complete prompt packs in one file.")
    lines.append("")
    lines.append("TABLE OF CONTENTS")
    lines.append("-" * 60)
    for r in results:
        lines.append(f"{r['file']}  ({r['prompts']} prompts, {r['bytes']} bytes)")
        text = r["text"]
        for sec_title in re.findall(r"^## (Section .+)$", text, re.M):
            start = text.index(sec_title)
            nxt = text.find("\n## Section ", start + 1)
            chunk = text[start:nxt if nxt != -1 else len(text)]
            ids = HEADING.findall(chunk)
            if ids:
                lines.append(f"    {sec_title}  [{ids[0][0]}-{ids[-1][0]}]")
        lines.append("")
    lines.append(LICENCE)
    lines.append("")
    lines.append("=" * 60)
    lines.append("")

    toc = "\n".join(lines)
    body = "\n\n".join(r["text"].rstrip("\n") for r in results) + "\n"
    mega = (toc + body).replace("\r\n", "\n").replace("\r", "\n")
    (BASE / MEGA).write_bytes(mega.encode("utf-8"))


def table(results: list[dict], extra: str) -> None:
    head = ("FILE", "PROMPTS", "SECTIONS", "BYTES")
    rows = [
        (r["file"], str(r["prompts"]), str(r["sections"]), f"{r['bytes']:,}")
        for r in results
    ]
    rows.append((extra, "390", "-", f"{(BASE / MEGA).stat().st_size:,}"))
    widths = [max(len(h), *(len(row[i]) for row in rows)) for i, h in enumerate(head)]

    def fmt(row: tuple[str, ...]) -> str:
        return row[0].ljust(widths[0]) + "  " + "  ".join(
            row[i].rjust(widths[i]) for i in range(1, len(row))
        )

    print(fmt(head))
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for row in rows:
        print(fmt(row))


def main() -> int:
    results = []
    for name, expected in PACKS:
        r = validate(name, expected)
        results.append(r)
        print(
            f"OK  {name}: {r['prompts']} prompts / {r['sections']} sections "
            f"x {r['per_section']}, {r['bytes']:,} bytes, UTF-8 no BOM, LF"
        )
    build_mega(results)
    print("\nPER-PACK SUMMARY")
    table(results, MEGA)
    print(f"\nAll checks passed: {sum(r['prompts'] for r in results)} prompts total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
