# -*- coding: utf-8 -*-
"""Render a clean, English-only store preview that mirrors the real Getly product page."""
import json, html, os

BASE = os.path.dirname(os.path.abspath(__file__))
sheets = json.load(open(os.path.join(BASE, "_sheets.json"), encoding="utf-8"))

PRODUCTS = [
    {
        "n": 1,
        "cover": "mockups/mock1.png",
        "price": "12.00",
        "compare": "19.00",
        "file": "Freelancer_Finance_Tracker_2026.xlsx",
        "meta": "Excel workbook &middot; 5 sheets &middot; Instant download",
        "title": "Freelancer Finance Tracker 2026 — Income, Expense &amp; Tax Dashboard",
        "blurb": "One clean dashboard for scattered income — PayPal, bank transfers, USDT. "
                 "Totals, tax reserve and take-home calculate themselves.",
        "bullets": [
            "Dashboard — income, expenses, net profit, tax reserve, take-home",
            "Income Log — client, project, fee, net received, status",
            "Expense Log — vendor, category, deductible flag",
            "Tax Reserve — annual, monthly, weekly set-aside + payment calendar",
            "Drop-downs, filters and conditional colors already set up",
        ],
        "compat": "Works in Excel 2016+ and Google Sheets. No macros, no ads.",
        "sample": "finance",
        "sample_sheet": "DASHBOARD",
    },
    {
        "n": 2,
        "cover": "mockups/mock2.png",
        "price": "9.00",
        "compare": None,
        "file": "AI_Prompt_Vault_for_Freelancers.pdf",
        "meta": "PDF eBook &middot; 13 pages &middot; 70 prompts",
        "title": "The AI Prompt Vault for Freelancers — 70 Copy-Paste Prompts",
        "blurb": "You are not being out-priced. You are being out-written. "
                 "70 fill-in-the-bracket prompts for proposals, emails, pricing and marketing.",
        "bullets": [
            "28 full prompt systems across 8 chapters",
            "Plus a 42-line quick library you can scan in a minute",
            "Winning proposals, follow-ups, proposal autopsy",
            "Client emails — delays, scope creep, payment reminders",
            "Price quotes, rate defense, retainer conversion",
        ],
        "compat": "Works with ChatGPT, Claude, Gemini or any AI tool.",
        "sample": None,
        "sample_sheet": None,
    },
    {
        "n": 3,
        "cover": "mockups/mock3.png",
        "price": "14.00",
        "compare": None,
        "file": "Ultimate_Wedding_Planner_2026.xlsx",
        "meta": "Excel workbook &middot; 6 sheets &middot; Instant download",
        "title": "The Ultimate Wedding Planner 2026 — Budget, Guests, Vendors &amp; Timeline",
        "blurb": "Everything for your 2026 wedding in one workbook — "
                 "so you can close twelve browser tabs and the group chat.",
        "bullets": [
            "Budget — targets, actual spend, \"% used\" warnings, 5% contingency",
            "Guest List — 40 guests pre-loaded, RSVP, meals, tables",
            "Vendors — compare three quotes, deposit vs balance",
            "Timeline — 27 tasks from 12 months out to the week after",
            "Seating Plan — 6 tables plus unassigned, ready to fill",
        ],
        "compat": "Works in Excel 2016+ and Google Sheets. Print-friendly.",
        "sample": "wedding",
        "sample_sheet": "BUDGET",
    },
]


def sample_table(key, name):
    if not key:
        return """
        <div class="sample">
          <div class="s-h">INSIDE THE PDF</div>
          <div class="s-body prompt">
            <p><b>2 &middot; The Mirror Proposal</b></p>
            <p>Write a proposal for [CLIENT] about [PROJECT]. Mirror back the exact
            words they used in their brief before you explain your approach.
            Open with the problem they described, not with my biography.</p>
            <p class="hint">[BRACKETS] = your context. Copy, fill, paste. 90 seconds.</p>
          </div>
        </div>"""
    sheet = next((s for s in sheets[key] if s["name"] == name), sheets[key][0])
    rows = []
    for i, r in enumerate(sheet["rows"]):
        if not any(c.strip() for c in r):
            continue
        cls = "head" if i == 0 else ""
        rows.append("<tr>" + "".join(
            f'<td class="{cls}">{html.escape(c)[:34]}</td>' for c in r) + "</tr>")
    return (f'<div class="sample"><div class="s-h">PREVIEW OF THE &ldquo;{html.escape(sheet["name"])}&rdquo; SHEET</div>'
            f'<div class="s-body"><table>{"".join(rows)}</table></div></div>')


cards = []
for p in PRODUCTS:
    li = "".join(f"<li>{b}</li>" for b in p["bullets"])
    cards.append(f"""
  <article class="p">
    <div class="p-img">
      <img src="{p['cover']}" alt="{p['n']}">
      <div class="price">{f'<s>${p["compare"]}</s>' if p['compare'] else ''}${p['price']} <span>USD</span></div>
    </div>
    <div class="p-info">
      <div class="tag">{p['meta']}</div>
      <h2>{p['title']}</h2>
      <p class="blurb">{p['blurb']}</p>
      <h3>What you get</h3>
      <ul>{li}</ul>
      <p class="compat">{p['compat']}</p>
      <div class="buy">
        <button class="btn">Buy now — ${p['price']}</button>
        <span class="auto">&rarr; Delivered automatically after payment</span>
      </div>
      <div class="file">{p['file']}</div>
    </div>
  </article>
  {sample_table(p['sample'], p['sample_sheet'])}""")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vault &amp; Sheet Studio — Store Preview</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f6f7fb;color:#1b2130;
