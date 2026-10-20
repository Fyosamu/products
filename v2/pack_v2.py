# -*- coding: utf-8 -*-
"""Package all v2 products into buyer-ready ZIPs in products\\v2\\dist\\.

One ZIP per product. Each holds the deliverable plus a short LICENSE/README.
Nothing internal (build scripts, QA tools, listings) goes into a buyer archive.

Run:  python pack_v2.py
"""
import pathlib
import zipfile

HERE = pathlib.Path(__file__).parent
DIST = HERE / "dist"

LICENSE = """Dreamer Prompt Lab — licence for this purchase
=============================================

You bought this file, so you may:
  * use it for your own business, clients and personal projects, forever;
  * print it, copy it, edit it and fill it in as many times as you like;
  * print copies for your own team (up to 10 people).

You may not:
  * resell, re-share, upload or redistribute this file, in whole or in part;
  * include it in a bundle or free download that you publish;
  * claim the design or the text as your own work.

No refunds on digital goods once downloaded. Questions: hkay7645@gmail.com

Store: https://www.getly.store/store/dreamer-prompt-lab-muifdken
"""

PRODUCTS = [
    # (zip name, folder, [source files], root prefix inside the zip)
    ("Client_Invoice_and_Quote_Kit_2026.zip", "xlsx",
     ["Client_Invoice_and_Quote_Kit_2026.xlsx"], "Client_Invoice_and_Quote_Kit_2026"),
    ("Content_Calendar_and_Social_Media_Planner_2026.zip", "xlsx",
     ["Content_Calendar_and_Social_Media_Planner_2026.xlsx"],
     "Content_Calendar_and_Social_Media_Planner_2026"),
    ("Personal_Budget_and_Savings_Tracker_2026.zip", "xlsx",
     ["Personal_Budget_and_Savings_Tracker_2026.xlsx"],
     "Personal_Budget_and_Savings_Tracker_2026"),
    ("Client_CRM_and_Project_Tracker.zip", "xlsx",
     ["Client_CRM_and_Project_Tracker.xlsx"], "Client_CRM_and_Project_Tracker"),
    ("AI_Video_Reels_Script_Prompts_150.zip", "prompts",
     ["ai-video-reels-script-prompts.txt"], "AI-Video-Reels-Script-Prompts-150"),
    ("Cold_Outreach_Sales_Prompts_120.zip", "prompts",
     ["cold-outreach-sales-prompt-prompts.txt"], "Cold-Outreach-Sales-Prompts-120"),
    ("Job_Resume_Interview_Prompts_120.zip", "prompts",
     ["job-search-resume-interview-prompts.txt"], "Job-Resume-Interview-Prompts-120"),
    ("Complete_Prompt_Mega_Pack_390.zip", "prompts",
     ["mega-prompt-pack-390.txt"], "Complete-Prompt-Mega-Pack-390"),
    ("Ultimate_Printable_Planner_2026.zip", "pdf",
     ["Ultimate_Printable_Planner_2026.pdf"], "Ultimate-Printable-Planner-2026"),
    ("Resume_and_Cover_Letter_Kit_2026.zip", "pdf",
     ["Resume_and_Cover_Letter_Kit_2026.pdf"], "Resume-and-Cover-Letter-Kit-2026"),
]


def main() -> None:
    DIST.mkdir(exist_ok=True)
    rows = []
    for zip_name, folder, files, prefix in PRODUCTS:
        src = HERE / folder
        missing = [f for f in files if not (src / f).is_file()]
        if missing:
            raise SystemExit(f"{zip_name}: missing {missing}")
        out = DIST / zip_name
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in files:
                z.write(src / f, f"{prefix}/{f}")
            z.writestr(f"{prefix}/LICENSE.txt", LICENSE)
        kb = out.stat().st_size // 1024
        rows.append((zip_name, len(files), kb))
        print(f"{zip_name:56s} {len(files)} file  {kb:5d} KB")

    total = sum(r[2] for r in rows)
    print(f"\n{len(rows)} buyer ZIPs, {total} KB total -> {DIST}")


if __name__ == "__main__":
    main()
