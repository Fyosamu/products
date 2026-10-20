# -*- coding: utf-8 -*-
"""Screenshot one page of a built HTML at true A4 size for close visual QA."""
import pathlib, re, subprocess, sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
here = pathlib.Path(__file__).parent
TMP = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
TMP.mkdir(parents=True, exist_ok=True)

stem = sys.argv[1] if len(sys.argv) > 1 else "resume_kit_2026"
idx = int(sys.argv[2]) if len(sys.argv) > 2 else 3   # 0-based page index

h = (here / (stem + ".html")).read_text(encoding="utf-8")
pages = re.findall(r'<section class="page.*?</section>', h, re.S)
print(f"{len(pages)} pages found; rendering #{idx}: {pages[idx][:70]!r}")

# remove all pages except the chosen one
for i, p in enumerate(pages):
    if i != idx:
        h = h.replace(p, "")
h = h.replace("page-break-after: always", "page-break-after: auto")
h = h.replace("body{", "body{")  # no-op, keeps CSS untouched

one = TMP / f"one_{stem}_{idx}_{int(__import__('time').time()*1000)}.html"
one.write_text(h, encoding="utf-8")

png = here / f"_page_{stem}_{idx}_v{int(__import__('time').time())}.png"
if png.exists():
    png.unlink()
profile = TMP / "chrome_qa_profile"
p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--disable-application-cache", "--disk-cache-size=1",
                    f"--user-data-dir={profile}",
                    "--hide-scrollbars", "--window-size=794,1123",
                    f"--screenshot={png}", one.as_uri()],
                   capture_output=True, text=True, timeout=180)
print("rc:", p.returncode, "bytes:", png.stat().st_size if png.exists() else 0)
