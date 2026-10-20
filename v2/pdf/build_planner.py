# -*- coding: utf-8 -*-
"""Build: THE ULTIMATE PRINTABLE PLANNER 2026  ->  HTML -> PDF (Chrome headless)."""
import datetime as dt
import html
import subprocess
import pathlib

OUT = pathlib.Path(__file__).parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

NAVY = "#1F2A44"
TEAL = "#0FA3B1"
GOLD = "#F4B942"
LIGHT = "#EAF4F4"
GREY = "#8D99AE"
INK = "#2B2F38"

MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
          "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

# key dates 2026 (day, month-index0, label)
KEY_DATES = {
    (0, 0): "New Year's Day",
    (19, 0): "Martin Luther King Jr. Day",
    (2, 1): "Groundhog Day",
    (14, 1): "Valentine's Day",
    (16, 1): "Presidents' Day",
    (17, 1): "Ramadan begins*",
    (8, 2): "International Women's Day",
    (20, 2): "Eid al-Fitr*",
    (17, 2): "St. Patrick's Day",
    (20, 3): "First day of Spring",
    (3, 4): "Easter Sunday*",
    (10, 4): "Mother's Day",
    (25, 5): "Memorial Day",
    (19, 5): "Juneteenth",
    (4, 5): "Father's Day",
    (4, 6): "Independence Day",
    (7, 6): "Eid al-Adha*",
    (7, 9): "Labor Day",
    (31, 9): "Halloween",
    (11, 10): "Veterans Day",
    (26, 10): "Thanksgiving*",
    (27, 10): "Black Friday",
    (30, 11): "New Year's Eve",
}

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#fff; color:{INK};
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width:210mm; height:297mm; padding:12mm 12mm 10mm; page-break-after: always;
  position:relative; overflow:hidden; display:flex; flex-direction:column; }}
.page > * {{ flex: 0 0 auto; }}
.page:last-child {{ page-break-after: auto; }}

