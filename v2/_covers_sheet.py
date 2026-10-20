# -*- coding: utf-8 -*-
"""Contact sheet of all product covers for a single visual QA pass."""
import pathlib
import subprocess

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = pathlib.Path(__file__).parent
COVERS = HERE / "covers"
TMP = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
TMP.mkdir(parents=True, exist_ok=True)

files = sorted(COVERS.glob("*.png"))
cells = "".join(
    f'<figure><img src="{f.as_uri()}"><figcaption>{f.stem}</figcaption></figure>'
    for f in files)
html = f"""<!doctype html><meta charset="utf-8">
<style>body{{background:#6B7280;margin:0;padding:14px;font-family:Segoe UI,sans-serif;
 display:grid;grid-template-columns:repeat(2,1fr);gap:14px;width:1300px}}
figure{{margin:0}} img{{width:100%;display:block;border-radius:6px;
 box-shadow:0 4px 14px rgba(0,0,0,.35)}}
figcaption{{color:#fff;font-size:15px;font-weight:700;padding:6px 2px}}</style>{cells}"""
src = TMP / "covers_sheet.html"
src.write_text(html, encoding="utf-8")

out = HERE / "_covers_sheet.png"
if out.exists():
    out.unlink()
p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--window-size=1320,4000",
                    f"--screenshot={out}", src.as_uri()],
                   capture_output=True, timeout=300)
print("rc:", p.returncode, "bytes:", out.stat().st_size if out.exists() else 0)
