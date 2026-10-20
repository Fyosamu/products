# -*- coding: utf-8 -*-
"""Render 1200x900 cover images for every v2 product.

Three mock styles:
  sheet  - spreadsheet window (xlsx products)
  card   - prompt card (txt products)
  pages  - stacked PDF pages (pdf products)

Usage:  python make_covers.py            # all
        python make_covers.py xlsx       # only products whose id starts with "xlsx_"
"""
import pathlib
import subprocess
import sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = pathlib.Path(__file__).parent
OUT = HERE / "covers"
TMP = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
OUT.mkdir(exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

NAVY = "#1F2A44"
TEAL = "#0FA3B1"
GOLD = "#F4B942"

# ---------------------------------------------------------------- data ----
PRODUCTS = [
    dict(
        id="xlsx_invoice", style="sheet", accent=TEAL,
        badge="Excel &middot; Google Sheets",
        title="Client Invoice<br>&amp; Quote <span>Kit</span> 2026",
        sub="Write the invoice, chase the money, see who owes what. "
            "Built-in crypto payment line for USDT on BNB Smart Chain.",
        feats=[("<b>Invoice</b> maker", "<b>Quote</b> maker"),
               ("<b>24-row</b> payment tracker", "<b>Client</b> ledger"),
               ("<b>Live</b> dashboard", "<b>Auto</b> overdue alerts")],
        price="Instant download",
        tabs=["INVOICE MAKER", "QUOTE MAKER", "PAYMENT TRACKER", "LEDGER"],
        kpi=[("$41,820", "Invoiced"), ("$36,140", "Collected"), ("$5,680", "Outstanding")],
        head=["Invoice #", "Client", "Amount", "Due", "Status"],
        rows=[["INV-2026-014", "Nova Studio", "$2,400.00", "12-Sep", ("ok", "Paid")],
              ["INV-2026-015", "Binance Blog", "$900.00", "18-Sep", ("ok", "Paid")],
              ["INV-2026-016", "Acme SaaS", "$3,150.00", "02-Sep", ("bad", "Overdue")],
              ["INV-2026-017", "Loop Agency", "$1,275.00", "29-Sep", ("pend", "Sent")],
              ["INV-2026-018", "Orbit CRM", "$4,800.00", "07-Oct", ("pend", "Sent")],
              ["INV-2026-019", "CoinDesk", "$650.00", "14-Oct", ("ok", "Paid")]],
        bar="DASHBOARD — updates itself",
    ),
    dict(
        id="xlsx_calendar", style="sheet", accent=TEAL,
        badge="Excel &middot; Google Sheets",
        title="Content Calendar<br>&amp; Social <span>Planner</span> 2026",
        sub="365 dated days, 22 marked key dates and 40 ready-to-copy posts — "
            "one workbook instead of twelve browser tabs.",
        feats=[("<b>365-day</b> 2026 calendar", "<b>40-post</b> content calendar"),
               ("<b>Hashtag</b> bank", "<b>Ideas</b> backlog"),
               ("<b>Analytics</b> W1–W52", "<b>Reach</b> dashboard")],
        price="Instant download",
        tabs=["YEAR 2026", "CONTENT CALENDAR", "POST TRACKER", "ANALYTICS"],
        kpi=[("40", "Posts planned"), ("1.2M", "Reach tracked"), ("6.4%", "Avg engagement")],
        head=["Date", "Platform", "Pillar", "Format", "Status"],
        rows=[["02-Jan", "Instagram", "Reels", "Short video", ("ok", "Posted")],
              ["09-Jan", "TikTok", "Tips", "Trend", ("ok", "Posted")],
              ["16-Jan", "YouTube", "Tutorial", "Long-form", ("pend", "Draft")],
              ["23-Jan", "X / Twitter", "Thread", "Text", ("pend", "Planned")],
              ["30-Jan", "LinkedIn", "Authority", "Carousel", ("bad", "Idea")],
              ["06-Feb", "Instagram", "Reels", "Short video", ("pend", "Planned")]],
        bar="CONTENT CALENDAR — every post in one view",
    ),
    dict(
        id="xlsx_budget", style="sheet", accent=TEAL,
        badge="Excel &middot; Google Sheets",
        title="Personal Budget<br>&amp; Savings <span>Tracker</span> 2026",
        sub="Plan the month, log every expense, hit the goals. "
            "50/30/20 scoring, debt snowball and net worth included.",
        feats=[("<b>14</b> budget categories", "<b>50/30/20</b> scorecard"),
               ("<b>Savings</b> goals", "<b>Debt</b> snowball"),
               ("<b>Net worth</b> tracker", "<b>Health</b> dashboard")],
        price="Instant download",
        tabs=["DASHBOARD", "MONTHLY BUDGET", "EXPENSE LOG", "GOALS"],
        kpi=[("$5,400", "Income"), ("$3,712", "Spent"), ("$1,688", "Saved")],
        head=["Category", "Planned", "Actual", "Variance", "% Used"],
        rows=[["Rent", "$1,400.00", "$1,400.00", "$0.00", ("ok", "100%")],
              ["Groceries", "$450.00", "$388.20", "+$61.80", ("ok", "86%")],
              ["Transport", "$180.00", "$212.40", "-$32.40", ("bad", "118%")],
              ["Eating out", "$220.00", "$164.90", "+$55.10", ("ok", "75%")],
              ["Subscriptions", "$65.00", "$79.97", "-$14.97", ("bad", "123%")],
              ["Savings", "$900.00", "$900.00", "$0.00", ("ok", "100%")]],
        bar="MONTHLY BUDGET — red when you overspend",
    ),
    dict(
        id="xlsx_crm", style="sheet", accent=TEAL,
        badge="Excel &middot; Google Sheets",
        title="Client CRM<br>&amp; Project <span>Tracker</span>",
        sub="Leads, projects, hours and deliverables in one place — "
            "with a dashboard that tells you what is late today.",
        feats=[("<b>25-lead</b> pipeline", "<b>Profit</b> per project"),
               ("<b>Timesheet</b> built in", "<b>Deliverables</b> tracker"),
               ("<b>Follow-up</b> alerts", "<b>Win-rate</b> dashboard")],
        price="Instant download",
        tabs=["PIPELINE", "PROJECTS", "TIMESHEET", "DASHBOARD"],
        kpi=[("$186,400", "Pipeline"), ("34%", "Win rate"), ("7", "Active projects")],
        head=["Lead", "Stage", "Value", "Weighted", "Next step"],
        rows=[["Nova Studio", "Proposal", "$12,000", "$7,200", ("pend", "14-Oct")],
              ["Acme SaaS", "Qualified", "$8,500", "$3,400", ("ok", "11-Oct")],
              ["Loop Agency", "Negotiation", "$22,000", "$15,400", ("ok", "08-Oct")],
              ["Orbit CRM", "Won", "$18,600", "$18,600", ("ok", "Kickoff")],
              ["Halberd Ltd", "New", "$4,200", "$840", ("bad", "Overdue")],
              ["CoinDesk", "Lost", "$6,000", "$0", ("bad", "—")]],
        bar="PIPELINE — weighted value by stage",
    ),
    dict(
        id="prompts_video", style="card", accent="#7C5CFF",
        badge="150 Prompts &middot; TXT",
        title="AI Video, Reels<br>&amp; YouTube <span>Scripts</span>",
        sub="Hooks, shot lists, faceless narration, titles, B-roll and "
            "retention edits — every prompt locks a shootable output format.",
        feats=[("<b>10</b> sections", "<b>3-second</b> hooks"),
               ("<b>Shot lists</b> included", "<b>Faceless</b> narration"),
               ("<b>Title + thumbnail</b> pairs", "<b>Rewrite</b> punch-up")],
        price="Copy · Fill · Paste",
        card_head="SECTION 1 — HOOK FORMULAS",
        card_body=('Write 15 three-second hooks for a video about [TOPIC] aimed at '
                   '[AUDIENCE].<br><br>Hook types: bold claim, curiosity gap, mistake, '
                   'contrarian take, result-first.<br><br><b>Output format:</b> '
                   'numbered list, max 14 words each, spoken-word phrasing, no hashtags.'),
        card_hint="[BRACKETS] = your context. Works in ChatGPT, Claude and Gemini.",
        bar="150 PROMPTS — every one has an output format",
    ),
    dict(
        id="prompts_outreach", style="card", accent="#7C5CFF",
        badge="120 Prompts &middot; TXT",
        title="Cold Outreach<br>&amp; Sales <span>Prompt Vault</span>",
        sub="First touches, follow-ups, LinkedIn DMs, cold calls, proposals "
            "and dead-lead revival — short enough that a human answers.",
        feats=[("<b>8</b> sections", "<b>4</b> personalisation slots"),
               ("<b>Hard</b> constraint line", "<b>Objection</b> handling"),
               ("<b>Price</b> negotiation", "<b>Deal</b> autopsy")],
        price="Copy · Fill · Paste",
        card_head="SECTION 1 — COLD EMAIL FIRST TOUCH",
        card_body=('Write a 90-word cold email to [NAME] at [COMPANY] referencing '
                   '[TRIGGER_EVENT]. Lead with the [PAIN] they described, prove it with '
                   '[PROOF], ask for 15 minutes.<br><br><b>Hard constraint:</b> one idea, '
                   'no adjectives, subject line under 6 words.'),
        card_hint="Fill [COMPANY] [TRIGGER_EVENT] [PAIN] [PROOF] with checkable detail.",
        bar="120 PROMPTS — email, LinkedIn, call, proposal, pricing",
    ),
    dict(
        id="prompts_job", style="card", accent="#7C5CFF",
        badge="120 Prompts &middot; TXT",
        title="Job Search, Resume<br>&amp; Interview <span>Vault</span>",
        sub="ATS-proof bullets, resume tailoring, cover letters, recruiter DMs, "
            "STAR answers and offer negotiation — in one ordered workflow.",
        feats=[("<b>8</b> sections", "<b>XYZ</b> formula bullets"),
               ("<b>ATS</b> tailoring", "<b>STAR</b> answers (20)"),
               ("<b>Story</b> bank", "<b>Salary</b> negotiation")],
        price="Copy · Fill · Paste",
        card_head="SECTION 1 — RESUME BULLETS THAT PASS ATS",
        card_body=('Turn these duties into achievement bullets using the XYZ formula: '
                   '"Accomplished [X] as measured by [Y] by doing [Z]".<br><br>'
                   '[SOURCE: your current resume + 3 real results]<br><br>'
                   '<b>Output format:</b> 8 bullets, max 32 words, first-person implied, '
                   'no pronouns, metric in every line.'),
        card_hint="Never let a prompt invent employers, dates or numbers — paste your truth.",
        bar="120 PROMPTS — resume, LinkedIn, interview, offer",
    ),
    dict(
        id="prompts_mega", style="card", accent="#7C5CFF",
        badge="390 Prompts &middot; Bundle",
        title="The Complete<br>Prompt <span>Mega Pack</span> — 390",
        sub="All three vaults in one file: video scripts, cold outreach and "
            "job search. The bundle costs less than buying them apart.",
        feats=[("<b>150</b> video prompts", "<b>120</b> outreach prompts"),
               ("<b>120</b> job-search prompts", "<b>10</b> structured sections"),
               ("<b>Single</b> TXT file", "<b>Bonus</b> how-to guide")],
        price="Copy · Fill · Paste",
        card_head="WHAT IS INSIDE",
        card_body=('<b>1 · AI Video, Reels &amp; YouTube Scripts (150)</b> — hooks, shot '
                   'lists, faceless narration, titles, retention edits.<br><br>'
                   '<b>2 · Cold Outreach &amp; Sales (120)</b> — first touches, follow-ups, '
                   'LinkedIn, cold calls, pricing, deal autopsies.<br><br>'
                   '<b>3 · Job Search, Resume &amp; Interview (120)</b> — ATS bullets, '
                   'tailoring, cover letters, STAR answers, negotiation.'),
        card_hint="Every prompt keeps its [BRACKETS] and its locked output format.",
        bar="390 PROMPTS — three vaults, one file",
    ),
    dict(
        id="pdf_planner", style="pages", accent=GOLD,
        badge="PDF &middot; 23 Pages",
        title="The Ultimate<br>Printable <span>Planner</span> 2026",
        sub="Twelve months, goals, habits, budget, meals and undated pages — "
            "print only what you use. A4 and US Letter friendly.",
        feats=[("<b>12</b> monthly spreads", "<b>3 x</b> 90-day goals"),
               ("<b>30-habit</b> tracker", "<b>Weekly + daily</b> pages"),
               ("<b>Budget</b> &amp; meal plan", "<b>Dot grid</b> free space")],
        price="Print at home — unlimited",
        pages_head="JANUARY 2026",
        pages_body="Monthly spread &middot; page 1 of 12",
        pages_grid=True,
        bar="23 PAGES — print only the ones you need",
    ),
    dict(
        id="pdf_resume", style="pages", accent=GOLD,
        badge="PDF &middot; 17 Pages",
        title="Resume &amp; Cover<br>Letter <span>Kit</span> 2026",
        sub="Six recruiter-ready resume layouts, three cover letters and the "
            "banks that fill them — ATS-checked and fully editable.",
        feats=[("<b>6</b> resume layouts", "<b>3</b> cover letters"),
               ("<b>ATS</b> checklist", "<b>Bullet</b> + power-verb banks"),
               ("<b>LinkedIn</b> rewrite", "<b>Interview</b> answers")],
        price="Print at home — unlimited",
        pages_head="LAYOUT 1 — COMPACT SINGLE-COLUMN",
        pages_body="Jordan A. Mercer &middot; Marketing Assistant",
        pages_grid=False,
        bar="17 PAGES — layouts, letters, banks, checklists",
    ),
]

# --------------------------------------------------------------- html -----
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
/* Author at 1200x750 (16:10), then scale x1.6 into a 1920x1200 stage so the
   screenshot lands on Getly's recommended product-card size without cropping. */
body{font-family:'Segoe UI',Helvetica,Arial,sans-serif;width:1920px;height:1200px;overflow:hidden;
 background:#1F2A44}
.stage{width:1920px;height:1200px;overflow:hidden}
.canvas{width:1200px;height:750px;position:relative;display:flex;color:#fff;
 transform:scale(1.6);transform-origin:0 0}
.badge{display:inline-block;color:#fff;font-size:14px;font-weight:700;letter-spacing:3px;
 padding:9px 20px;border-radius:30px;text-transform:uppercase}
h1{font-size:50px;line-height:1.08;margin-top:30px;font-weight:800;letter-spacing:-1.4px;
 max-width:505px}
h1 span{color:var(--acc)}
.sub{font-size:19.5px;color:#B8C4D9;margin-top:22px;line-height:1.5;max-width:470px;font-weight:300}
.feats{margin-top:36px;display:grid;grid-template-columns:1fr 1fr;gap:13px 18px;max-width:478px}
.feat{background:rgba(255,255,255,.09);border-left:4px solid var(--acc);padding:13px 15px;
 font-size:15.5px;border-radius:0 8px 8px 0}
.feat b{color:var(--acc)}
.price{position:absolute;bottom:60px;left:70px;background:var(--acc);color:#1F2A44;
 font-size:24px;font-weight:800;padding:15px 32px;border-radius:50px}

/* sheet mock */
.sheet{position:absolute;right:36px;top:96px;width:560px;background:#fff;border-radius:14px;
 box-shadow:0 40px 80px rgba(0,0,0,.45);overflow:hidden;transform:rotate(-3deg);color:#2B2D42}
.tabs{background:#1F2A44;padding:12px 16px;display:flex;gap:8px}
.tab{font-size:11.5px;padding:6px 12px;border-radius:6px 6px 0 0;background:#33415f;color:#9fb0cc}
.tab.on{background:#fff;color:#1F2A44;font-weight:700}
.kpi{display:flex;gap:10px;padding:16px}
.kpi div{flex:1;background:#EAF4F4;border-radius:8px;padding:12px;text-align:center}
.kpi .n{font-size:21px;font-weight:800;color:#0FA3B1}
.kpi .l{font-size:9.5px;color:#8D99AE;text-transform:uppercase;letter-spacing:.6px;margin-top:3px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:#0FA3B1;color:#fff;padding:9px 8px;text-align:left;font-size:11.5px}
td{padding:8px;border-bottom:1px solid #eef2f6}
tr:nth-child(even) td{background:#F7FAFC}
.ok{color:#1E7E34;font-weight:700}.pend{color:#997404;font-weight:700}.bad{color:#B02A37;font-weight:700}
.bar{height:64px;background:#0FA3B1;display:flex;align-items:center;justify-content:space-between;
 padding:0 18px;color:#fff;font-weight:700;font-size:13.5px}

/* prompt card mock */
.card{position:absolute;right:40px;top:104px;width:530px;background:#fff;border-radius:14px;
 box-shadow:0 40px 80px rgba(0,0,0,.45);overflow:hidden;transform:rotate(2.5deg);color:#2B2D42}
.c-head{background:#7C5CFF;color:#fff;padding:15px 20px;font-size:13px;font-weight:700;
 letter-spacing:2.2px}
.c-body{padding:22px 22px 18px;font-family:Consolas,'Courier New',monospace;font-size:14.5px;
 line-height:1.62;color:#3b4666}
.c-body b{color:#7C5CFF}
.c-hint{background:#F5F3FF;border-top:1px dashed #c9c0ff;padding:13px 20px;font-size:12.5px;
 color:#6b649a;font-style:italic}
.bar.card-bar{background:#7C5CFF}

/* stacked pages mock */
.stack{position:absolute;right:56px;top:84px;width:520px;height:560px}
.pgsheet{position:absolute;background:#fff;border-radius:6px;box-shadow:0 26px 60px rgba(0,0,0,.45);
 color:#1F2A44;overflow:hidden}
.pgsheet.back1{right:0;top:0;width:400px;height:520px;transform:rotate(7deg);opacity:.9}
.pgsheet.back2{right:34px;top:26px;width:400px;height:520px;transform:rotate(3deg)}
.pgsheet.front{right:70px;top:56px;width:400px;height:520px}
.pg-h{background:#1F2A44;color:#fff;padding:13px 16px;font-size:12.5px;font-weight:700;
 letter-spacing:1.6px}
.pg-h span{float:right;color:#F4B942;font-weight:600;letter-spacing:0}
.pg-sub{padding:9px 16px 0;font-size:11.5px;color:#8D99AE;letter-spacing:.5px}
.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;padding:12px 16px}
.gcell{background:#EAF4F4;border-radius:3px;height:34px;font-size:9.5px;color:#5b6a86;
 padding:3px 4px;font-weight:600}
.gcell.hd{background:#0FA3B1;color:#fff;text-align:center;height:auto;padding:4px 0}
.gcell.gold{background:#FDF0D5;color:#9a6b00}
.lines{padding:10px 16px}
.ln{height:9px;background:#EEF2F7;border-radius:4px;margin-bottom:8px}
.ln.w70{width:70%}.ln.w90{width:90%}.ln.w50{width:50%}.ln.acc{background:#F4B942;width:38%}
.pg-foot{position:absolute;bottom:0;left:0;right:0;background:#F7FAFC;border-top:1px solid #e6ebf2;
 padding:8px 16px;font-size:10.5px;color:#8D99AE;display:flex;justify-content:space-between}
.bar.gold-bar{background:#F4B942;color:#1F2A44}
"""


def build(p):
    left = f"""
  <div style="position:relative; z-index:2; padding:56px 0 0 70px;">
    <div class="badge" style="background:{p['accent']}">{p['badge']}</div>
    <h1>{p['title']}</h1>
    <div class="sub">{p['sub']}</div>
    <div class="feats">{''.join(f'<div class="feat">{a}</div><div class="feat">{b}</div>' for a, b in p['feats'])}</div>
    <div class="price">{p['price']}</div>
  </div>"""

    if p["style"] == "sheet":
        tabs = "".join(f'<div class="tab{" on" if i == 0 else ""}">{t}</div>'
                       for i, t in enumerate(p["tabs"]))
        kpi = "".join(f'<div><div class="n">{n}</div><div class="l">{l}</div></div>'
                      for n, l in p["kpi"])
        head = "".join(f"<th>{h}</th>" for h in p["head"])
        body = "".join(
            "<tr>" + "".join(
                f'<td class="{c[0]}">{c[1]}</td>' if isinstance(c, tuple) else f"<td>{c}</td>"
                for c in r) + "</tr>" for r in p["rows"])
        right = (f'<div class="sheet"><div class="tabs">{tabs}</div>'
                 f'<div class="kpi">{kpi}</div>'
                 f"<table><tr>{head}</tr>{body}</table>"
                 f'<div class="bar"><span>{p["bar"]}</span><span>2026</span></div></div>')
        bar_cls = ""
    elif p["style"] == "card":
        right = (f'<div class="card"><div class="c-head">{p["card_head"]}</div>'
                 f'<div class="c-body">{p["card_body"]}</div>'
                 f'<div class="c-hint">{p["card_hint"]}</div>'
                 f'<div class="bar card-bar"><span>{p["bar"]}</span><span>2026</span></div></div>')
        bar_cls = ""
    else:
        if p.get("pages_grid"):
            days = "".join(
                f'<div class="gcell{" hd" if i < 7 else ""}'
                f'{" gold" if i % 9 == 0 and i >= 7 else ""}">'
                f'{["SUN","MON","TUE","WED","THU","FRI","SAT"][i] if i < 7 else i - 6}</div>'
                for i in range(35))
            inner = f'<div class="grid">{days}</div>'
        else:
            inner = ('<div class="lines">'
                     '<div class="ln acc"></div><div class="ln w90"></div><div class="ln w70"></div>'
                     '<div class="ln w90"></div><div class="ln w50"></div><div class="ln w70"></div>'
                     '<div class="ln w90"></div><div class="ln w70"></div><div class="ln w50"></div>'
                     '<div class="ln w90"></div><div class="ln w70"></div><div class="ln w90"></div>'
                     "</div>")
        right = (f'<div class="stack">'
                 f'<div class="pgsheet back1"></div><div class="pgsheet back2"></div>'
                 f'<div class="pgsheet front"><div class="pg-h">{p["pages_head"]}'
                 f'<span>2026</span></div>'
                 f'<div class="pg-sub">{p["pages_body"]}</div>{inner}'
                 f'<div class="pg-foot"><span>Dreamer Prompt Lab</span><span>Page 4 / 23</span></div>'
                 f"</div></div>")
        bar_cls = " gold-bar"

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>
:root{{--acc:{p['accent']}}}
{CSS}
</style></head><body><div class="stage"><div class="canvas" style="background:
 linear-gradient(135deg,#1F2A44 0%,#28355a 55%,{'#3a2f00' if p['accent'] == GOLD else '#0b1f33'} 160%)">
{left}
{right}
</div></div></body></html>"""


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    made = []
    for p in PRODUCTS:
        if only and not p["id"].startswith(only):
            continue
        src = TMP / (p["id"] + "_cover.html")
        src.write_text(build(p), encoding="utf-8")
        out = OUT / (p["id"] + ".png")
        if out.exists():
            out.unlink()
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--window-size=1920,1200",
                        f"--screenshot={out}", src.as_uri()],
                       capture_output=True, timeout=300)
        size = out.stat().st_size if out.exists() else 0
        print(f"{p['id']:20s} {size:>8} bytes")
        made.append((p["id"], size))
    bad = [i for i, s in made if s < 20000]
    if bad:
        raise SystemExit("FAILED: " + ", ".join(bad))
    print("covers:", len(made), "->", OUT)


if __name__ == "__main__":
    main()
