"""Re-download the v2 product files from Getly's public R2 storage.

The local copies were destroyed by an unrelated workspace cleanup on 27 Sep 2026.
Getly still hosts every uploaded file, so the seller API (/api/products/<slug>)
gives back the public URLs. This script pulls them into products/v2/dist and
products/v2/covers under their original filenames and verifies the byte sizes.
"""
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(BASE, "dist")
COVERS = os.path.join(BASE, "covers")

ITEMS = [
    # (zip url, zip filename, cover url, cover filename, expected zip bytes)
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/gDu1kltp0Pp0QfIAAomwQ.zip",
     "Client_Invoice_and_Quote_Kit_2026.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/EqDZgsCLxDOmXtTZGU-1d.png",
     "xlsx_invoice.png", 17635),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/Hee5IJW9IEb8io7Z7Mc7l.zip",
     "Content_Calendar_and_Social_Media_Planner_2026.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/IfcH7YiqJBQl2WSqzDw62.png",
     "xlsx_calendar.png", 38817),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/Rqj7UnGbuXc_nq6Z9s0RG.zip",
     "Personal_Budget_and_Savings_Tracker_2026.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/kxEuG_XmQKi7ESFDz2Wav.png",
     "xlsx_budget.png", 24313),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/zvFOoi4Egnye1dhCZwRXH.zip",
     "Client_CRM_and_Project_Tracker.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/n3vcgpL6kWDc07aCh0aBi.png",
     "xlsx_crm.png", 24425),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/uAUWIU56EJLGs-ZPSLPFq.zip",
     "AI_Video_Reels_Script_Prompts_150.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/d_D62OfdR89MI8I5Id18F.png",
     "prompts_video.png", 31004),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/Y7U86lYBv29-qkz4W3MJM.zip",
     "Cold_Outreach_Sales_Prompts_120.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/v3qNIsYN63jsn8DTt9381.png",
     "prompts_outreach.png", 22660),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/gPRyrt6CYx8RZq7t5oFrZ.zip",
     "Job_Resume_Interview_Prompts_120.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/rtwwWZEk-a2QbAPTeZr24.png",
     "prompts_job.png", 25217),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/ToZ6-v3jgTIfjR6IVdP9m.zip",
     "Complete_Prompt_Mega_Pack_390.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/jErrR9O0LJToQ3aTymsWy.png",
     "prompts_mega.png", 76041),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/f00SFQZWpya3GHq8iPtrJ.zip",
     "Ultimate_Printable_Planner_2026.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/Wx6bGJ-OfJdp-br3VpSHX.png",
     "pdf_planner.png", 535731),
    ("https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/files/f76edbb9-ced8-4f42-8a82-400a1e39b73f/Ldd4_UhYJJESxNXH0TRi5.zip",
     "Resume_and_Cover_Letter_Kit_2026.zip",
     "https://pub-94bac7ffddcd49979b3fd722ae492e58.r2.dev/images/f76edbb9-ced8-4f42-8a82-400a1e39b73f/6QhPUJdpPnbbVKx1Qo7Iy.png",
     "pdf_resume.png", 279316),
]


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest, "wb") as fh:
        fh.write(data)
    return len(data)


def main():
    os.makedirs(DIST, exist_ok=True)
    os.makedirs(COVERS, exist_ok=True)
    failures = []
    for zip_url, zip_name, img_url, img_name, expected in ITEMS:
        for url, dest, kind in (
            (zip_url, os.path.join(DIST, zip_name), "zip"),
            (img_url, os.path.join(COVERS, img_name), "cover"),
        ):
            try:
                size = fetch(url, dest)
                if kind == "zip":
                    ok = size == expected
                    if not ok:
                        failures.append(f"{zip_name}: {size} != {expected}")
                    print(f"{'OK ' if ok else 'BAD'} {kind:5} {zip_name:52} {size:>9,} bytes")
                else:
                    with open(dest, "rb") as fh:
                        head = fh.read(8)
                    ok = head.startswith(b"\x89PNG")
                    if not ok:
                        failures.append(f"{img_name}: not a PNG")
                    print(f"{'OK ' if ok else 'BAD'} {kind:5} {img_name:52} {size:>9,} bytes")
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{dest}: {exc}")
                print(f"ERR  {kind:5} {os.path.basename(dest):52} {exc}")
    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        return 1
    print("All 20 files recovered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