font-family:'Segoe UI',system-ui,-apple-system,sans-serif;line-height:1.65}}
.wrap{{max-width:1040px;margin:0 auto;padding:34px 20px 70px}}
header{{background:#fff;border:1px solid #e4e7f0;border-radius:16px;
padding:24px 26px;margin-bottom:22px;box-shadow:0 2px 10px rgba(20,30,60,.05)}}
h1{{margin:0 0 4px;font-size:25px;letter-spacing:-.4px}}
h1 b{{color:#3b5bdb}}
.sub{{color:#6b7488;font-size:14.5px}}
.chips{{margin-top:12px;display:flex;gap:7px;flex-wrap:wrap}}
.chip{{background:#eef1fa;border:1px solid #dde2f0;padding:4px 11px;
border-radius:99px;font-size:12.5px;color:#4b5876}}
.p{{background:#fff;border:1px solid #e4e7f0;border-radius:16px;padding:24px;
margin-bottom:20px;box-shadow:0 2px 10px rgba(20,30,60,.05)}}
.p-img{{float:left;width:300px;margin-right:26px}}
img{{width:100%;border-radius:10px;border:1px solid #e4e7f0;display:block}}
.price{{margin-top:12px;background:#e8f8ef;border:1px solid #b9e6cd;border-radius:10px;
padding:9px;text-align:center;font-size:23px;font-weight:800;color:#12805c}}
.price s{{color:#9aa3b8;font-weight:600;font-size:16px;margin-right:6px}}
.price span{{font-size:12px;font-weight:600;color:#5c9e83}}
.tag{{display:inline-block;background:#eef1fa;color:#4b5876;border-radius:99px;
padding:4px 12px;font-size:12px;font-weight:600;margin-bottom:9px}}
h2{{margin:0 0 9px;font-size:21px;line-height:1.4}}
.blurb{{margin:0 0 14px;color:#4a5568;font-size:15px}}
h3{{margin:0 0 7px;font-size:14px;text-transform:uppercase;letter-spacing:1.1px;color:#8a93a8}}
ul{{margin:0 0 12px;padding-left:20px;font-size:14.7px}}
li{{margin-bottom:5px}}
.compat{{font-size:13.5px;color:#6b7488;background:#f6f7fb;border-radius:8px;
padding:9px 12px;margin:0 0 15px}}
.buy{{display:flex;align-items:center;gap:13px;flex-wrap:wrap;margin-bottom:12px}}
.btn{{background:#3b5bdb;color:#fff;border:0;border-radius:9px;padding:12px 26px;
font-size:15.5px;font-weight:700;cursor:pointer;box-shadow:0 3px 10px rgba(59,91,219,.3)}}
.auto{{font-size:13px;color:#12805c;font-weight:600}}
.file{{font-size:12.5px;color:#8a93a8;font-family:Consolas,monospace;
border-top:1px solid #eef0f6;padding-top:9px}}
.clear{{clear:both}}
.sample{{clear:both;background:#fff;border:1px solid #e4e7f0;border-radius:14px;
overflow:hidden;margin-top:18px}}
.s-h{{background:#f0f3fb;padding:9px 15px;font-size:12px;font-weight:700;
letter-spacing:1.1px;color:#4b5876;border-bottom:1px solid #e4e7f0}}
.s-body{{padding:14px 15px;overflow-x:auto}}
table{{border-collapse:collapse;font-size:12.6px;font-family:Consolas,monospace;width:100%}}
td{{padding:6px 10px;border-bottom:1px solid #eef0f6;color:#48536b;white-space:nowrap}}
tr:nth-child(even) td{{background:#fafbfe}}
td.head{{background:#eef1fa;color:#31406b;font-weight:700;font-family:'Segoe UI',sans-serif}}
.prompt p{{margin:0 0 9px;font-family:Consolas,monospace;font-size:13.5px;color:#3b4666}}
.prompt .hint{{color:#8a93a8;font-size:12.5px;font-style:italic}}
.note{{background:#fffbe8;border:1px solid #ffe08a;border-left:4px solid #f2c200;
border-radius:10px;padding:13px 17px;font-size:14px;color:#6b5b12;margin-bottom:20px}}
footer{{clear:both;text-align:center;color:#8a93a8;font-size:13px;margin-top:26px}}
@media(max-width:820px){{.p-img{{float:none;width:100%;margin:0 0 18px}}}}
</style></head><body><div class="wrap">

<header>
  <h1>Vault &amp; Sheet Studio</h1>
  <div class="sub">Digital spreadsheets &amp; eBooks for freelancers and organizers — delivered instantly, paid in USDT.</div>
  <div class="chips">
    <span class="chip">Instant download</span>
    <span class="chip">Excel &amp; Google Sheets</span>
    <span class="chip">No subscription</span>
    <span class="chip">Secure USDT checkout</span>
  </div>
</header>

<div class="note"><b>Store preview &mdash; what a buyer will see.</b>
Each product has its own page with a <b>Buy now</b> button. After payment the file is
released automatically &mdash; nothing for you to do per sale.</div>

{"".join(cards)}

<footer>Preview only &middot; prices and buttons will be live on your Getly store page after publishing</footer>

</div></body></html>"""

with open(os.path.join(BASE, "preview.html"), "w", encoding="utf-8") as f:
    f.write(page)
print("written", len(page))