/* ---------- cover ---------- */
.cover {{ background:{NAVY}; color:#fff; display:flex; flex-direction:column; justify-content:space-between; padding:22mm 18mm; }}
.cover h1 {{ font-size:56px; line-height:1.02; margin:0; letter-spacing:-1.5px; font-weight:800; }}
.cover h1 span {{ color:{GOLD}; }}
.cover .kicker {{ font-size:12px; letter-spacing:5px; text-transform:uppercase; color:{TEAL}; margin-bottom:10mm; font-weight:700; }}
.cover .sub {{ font-size:16px; color:#C9D2E0; margin-top:6mm; line-height:1.6; max-width:120mm; }}
.cover .rule {{ height:3px; width:40mm; background:{GOLD}; margin:8mm 0; }}
.cover .badges {{ display:flex; gap:6mm; flex-wrap:wrap; }}
.cover .badge {{ border:1px solid rgba(255,255,255,.28); border-radius:40px; padding:3mm 6mm; font-size:11px; letter-spacing:.6px; }}
.cover .foot {{ font-size:11px; color:#7E8CA3; letter-spacing:1px; }}

/* ---------- generic page furniture ---------- */
.hdr {{ display:flex; align-items:flex-end; justify-content:space-between; border-bottom:2.5px solid {NAVY}; padding-bottom:3mm; margin-bottom:5mm; }}
.hdr h2 {{ font-size:24px; margin:0; color:{NAVY}; letter-spacing:-.4px; font-weight:800; text-transform:uppercase; }}
.hdr .tag {{ font-size:10px; letter-spacing:3px; text-transform:uppercase; color:{TEAL}; font-weight:700; }}
.subhead {{ font-size:11px; color:{GREY}; margin:-3mm 0 5mm; }}

/* ---------- year at a glance ---------- */
.yr {{ display:grid; grid-template-columns:repeat(4,1fr); gap:4mm; }}
.yr .m {{ border:1px solid #DCE3EA; border-radius:3mm; overflow:hidden; }}
.yr .m b {{ display:block; background:{NAVY}; color:#fff; font-size:9.5px; letter-spacing:2px; text-align:center; padding:1.6mm 0; }}
.yr table {{ width:100%; border-collapse:collapse; font-size:8.5px; text-align:center; }}
.yr th {{ color:{TEAL}; font-weight:700; padding:.9mm 0; font-size:7.5px; }}
.yr td {{ padding:.9mm 0; color:#4A5260; }}
.yr td.we {{ color:{GREY}; }}
.yr td.k {{ background:{GOLD}; color:{NAVY}; font-weight:700; border-radius:50%; }}

/* ---------- monthly ---------- */
.cal {{ width:100%; border-collapse:collapse; table-layout:fixed; }}
.cal th {{ background:{NAVY}; color:#fff; font-size:9.5px; letter-spacing:2px; padding:2mm 0; font-weight:700; }}
.cal td {{ border:1px solid #D8DFE7; height:24mm; vertical-align:top; padding:1.5mm 2mm; }}
.cal td .n {{ display:inline-block; background:{LIGHT}; color:{NAVY}; font-weight:700; font-size:11px;
  width:6mm; height:6mm; line-height:6mm; text-align:center; border-radius:50%; }}
.cal td.k .n {{ background:{GOLD}; }}
.cal td .d {{ display:block; font-size:7.5px; color:{TEAL}; font-weight:700; margin-top:.6mm; letter-spacing:.3px; }}
.cal td.blank {{ background:#F7F9FB; }}

.grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; margin-top:4mm; flex:1 1 auto; min-height:0; }}
.box {{ border:1px solid #D8DFE7; border-radius:2mm; padding:3mm; display:flex; flex-direction:column; }}
.box h4 {{ margin:0 0 2.5mm; font-size:9px; letter-spacing:2.2px; text-transform:uppercase; color:{TEAL}; }}
.line {{ border-bottom:1px dotted #C3CBD5; flex:1 1 auto; min-height:5.6mm; }}
.lines {{ display:flex; flex-direction:column; flex:1 1 auto; min-height:0; }}
.budwrap {{ display:flex; flex-direction:column; flex:1 1 auto; min-height:0; }}
.bud {{ display:flex; justify-content:space-between; font-size:9.5px; padding:1.6mm 0;
  border-bottom:1px dotted #C3CBD5; flex:1 1 auto; min-height:7mm; }}
.bud span:last-child {{ color:{NAVY}; font-weight:700; }}

/* ---------- weekly / daily ---------- */
.week {{ display:grid; grid-template-columns:repeat(4,1fr); gap:3mm; }}
.day {{ border:1px solid #D8DFE7; border-radius:2mm; overflow:hidden; display:flex; flex-direction:column; }}
.day .dh {{ background:{NAVY}; color:#fff; font-size:9px; letter-spacing:2.5px; padding:1.8mm 2.5mm; font-weight:700; display:flex; justify-content:space-between; }}
.day .dh em {{ font-style:normal; color:{GOLD}; }}
.slot {{ font-size:7.5px; color:{GREY}; border-bottom:1px solid #EDF1F5; padding:1.15mm 2mm; height:6.4mm; }}
.slot b {{ color:{NAVY}; font-weight:600; margin-right:2mm; display:inline-block; width:8.5mm; }}
.day.tall .slot {{ height:5.8mm; }}

.habit {{ width:100%; border-collapse:collapse; font-size:8.5px; }}
.habit th {{ background:{NAVY}; color:#fff; font-size:7.5px; padding:1.6mm 0; }}
.habit th:first-child {{ width:56mm; text-align:left; padding-left:3mm; }}
.habit td {{ border:1px solid #E3E9EF; height:6.4mm; text-align:center; color:#9AA5B4; }}
.habit td:first-child {{ text-align:left; padding-left:3mm; color:{NAVY}; font-weight:600; font-size:9px; background:#FAFCFD; }}

.check {{ width:100%; border-collapse:collapse; font-size:9px; }}
.check th {{ background:{TEAL}; color:#fff; font-size:8px; letter-spacing:1.4px; padding:2mm; }}
.check td {{ border:1px solid #E3E9EF; padding:2.2mm 2.5mm; height:8mm; }}
.check td:first-child {{ background:#FAFCFD; font-weight:600; color:{NAVY}; width:70mm; }}

.cols2 {{ display:grid; grid-template-columns:1fr 1fr; gap:6mm; }}
.cols3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; }}
.card {{ border:1px solid #D8DFE7; border-radius:2.5mm; padding:4mm; }}
.card h4 {{ margin:0 0 3mm; font-size:9.5px; letter-spacing:2.4px; text-transform:uppercase; color:{TEAL};
  border-bottom:1.5px solid {LIGHT}; padding-bottom:2mm; }}
.pill {{ display:inline-block; background:{LIGHT}; color:{NAVY}; border-radius:30px; padding:1.2mm 3.5mm;
  font-size:8.5px; font-weight:700; margin:0 1.5mm 1.5mm 0; }}
.ok {{ background:{GOLD}; }}
.note {{ background:#FFFDF6; border-left:3px solid {GOLD}; padding:3mm 4mm; font-size:9.5px; line-height:1.65; color:#5A6272; border-radius:0 2mm 2mm 0; }}
.foot {{ position:absolute; left:12mm; right:12mm; bottom:6mm; display:flex; justify-content:space-between;
  font-size:8px; color:{GREY}; letter-spacing:1.6px; text-transform:uppercase; border-top:1px solid #E6EBF0; padding-top:2mm; }}
ul.tight {{ margin:0; padding-left:5mm; font-size:10.5px; line-height:1.85; color:#4A5260; }}
ul.tight li::marker {{ color:{TEAL}; }}
"""


def esc(s):
    return html.escape(str(s))


def footer(l, r):
    return f'<div class="foot"><span>{esc(l)}</span><span>{esc(r)}</span></div>'


def month_cal(mi):
    """Calendar grid for month mi (0-based) of 2026."""
    first = dt.date(2026, mi + 1, 1)
    ndays = (dt.date(2026, mi + 2, 1) - dt.timedelta(days=1)).day if mi < 11 else 31
    start_col = first.weekday()  # 0 = Monday
    # use Sunday-first columns
    start_col = (start_col + 1) % 7
    cells = [""] * start_col
    for d in range(1, ndays + 1):
        cells.append(d)
    while len(cells) % 7:
        cells.append("")
    rows = ""
    for r in range(0, len(cells), 7):
        tds = ""
        for c in range(7):
            v = cells[r + c]
            if v == "":
                tds += '<td class="blank"></td>'
            else:
                key = KEY_DATES.get((v, mi), "")
                cls = "k" if key else ""
                dot = f'<span class="d">{esc(key)}</span>' if key else ""
                tds += f'<td class="{cls}"><span class="n">{v}</span>{dot}</td>'
        rows += f"<tr>{tds}</tr>"
    heads = "".join(f"<th>{n}</th>" for n in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"])
    return f'<table class="cal"><tr>{heads}</tr>{rows}</table>'


def mini_month(mi):
    first = dt.date(2026, mi + 1, 1)
    ndays = (dt.date(2026, mi + 2, 1) - dt.timedelta(days=1)).day if mi < 11 else 31
    start_col = (first.weekday() + 1) % 7
    cells = [""] * start_col + list(range(1, ndays + 1))
    while len(cells) % 7:
        cells.append("")
    rows = ""
    for r in range(0, len(cells), 7):
        tds = ""
        for c in range(7):
            v = cells[r + c]
            if v == "":
                tds += "<td></td>"
            else:
                k = "k" if (v, mi) in KEY_DATES else ("we" if c == 0 else "")
                tds += f'<td class="{k}">{v}</td>'
        rows += f"<tr>{tds}</tr>"
    return (f'<div class="m"><b>{MONTHS[mi][:3]}</b>'
            f'<table><tr><th>M</th><th>T</th><th>W</th><th>T</th><th>F</th><th>S</th><th>S</th></tr>'
            f"{rows}</table></div>")


def lines(n):
    return '<div class="lines">' + '<div class="line"></div>' * n + "</div>"


pages = []

# ---------------------------------------------------------------- COVER
pages.append(f"""
<section class="page cover">
  <div>
    <div class="kicker">Printable Edition &nbsp;·&nbsp; 2026</div>
    <h1>THE ULTIMATE<br>PRINTABLE<br><span>PLANNER 2026</span></h1>
    <div class="rule"></div>
    <div class="sub">365 days of planning on paper — a full year-at-a-glance, 12 monthly
    spreads, undated weekly and daily pages, goal tracking, habit grids, budgets and bill
    reminders. Print only the pages you need; the weekly and daily sheets are undated, so
    you never waste a page.</div>
  </div>
  <div>
    <div class="badges">
      <div class="badge">A4 &amp; LETTER READY</div>
      <div class="badge">36 CALENDAR PAGES</div>
      <div class="badge">UNDATED WEEKLY + DAILY</div>
      <div class="badge">PRINT AT 100% SCALE</div>
    </div>
    <div class="rule" style="margin-top:10mm"></div>
    <div class="foot">INSTANT DOWNLOAD · PERSONAL USE · NO REFUNDS ON DIGITAL FILES</div>
  </div>
</section>""")

# ---------------------------------------------------------------- HOW TO USE
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>How to use this planner</h2><div class="tag">Start here</div></div>
  <div class="cols2">
    <div class="card">
      <h4>Printing</h4>
      <ul class="tight">
        <li>Paper size <b>A4</b> (210 × 297 mm). To print on US Letter, choose "Fit to page".</li>
        <li>Scale <b>100%</b> — never "Shrink to fit", or the grid lines will not line up.</li>
        <li>Borderless is not required; every page has a built-in 12 mm safe margin.</li>
        <li>Colour mode gives the gold accents. Greyscale still reads perfectly.</li>
        <li>Paper weight: 100–120 gsm stops pens bleeding through.</li>
        <li>Print the weekly and daily pages as many times as you like — they are undated.</li>
      </ul>
    </div>
    <div class="card">
      <h4>The 5-page weekly rhythm</h4>
      <ul class="tight">
        <li><b>Sunday, 20 min:</b> fill the <i>Year at a glance</i> + this month's spread.</li>
        <li><b>Sunday, 10 min:</b> write the three priorities on the weekly page.</li>
        <li><b>Daily, 2 min:</b> morning — top 3 tasks. Evening — one gratitude line.</li>
        <li><b>Monthly review:</b> budget page, habit grid, then roll unfinished tasks forward.</li>
        <li><b>Quarterly:</b> revisit the 90-Day Goal pages. Cross off, rewrite, repeat.</li>
      </ul>
    </div>
  </div>

  <div class="note" style="margin-top:6mm">
    <b>Why the weekly and daily pages are undated:</b> most planners force you to start in
    January and waste 200 pages if you buy it in June. Here you write the date yourself, so
    a single print-out lasts as long as you do — reprint only the sheet you used.
  </div>

  <div class="cols3" style="margin-top:6mm">
    <div class="card"><h4>What's inside</h4>
      <span class="pill">Year at a glance</span><span class="pill">12 monthly spreads</span>
      <span class="pill">Undated weekly</span><span class="pill">Undated daily</span>
      <span class="pill">90-day goals</span><span class="pill">Habit grids</span>
      <span class="pill">Monthly budget</span><span class="pill">Bill tracker</span>
      <span class="pill">Meal plan</span><span class="pill">Gratitude</span>
      <span class="pill">Notes + dot grid</span>
    </div>
    <div class="card"><h4>Key dates marked</h4>
      <ul class="tight" style="font-size:9.5px">
        <li>Holidays &amp; observances are pre-dot on every monthly grid</li>
        <li>Ramadan, Eid and other lunar dates are marked * — they shift by a day each
        year, so confirm locally before you plan around them</li>
        <li>Black Friday 2026 lands on 27 November</li>
        <li>Thanksgiving 2026 lands on 26 November</li>
      </ul>
    </div>
    <div class="card"><h4>Care of your file</h4>
      <ul class="tight" style="font-size:9.5px">
        <li>You receive one PDF. Keep the original safe.</li>
        <li>Print as often as you like for <b>personal use</b>.</li>
        <li>Reselling or redistributing the file is not permitted.</li>
      </ul>
    </div>
  </div>
  {footer('The Ultimate Printable Planner 2026', '02')}
</section>""")

# ---------------------------------------------------------------- YEAR AT A GLANCE
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Year at a glance — 2026</h2><div class="tag">1 Jan → 31 Dec</div></div>
  <div class="subhead">Golden dots mark holidays and key dates. 1 January 2026 is a Thursday.</div>
  <div class="yr">{''.join(mini_month(i) for i in range(12))}</div>

  <div class="cols2" style="margin-top:6mm">
    <div class="card">
      <h4>Top 3 goals for the year</h4>
      {lines(3)}
      <h4 style="margin-top:5mm">Words for 2026</h4>
      {lines(2)}
    </div>
    <div class="card">
      <h4>Quarterly checkpoints</h4>
      <table class="check">
        <tr><th>Quarter</th><th>Date range</th><th>Did it happen?</th></tr>
        <tr><td>Q1 — plan and set up</td><td>1 Jan – 31 Mar</td><td></td></tr>
        <tr><td>Q2 — build momentum</td><td>1 Apr – 30 Jun</td><td></td></tr>
        <tr><td>Q3 — push and ship</td><td>1 Jul – 30 Sep</td><td></td></tr>
        <tr><td>Q4 — finish strong</td><td>1 Oct – 31 Dec</td><td></td></tr>
      </table>
      <div class="note" style="margin-top:4mm">Write the single thing that must be true by
      31 December before you fill anything else in. Everything else is a route to it.</div>
    </div>
  </div>
  {footer('Year at a glance', '03')}
</section>""")

# ---------------------------------------------------------------- MONTHLY x12
for mi in range(12):
    budget_rows = '<div class="budwrap">' + "".join(
        f'<div class="bud"><span>{k}</span><span>&nbsp;</span></div>'
        for k in ["Income", "Fixed costs", "Variable / lifestyle", "Savings", "Left over"]) + "</div>"
    pages.append(f"""
<section class="page">
  <div class="hdr"><h2>{MONTHS[mi]} 2026</h2><div class="tag">Monthly spread · page {mi+1} of 12</div></div>
  {month_cal(mi)}
  <div class="grid3">
    <div class="box"><h4>Three priorities</h4>{lines(4)}</div>
    <div class="box"><h4>This month's budget</h4>{budget_rows}</div>
    <div class="box"><h4>Notes &amp; birthdays</h4>{lines(4)}</div>
  </div>
  <div class="grid3">
    <div class="box"><h4>Habits &amp; routines</h4>{lines(4)}</div>
    <div class="box"><h4>Bills &amp; payments due</h4>{lines(4)}</div>
    <div class="box"><h4>Ideas, fixes &amp; small jobs</h4>{lines(4)}</div>
  </div>
  {footer(MONTHS[mi].title() + ' 2026', str(4+mi))}
</section>""")

# ---------------------------------------------------------------- 90-DAY GOALS
def goal_block(title, hint):
    return f"""
    <div class="card">
      <h4>{title}</h4>
      <div style="font-size:8.5px;color:{GREY};margin-bottom:2.5mm">{hint}</div>
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin-bottom:1mm">THE GOAL</div>
      {lines(2)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">WHY IT MATTERS</div>
      {lines(2)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">MILESTONES</div>
      {lines(4)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">FIRST STEP (2 MINUTES)</div>
      {lines(1)}
    </div>"""

pages.append(f"""
<section class="page">
  <div class="hdr"><h2>90-day goal pages</h2><div class="tag">Plan · Do · Review</div></div>
  <div class="subhead">One page per quarter. Fill it in on the first working day, then check it every Sunday.</div>
  <div class="cols3">
    {goal_block('Q1 · Jan – Mar', 'Theme of the quarter:')}
    {goal_block('Q2 · Apr – Jun', 'Theme of the quarter:')}
    {goal_block('Q3 · Jul – Sep', 'Theme of the quarter:')}
  </div>
  <div style="height:5mm"></div>
  <div class="cols3">
    {goal_block('Q4 · Oct – Dec', 'Theme of the quarter:')}
    <div class="card">
      <h4>Goal autopsy</h4>
      <div style="font-size:8.5px;color:{GREY};margin-bottom:2.5mm">Run this whenever a goal dies.</div>
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin-bottom:1mm">WHAT ACTUALLY STOPPED IT?</div>
      {lines(3)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">WHAT DID I CONTROL?</div>
      {lines(2)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">REWRITE, SMALLER</div>
      {lines(2)}
    </div>
    <div class="card">
      <h4>Quarter in one line</h4>
      {lines(3)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:4mm 0 1mm">KEEP DOING</div>
      {lines(2)}
      <div style="font-size:9px;font-weight:700;color:{NAVY};margin:3mm 0 1mm">STOP DOING</div>
      {lines(2)}
    </div>
  </div>
  {footer('90-day goals', '16')}
</section>""")

# ---------------------------------------------------------------- HABIT TRACKER
hdr = '<tr><th>HABIT</th>' + "".join(f"<th>{d}</th>" for d in range(1, 32)) + "</tr>"
habits = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
rows = "".join("<tr><td></td>" + "<td></td>" * 31 + "</tr>" for _ in habits)
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Habit tracker</h2><div class="tag">30 habits · 31 days</div></div>
  <div class="subhead">Print one of these per month. A habit counts only if the box is filled — no partial credit.</div>
  <table class="habit">{hdr}{rows}</table>
  <div class="cols3" style="margin-top:5mm">
    <div class="card"><h4>This month I will</h4>{lines(4)}</div>
    <div class="card"><h4>The one habit that matters most</h4>{lines(4)}</div>
    <div class="card"><h4>What broke the streak</h4>{lines(4)}</div>
  </div>
  {footer('Habit tracker', '17')}
</section>""")

# ---------------------------------------------------------------- WEEKLY
SLOTS = ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM",
         "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM"]


def day_box(name, tall=True, last=False):
    slots = "".join(f'<div class="slot"><b>{s}</b></div>' for s in (SLOTS if tall else SLOTS[:10]))
    return f"""<div class="day{' tall' if tall else ''}">
      <div class="dh"><span>{name}</span><em>&nbsp;</em></div>
      {slots}
      <div class="slot" style="background:{LIGHT};color:{NAVY};font-weight:700">TOP 3</div>
      <div class="slot">1.</div><div class="slot">2.</div><div class="slot">3.</div>
    </div>"""


days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Weekly planner</h2><div class="tag">Undated · print as needed</div></div>
  <div style="display:flex;gap:5mm;margin-bottom:4mm">
    <div class="box" style="flex:1"><h4>Week of</h4><div class="line"></div></div>
    <div class="box" style="flex:1"><h4>Three things that make this week a win</h4><div class="line"></div></div>
    <div class="box" style="flex:1"><h4>Not doing this week</h4><div class="line"></div></div>
  </div>
  <div class="week">
    {day_box(days[0])}{day_box(days[1])}{day_box(days[2])}{day_box(days[3])}
    {day_box(days[4])}{day_box(days[5])}{day_box(days[6])}
    <div class="day"><div class="dh"><span>WEEK REVIEW</span></div>
      <div class="slot" style="height:auto;padding:2mm">Wins</div><div class="slot" style="height:11mm"></div>
      <div class="slot" style="height:auto;padding:2mm">Drag</div><div class="slot" style="height:11mm"></div>
      <div class="slot" style="height:auto;padding:2mm">Carry over</div><div class="slot" style="height:11mm"></div>
      <div class="slot" style="height:auto;padding:2mm">Next week</div><div class="slot" style="height:11mm"></div>
    </div>
  </div>
  {footer('Weekly planner — undated', '18')}
</section>""")

# ---------------------------------------------------------------- DAILY
daily_slots = "".join(
    f'<div class="slot" style="height:7.4mm"><b>{s}</b></div>' for s in
    ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM",
     "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM"])
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Daily page</h2><div class="tag">Undated · print as needed</div></div>
  <div style="display:flex;gap:5mm;margin-bottom:4mm">
    <div class="box" style="flex:1"><h4>Date</h4><div class="line"></div></div>
    <div class="box" style="flex:1"><h4>Today's theme in five words</h4><div class="line"></div></div>
    <div class="box" style="flex:.7"><h4>Mood</h4><div class="line"></div></div>
  </div>
  <div class="cols2">
    <div class="day"><div class="dh"><span>SCHEDULE</span><em>→</em></div>{daily_slots}</div>
    <div style="display:flex;flex-direction:column;gap:4mm">
      <div class="box"><h4>Top 3 — these must happen</h4>{lines(3)}</div>
      <div class="box"><h4>Task list</h4>{lines(8)}</div>
      <div class="box"><h4>Quick capture</h4>{lines(4)}</div>
    </div>
  </div>
  <div class="cols3" style="margin-top:4mm">
    <div class="box"><h4>Water &amp; body</h4>
      <div style="font-size:9px;padding-top:1mm">Glasses &nbsp; {'◻' * 8}</div>
      <div style="font-size:9px;padding-top:1.6mm">Steps &nbsp; ____________</div>
      <div style="font-size:9px;padding-top:1.6mm">Sleep &nbsp; ______ h</div>
    </div>
    <div class="box"><h4>One thing I'm grateful for</h4>{lines(2)}</div>
    <div class="box"><h4>Tomorrow's first move</h4>{lines(2)}</div>
  </div>
  {footer('Daily page — undated', '19')}
</section>""")

# ---------------------------------------------------------------- BUDGET + BILLS
bud_cats = ["Income — main", "Income — side", "Rent / mortgage", "Utilities", "Groceries",
            "Transport", "Insurance", "Phone & internet", "Subscriptions", "Dining out",
            "Health", "Clothing", "Entertainment", "Debt payments", "Savings", "Misc"]
bud_rows = "".join(f"<tr><td>{c}</td><td></td><td></td><td></td></tr>" for c in bud_cats)
bill_names = ["Rent / mortgage", "Electricity", "Water", "Gas", "Internet", "Phone",
              "Insurance — health", "Insurance — car", "Streaming A", "Streaming B",
              "", ""]
bill_rows = "".join(
    f"<tr><td>{n}</td><td></td><td></td><td></td><td></td><td></td></tr>" for n in bill_names)

pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Monthly budget &amp; bills</h2><div class="tag">Undated · print per month</div></div>
  <div class="cols2">
    <div class="card" style="padding:0;overflow:hidden">
      <table class="check">
        <tr><th style="width:auto">CATEGORY</th><th>PLAN</th><th>ACTUAL</th><th>DIFF</th></tr>
        {bud_rows}
        <tr style="background:{LIGHT}"><td><b>TOTAL</b></td><td></td><td></td><td></td></tr>
      </table>
    </div>
    <div style="display:flex;flex-direction:column;gap:4mm">
      <div class="card" style="padding:0;overflow:hidden">
        <table class="check">
          <tr><th style="width:auto">BILL</th><th>DUE</th><th>AMOUNT</th><th>PAID</th></tr>
          {bill_rows}
        </table>
      </div>
      <div class="box"><h4>Money dates this month</h4>{lines(3)}</div>
    </div>
  </div>
  <div class="cols3" style="margin-top:5mm">
    <div class="box"><h4>Savings goals — deposits made</h4>{lines(4)}</div>
    <div class="box"><h4>Unexpected costs</h4>{lines(4)}</div>
    <div class="box"><h4>Next month's one change</h4>{lines(4)}</div>
  </div>
  <div class="note" style="margin-top:5mm">
    <b>The 20-second rule:</b> log the expense the day it happens. A budget rebuilt from
    memory a week later is fiction, and fiction is how budgets die.
  </div>
  {footer('Monthly budget & bills', '20')}
</section>""")

# ---------------------------------------------------------------- MEALS + GRATITUDE
meal_rows = "".join(
    f"<tr><td>{d}</td><td></td><td></td><td></td><td></td></tr>"
    for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Meal plan, gratitude &amp; notes</h2><div class="tag">Undated</div></div>
  <div class="card" style="padding:0;overflow:hidden">
    <table class="check">
      <tr><th style="width:26mm">DAY</th><th>BREAKFAST</th><th>LUNCH</th><th>DINNER</th><th>SNACK</th></tr>
      {meal_rows}
    </table>
  </div>
  <div class="cols3" style="margin-top:5mm">
    <div class="card"><h4>Grocery list</h4>{lines(12)}</div>
    <div class="card"><h4>Gratitude — 3 lines a day</h4>{lines(16)}</div>
    <div class="card"><h4>Brain dump</h4>{lines(16)}</div>
  </div>
  {footer('Meals · gratitude · notes', '21')}
</section>""")

# ---------------------------------------------------------------- DOT GRID
dots = "".join(
    "<div style='width:6mm;height:6mm;border-right:1px solid #E3E9EF;border-bottom:1px solid #E3E9EF'></div>"
    for _ in range(32 * 40))
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Dot grid</h2><div class="tag">Free space</div></div>
  <div style="display:flex;flex-wrap:wrap;width:192mm;height:240mm;align-content:flex-start;
       border-top:1px solid #E3E9EF;border-left:1px solid #E3E9EF">{dots}</div>
  {footer('Dot grid', '22')}
</section>""")

# ---------------------------------------------------------------- LICENSE
pages.append(f"""
<section class="page">
  <div class="hdr"><h2>Terms &amp; licence</h2><div class="tag">Please read</div></div>
  <div class="cols2">
    <div class="card">
      <h4>You may</h4>
      <ul class="tight">
        <li>Print unlimited copies for your own household and personal use.</li>
        <li>Reprint any page as often as you like — the weekly and daily sheets are undated for exactly that reason.</li>
        <li>Write on it, scribble on it, hole-punch it, take it apart.</li>
      </ul>
    </div>
    <div class="card">
      <h4>You may not</h4>
      <ul class="tight">
        <li>Resell, share, email or redistribute the PDF file.</li>
        <li>Upload the file to any cloud drive "for safekeeping" with link sharing on.</li>
        <li>Sell printed copies, or include the pages in a product you sell.</li>
        <li>Claim the design as your own.</li>
      </ul>
    </div>
  </div>
  <div class="note" style="margin-top:6mm">
    <b>Digital goods policy:</b> because this is an instant-download file, all sales are final
    and no refunds are issued. If a file will not open or a page prints wrongly, message the
    seller and it will be fixed or replaced.
  </div>
  <div class="card" style="margin-top:6mm">
    <h4>One last thing</h4>
    <ul class="tight">
      <li>The planner is only as good as the Sunday you actually sit down with it.</li>
      <li>Print week 1, fill in three priorities, and start. You can tune it after two weeks — not before.</li>
      <li>Dated calendars cover 1 January – 31 December 2026. Lunar dates marked * shift yearly.</li>
    </ul>
  </div>
  <div class="cols2" style="margin-top:6mm">
    <div class="card">
      <h4>What's in your download</h4>
      <ul class="tight">
        <li><b>One PDF file</b> — 23 pages, A4, print-ready, no software to install.</li>
        <li>Opens in any PDF reader, and on phone or tablet in any annotation app.</li>
        <li>Undated weekly, daily, habit, budget, meal and note pages — reprint freely.</li>
        <li>12 dated monthly spreads + a full 2026 year-at-a-glance.</li>
      </ul>
    </div>
    <div class="card">
      <h4>Support &amp; updates</h4>
      <ul class="tight">
        <li>Something not printing right? Message the seller — replies within 24 hours.</li>
        <li>Spotted a typo or a date that is off? Report it and get the corrected file free.</li>
        <li>Keep your original download link; updated editions are sent to the same address.</li>
        <li>Questions before buying? Ask first — no pressure, no auto-responder.</li>
      </ul>
    </div>
  </div>
  {footer('Terms & licence', '23')}
</section>""")

html_doc = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<title>The Ultimate Printable Planner 2026</title>"
            f"<style>{CSS}</style></head><body>" + "\n".join(pages) + "</body></html>")

html_path = OUT / "planner_2026.html"
pdf_path = OUT / "Ultimate_Printable_Planner_2026.pdf"
html_path.write_text(html_doc, encoding="utf-8")

subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", str(html_path)],
               check=True, capture_output=True, timeout=180)

print("pages:", len(pages))
print("html :", html_path.stat().st_size, "bytes")
print("pdf  :", pdf_path.stat().st_size, "bytes")
