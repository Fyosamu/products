# -*- coding: utf-8 -*-
"""Render a contact sheet of every planner page to PNG for visual QA."""
import pathlib, subprocess

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
here = pathlib.Path(__file__).parent
TMP = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
TMP.mkdir(parents=True, exist_ok=True)

import sys as _sys
STEM = _sys.argv[1] if len(_sys.argv) > 1 else "planner_2026"
h = (here / (STEM + ".html")).read_text(encoding="utf-8")
extra = """
body{display:flex;flex-wrap:wrap;gap:6mm;padding:6mm;background:#6B7280;width:1350px;
     align-content:flex-start}
.page{zoom:.26;page-break-after:auto!important;break-inside:avoid;background:#fff;
      box-shadow:0 0 0 1px rgba(0,0,0,.35)}
.cover{background:#1F2A44}
"""
h = h.replace("</style>", extra + "</style>", 1)
out_html = TMP / ("contact_" + STEM + ".html")
out_html.write_text(h, encoding="utf-8")

png = here / ("_contact_" + STEM + ".png")
if png.exists():
    png.unlink()
p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--window-size=1400,1400",
                    f"--screenshot={png}", out_html.as_uri()],
                   capture_output=True, text=True, timeout=300)
print("rc:", p.returncode, "bytes:", png.stat().st_size if png.exists() else 0)
if p.returncode:
    print(p.stderr[-1200:])
