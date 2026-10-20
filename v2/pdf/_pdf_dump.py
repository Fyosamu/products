# -*- coding: utf-8 -*-
"""Dump sample text-showing operators from the PDF content streams."""
import re, zlib, pathlib, sys

pdf = pathlib.Path(sys.argv[1])
raw = pdf.read_bytes()
n = 0
for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
    try:
        d = zlib.decompress(m.group(1))
    except Exception:
        continue
    if b"Tj" in d or b"TJ" in d:
        n += 1
        if n <= 3:
            print(d[:700])
            print("----")
print("text streams:", n)
