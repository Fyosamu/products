# -*- coding: utf-8 -*-
"""Probe StableDeliver for a file-upload / delivery-type capability.

Goal: find out whether we can host the pack ZIP on StableDeliver itself instead of
needing a Proton Drive public link (which currently requires a working browser).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch  # noqa: E402

PATHS = [
    "/api/dashboard/upload",
    "/api/dashboard/uploads",
    "/api/dashboard/files",
    "/api/dashboard/assets",
    "/api/dashboard/products/upload",
    "/api/dashboard/storage",
    "/api/dashboard/products/new",
    "/api/dashboard/products",
    "/api/me",
    "/api/dashboard/settings",
]


def main():
    for p in PATHS:
        st, body, _, _ = fetch(p, accept="application/json", tries=1)
        if isinstance(body, dict):
            s = json.dumps(body, ensure_ascii=False)
            print("%-34s %-4s %s" % (p, st, s[:160]))
        else:
            print("%-34s %-4s (%s chars)" % (p, st, len(body) if isinstance(body, str) else "?"))


if __name__ == "__main__":
    main()
