# -*- coding: utf-8 -*-
"""Does StableDeliver host files itself (no Proton link needed)?

Dumps the new-product form HTML and looks for file inputs / upload endpoints.
"""
import html as htmllib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch  # noqa: E402


def main():
    for path in ("/dashboard/products/new", "/dashboard/products", "/dashboard/settings"):
        st, page, _, _ = fetch(path, accept="text/html", tries=2)
        if not isinstance(page, str):
            print(path, "->", st)
            continue
        print("=" * 70)
        print(path, st, len(page))
        # file inputs and upload-ish markup
        for m in re.finditer(r"<input[^>]*type=[\"']file[\"'][^>]*>", page, re.I):
            print("  FILEINPUT:", m.group(0)[:200])
        for kw in ("upload", "dropzone", "attachment", "presign", "storage", "asset"):
            hits = [m.start() for m in re.finditer(kw, page, re.I)]
            if hits:
                i = hits[0]
                snippet = htmllib.unescape(re.sub(r"\s+", " ", page[max(0, i - 120):i + 180]))
                print(f"  {kw}: {len(hits)}x -> {snippet[:260]}")
        # api paths referenced by the bundle
        apis = sorted(set(re.findall(r"/api/[a-z0-9_\-/]+", page, re.I)))
        print("  apis:", ", ".join(apis[:40]))


if __name__ == "__main__":
    main()
