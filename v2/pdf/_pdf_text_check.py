# -*- coding: utf-8 -*-
"""Extract real text from PDF pages with pypdf and check for expected strings."""
import sys, pathlib
from pypdf import PdfReader

pdf = pathlib.Path(sys.argv[1])
needles = sys.argv[2:]
r = PdfReader(str(pdf))
print("pdf:", pdf.name, len(r.pages), "pages")
pages = [p.extract_text() or "" for p in r.pages]
for n in needles:
    hits = [i + 1 for i, t in enumerate(pages) if n.lower() in t.lower()]
    print(("  FOUND " if hits else "  MISSING ") + repr(n) +
          ("  pages=" + ",".join(map(str, hits)) if hits else ""))
if "-v" in needles:
    for i, t in enumerate(pages):
        print(f"--- page {i+1} ({len(t)} chars) ---")
        print(t[:400])
