# -*- coding: utf-8 -*-
"""Overflow QA: re-print the planner with .page height:auto and compare page counts."""
import pathlib, re, subprocess, sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TMP = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
TMP.mkdir(parents=True, exist_ok=True)

src = pathlib.Path(__file__).parent / "planner_2026.html"
h = src.read_text(encoding="utf-8")
extra = (".page{height:auto!important;min-height:296mm;overflow:visible!important}"
         ".foot{position:static!important;margin-top:8mm}")
assert "</style>" in h
h = h.replace("</style>", extra + "</style>", 1)
qa_html = TMP / "qa_planner.html"
qa_html.write_text(h, encoding="utf-8")

qa_pdf = TMP / "qa_planner.pdf"
if qa_pdf.exists():
    qa_pdf.unlink()
p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={qa_pdf}", qa_html.as_uri()],
                   capture_output=True, text=True, timeout=300)
print("chrome rc:", p.returncode)
if p.returncode != 0:
    print(p.stderr[-2000:]); sys.exit(1)
if not qa_pdf.exists():
    print("no output"); print(p.stderr[-2000:]); sys.exit(1)


def count_pages(path: pathlib.Path) -> int:
    b = path.read_bytes()
    # unfiltered objects carry /Type /Page  directly
    n = len(re.findall(rb"/Type\s*/Page[^s]", b))
    if n:
        return n
    m = re.findall(rb"/Count\s+(\d+)", b)
    return max(int(x) for x in m) if m else -1


src_pdf = pathlib.Path(__file__).parent / "Ultimate_Printable_Planner_2026.pdf"
a, bq = count_pages(src_pdf), count_pages(qa_pdf)
print(f"printed pdf  : {src_pdf.stat().st_size:>9} bytes, {a} pages")
print(f"overflow  pdf: {qa_pdf.stat().st_size:>9} bytes, {bq} pages")
print("OVERFLOWING PAGES:", bq - a if bq > 0 and a > 0 else "could not count")
