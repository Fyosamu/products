# -*- coding: utf-8 -*-
"""Build: Content Calendar & Social Media Planner 2026 (XLSX)"""
import os, random
from datetime import date, timedelta

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule

# ----------------------------------------------------------------- STYLE
NAVY = "1F2A44"
TEAL = "0FA3B1"
LIGHT = "EAF4F4"
GOLD = "F4B942"
WHITE = "FFFFFF"
GREY = "8D99AE"
BAND = "F7FAFC"

FONT = "Calibri"
thin = Side(style="thin", color="D5DDE5")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

MONEY = "$#,##0.00"
DATEF = "dd-mmm-yyyy"
PCT = "0.0%"

TODAY = date(2026, 9, 27)
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def hdr(ws, row, headers, start=1, fill=NAVY):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start + i, value=h)
        c.font = Font(name=FONT, bold=True, color=WHITE, size=11)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border
    ws.row_dimensions[row].height = 24


def band(ws, row, c1, c2, text, fill=NAVY, color=WHITE, size=11):
    for c in range(c1, c2 + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.border = border
        cell.alignment = Alignment(horizontal="center", vertical="center")
    c = ws.cell(row=row, column=c1, value=text)
    c.font = Font(name=FONT, bold=True, color=color, size=size)


def box(ws, r1, r2, c1, c2, money=(), dates=(), pct=(), ints=(), zebra=True):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = border
            if c in money:
                cell.number_format = MONEY
            elif c in dates:
                cell.number_format = DATEF
            elif c in pct:
                cell.number_format = PCT
            elif c in ints:
                cell.number_format = "#,##0"
            if zebra and (r - r1) % 2 == 1 and cell.fill.patternType is None:
                cell.fill = PatternFill("solid", fgColor=BAND)


def widths(ws, spec):
    for k, v in spec.items():
        ws.column_dimensions[k].width = v


def sheet(wb, name):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    return ws


def start_here(ws, title, tagline, lines):
    widths(ws, {"A": 3, "B": 100})
    ws["B2"] = title
    ws["B2"].font = Font(name=FONT, bold=True, size=20, color=NAVY)
    ws["B3"] = tagline
    ws["B3"].font = Font(name=FONT, size=12, color=TEAL, italic=True)
    r = 5
    for line in lines:
        c = ws.cell(row=r, column=2, value=line)
        if line.isupper() and len(line) > 3:
            c.font = Font(name=FONT, bold=True, size=12, color=TEAL)
        else:
            c.font = Font(name=FONT, size=11, color="2B2D42")
        r += 1


def kpi(ws, row, col, label, formula, fmt="#,##0"):
    lab = ws.cell(row=row, column=col, value=label)
    lab.font = Font(name=FONT, bold=True, size=10, color=WHITE)
    lab.fill = PatternFill("solid", fgColor=NAVY)
    lab.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    lab.border = border
    val = ws.cell(row=row + 1, column=col, value=formula)
    val.font = Font(name=FONT, bold=True, size=18, color=TEAL)
    val.fill = PatternFill("solid", fgColor=LIGHT)
    val.alignment = Alignment(horizontal="center", vertical="center")
    val.border = border
    val.number_format = fmt
    ws.row_dimensions[row].height = 28
    ws.row_dimensions[row + 1].height = 30


def dv_list(ws, options, rng, error="Pick a value from the list"):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    dv.error = error
    ws.add_data_validation(dv)
    dv.add(rng)
    return dv


def status_cf(ws, rng, rules):
    for op, fill, fc, bold in rules:
        ws.conditional_formatting.add(
            rng,
            CellIsRule(operator="equal", formula=[f'"{op}"'],
                       fill=PatternFill("solid", fgColor=fill),
                       font=Font(name=FONT, color=fc, bold=bold)))


# ----------------------------------------------------------------- WORKBOOK
wb = openpyxl.Workbook()

# ================================================================= START HERE
ins = wb.active
ins.title = "Start Here"
ins.sheet_view.showGridLines = False
start_here(
    ins,
    "CONTENT CALENDAR & SOCIAL MEDIA PLANNER 2026",
    "Year at a glance  ·  Content calendar  ·  Post tracker  ·  Hashtags  ·  Analytics",
    [
        "",
        "HOW TO USE THIS WORKBOOK (5 minutes to set up)",
        "",
        "1. Open YEAR 2026 - every date of the year with the weekday already worked out for you.",
        "   Key dates (Super Bowl, Ramadan, Black Friday, Christmas...) are marked in the notes column.",
        "2. Plan in CONTENT CALENDAR: Date, Platform, Pillar, Format, Hook, CTA - then a Status.",
        "3. When a post goes live, change Status to Published and fill Likes / Comments / Shares / Reach.",
        "4. Keep the numbers you care about in POST TRACKER - engagement rate calculates itself.",
        "5. Park raw ideas in IDEAS BACKLOG and reusable tag sets in HASHTAG BANK.",
        "6. ANALYTICS takes one minute a week (W1 to W52) and feeds the DASHBOARD automatically.",
        "",
        "RULES THAT KEEP IT CLEAN",
        "",
        "- Never delete rows - set Status to Repurposed or Archived instead.",
        "- Use the drop-down lists (Platform, Pillar, Format, Status) so the dashboard counts work.",
        "- Dates use dd-mmm-yyyy, e.g. 14-Feb-2026. Weekdays in YEAR 2026 are already correct.",
        "- Enter Reach as a plain number: type 12500 not 12,500.",
        "- Only published posts get metric numbers - leave Likes / Reach blank until it is live.",
        "- The DASHBOARD reads TODAY(), so open it fresh before your planning session.",
        "",
        "THE 4-PILLAR RULE",
        "",
        "1. Educate (how-to, tips), Entertain (trends, humour), Inspire (stories, results),",
        "   Promote (offers, launches), Behind the scenes (people, process).",
        "2. Aim for at least one post per pillar per week - the pillar column makes this visible.",
        "3. Batch filming on one day, write captions on another, schedule a week ahead.",
    ],
)

# ================================================================= YEAR 2026
yr = sheet(wb, "YEAR 2026")
y_headers = ["Date", "Week no", "Month", "Day", "Weekday", "Seasonality / key dates"]
y_widths = [14, 10, 13, 8, 13, 52]
for i, (h, w) in enumerate(zip(y_headers, y_widths), start=1):
    yr.cell(row=1, column=i, value=h)
    yr.column_dimensions[get_column_letter(i)].width = w
hdr(yr, 1, y_headers)

key_dates = {
    date(2026, 1, 1): "New Year's Day",
    date(2026, 1, 19): "Martin Luther King Jr. Day (US holiday)",
    date(2026, 2, 8): "Super Bowl LX - biggest ad night of the year",
    date(2026, 2, 14): "Valentine's Day",
    date(2026, 2, 16): "Presidents' Day (US holiday)",
    date(2026, 2, 18): "Ramadan 2026 begins (approx.)",
    date(2026, 3, 8): "International Women's Day",
    date(2026, 3, 14): "Pi Day / weekend content hook",
    date(2026, 3, 20): "Eid al-Fitr (approx. end of Ramadan)",
    date(2026, 4, 5): "Easter Sunday",
    date(2026, 5, 10): "Mother's Day (US)",
    date(2026, 5, 25): "Memorial Day (US) - summer push starts",
    date(2026, 5, 27): "Eid al-Adha (approx.)",
    date(2026, 6, 21): "Father's Day (US)",
    date(2026, 7, 4): "Independence Day (US)",
    date(2026, 9, 7): "Labor Day (US) - back to routine content",
    date(2026, 10, 31): "Halloween",
    date(2026, 11, 26): "Thanksgiving (US)",
    date(2026, 11, 27): "Black Friday - biggest sale day of the year",
    date(2026, 11, 30): "Cyber Monday",
    date(2026, 12, 25): "Christmas Day",
    date(2026, 12, 31): "New Year's Eve - recap content",
}

d = date(2026, 1, 1)
r = 2
while d.year == 2026:
    iso = d.isocalendar()
    yr.cell(row=r, column=1, value=d).number_format = DATEF
    yr.cell(row=r, column=2, value=iso[1])
    yr.cell(row=r, column=3, value=MONTHS[d.month - 1])
    yr.cell(row=r, column=4, value=d.day)
    yr.cell(row=r, column=5, value=WEEKDAYS[d.weekday()])
    yr.cell(row=r, column=6, value=key_dates.get(d, ""))
    d += timedelta(days=1)
    r += 1
last_year_row = r - 1  # 366 -> 365 rows of data
box(yr, 2, last_year_row, 1, 6, dates=(1,), ints=(2, 4))
for rr in range(2, last_year_row + 1):
    yr.cell(row=rr, column=1).alignment = Alignment(horizontal="center")
    for cc in (2, 4, 5):
        yr.cell(row=rr, column=cc).alignment = Alignment(horizontal="center")
    yr.cell(row=rr, column=6).alignment = Alignment(horizontal="left")
yr.freeze_panes = "A2"
yr.auto_filter.ref = f"A1:F{last_year_row}"
yr.conditional_formatting.add(
    f"F2:F{last_year_row}",
    FormulaRule(formula=["LEN($F2)>0"],
                fill=PatternFill("solid", fgColor=LIGHT),
                font=Font(name=FONT, bold=True, color=NAVY)))

# ========================================================== CONTENT CALENDAR
PLATFORMS = ["Instagram", "TikTok", "X", "YouTube", "LinkedIn", "Pinterest", "Facebook"]
PILLARS = ["Educate", "Entertain", "Inspire", "Promote", "Behind the scenes"]
FORMATS = ["Reel", "Carousel", "Story", "Long video", "Thread", "Pin", "Static"]
STATUSES = ["Idea", "Draft", "Scheduled", "Published", "Repurposed"]
CTAS = ["Follow for more", "Save this post", "Comment your take", "Book a free call",
        "Shop the offer", "Share with a teammate", "Tap the link in bio", "Watch part 2"]

cc = sheet(wb, "CONTENT CALENDAR")
c_headers = ["Date", "Platform", "Content pillar", "Format", "Hook/Title", "Caption notes",
             "CTA", "Status", "Publish link", "Likes", "Comments", "Shares", "Reach"]
c_widths = [13, 13, 17, 12, 40, 42, 18, 13, 34, 10, 11, 10, 12]
for i, (h, w) in enumerate(zip(c_headers, c_widths), start=1):
    cc.cell(row=1, column=i, value=h)
    cc.column_dimensions[get_column_letter(i)].width = w
hdr(cc, 1, c_headers)

hooks = [
    "3 hooks that stop the scroll in 2026",
    "Behind the scenes: a client kickoff call",
    "The 20-minute weekly content routine",
    "We tried posting daily for 30 days",
    "5 signs your brand needs a refresh",
    "What a $2k design budget actually buys",
    "Answering the top 5 client questions",
    "POV: your first viral reel lands",
    "Before / after: homepage redesign",
    "The mistake that kills cold emails",
    "How we plan a month of content in one hour",
    "Unboxing the new studio gear",
    "Why beats talent: the consistency math",
    "A day in the life of a small studio",
    "3 free tools we use every single day",
    "Client story: from brief to launch in 14 days",
    "Stop making this caption mistake",
    "The one metric you should watch instead of likes",
    "Reading our worst-performing post out loud",
    "Carousel vs reel: what to post where",
    "How to price your first freelance project",
    "Reply guy roast: bad website edition",
    "Our 5-step content approval flow",
    "Top 3 trends worth stealing this month",
    "What we learned from 100 client calls",
    "Set up with me: planning Q4 on one page",
    "The 3-second rule for video intros",
    "Steal our outreach template (free)",
    "Myth: you need to post every day",
    "How one pin drove 12k visits in a week",
    "Turn one long video into 7 short posts",
    "Meet the team: the person behind the captions",
    "Black Friday prep: the 5-post checklist",
    "Why we stopped chasing follower counts",
    "From idea to published in 90 seconds",
    "The anatomy of a post that gets saves",
    "Ask me anything: agency life answers",
    "Recap: what worked this quarter",
    "New offer announcement - design sprint",
    "Holiday content calendar you can copy",
]

random.seed(2026)
cc_rows = []
d0 = date(2026, 1, 5)
tail = [date(2026, 9, 20), date(2026, 9, 27), date(2026, 9, 28), date(2026, 9, 30)]
for i in range(40):
    if i < 36:
        dt = d0 + timedelta(days=i * 7 + random.randint(0, 3))
    else:
        dt = tail[i - 36]
    platform = PLATFORMS[i % len(PLATFORMS)]
    pillar = PILLARS[(i * 3) % len(PILLARS)]
    fmt = FORMATS[(i * 2) % len(FORMATS)]
    hook = hooks[i]
    caption = f"Hook in line 1, {pillar.lower()} angle, keep it under 150 words."
    cta = CTAS[i % len(CTAS)]
    if dt >= TODAY:
        status = "Scheduled"
    else:
        k = i % 10
        if k == 5:
            status = "Repurposed"
        elif k == 7:
            status = "Idea"
        elif k == 3:
            status = "Draft"
        else:
            status = "Published"
    link = ""
    likes = comments = shares = reach = None
    if status in ("Published", "Repurposed"):
        slug = ["reel", "carousel", "story", "video", "thread", "pin", "static"][i % 7]
        link = f"https://social.example/{slug}/{dt.strftime('%Y%m%d')}{i:02d}"
        reach = random.randint(1200, 46000)
        likes = int(reach * random.uniform(0.025, 0.075))
        comments = max(2, int(likes * random.uniform(0.02, 0.09)))
        shares = max(1, int(likes * random.uniform(0.03, 0.14)))
    cc_rows.append([dt, platform, pillar, fmt, hook, caption, cta, status,
                    link, likes, comments, shares, reach])

for i, vals in enumerate(cc_rows):
    r = 2 + i
    for c, v in enumerate(vals, start=1):
        if v is None or v == "":
            continue
        cc.cell(row=r, column=c, value=v)
last_cc = 1 + len(cc_rows)  # 41
box(cc, 2, last_cc, 1, 13, dates=(1,), ints=(10, 11, 12, 13))
for r in range(2, last_cc + 1):
    cc.cell(row=r, column=1).alignment = Alignment(horizontal="center")
    for c in (2, 3, 4, 7, 8):
        cc.cell(row=r, column=c).alignment = Alignment(horizontal="center")
cc.freeze_panes = "A2"
cc.auto_filter.ref = f"A1:M{last_cc}"

dv_list(cc, PLATFORMS, "B2:B500")
dv_list(cc, PILLARS, "C2:C500")
dv_list(cc, FORMATS, "D2:D500")
dv_list(cc, STATUSES, "H2:H500")
dv_list(cc, CTAS, "G2:G500", error="Pick a call to action or type your own")

status_cf(cc, "H2:H500", [
    ("Published", "D4EDDA", "1E7E34", False),
    ("Repurposed", "D1ECF1", "0C5460", False),
    ("Scheduled", "FFF3CD", "997404", False),
    ("Draft", "E2E3E5", "6C757D", False),
    ("Idea", "F8D7DA", "A02020", False),
])
cc.conditional_formatting.add(
    f"M2:M{last_cc}",
    DataBarRule(start_type="num", start_value=0, end_type="max", color=TEAL))

# ============================================================= POST TRACKER
tr = sheet(wb, "POST TRACKER")
t_headers = ["Date", "Platform", "Title", "Publish status", "URL", "Reach", "Likes",
             "Comments", "Shares", "Engagement %", "Link clicks", "Notes"]
t_widths = [13, 13, 40, 15, 34, 12, 10, 11, 10, 14, 12, 30]
for i, (h, w) in enumerate(zip(t_headers, t_widths), start=1):
    tr.cell(row=1, column=i, value=h)
    tr.column_dimensions[get_column_letter(i)].width = w
hdr(tr, 1, t_headers)

published = [row for row in cc_rows if row[7] in ("Published", "Repurposed")]
tracker_rows = []
for i, row in enumerate(published[:24]):
    dt, platform, pillar, fmt, hook = row[0], row[1], row[2], row[3], row[4]
    reach, likes, comments, shares = row[12], row[9], row[10], row[11]
    clicks = max(3, int(reach * random.uniform(0.004, 0.022)))
    note = "Boosted" if i % 8 == 3 else ("Posted 07:30" if i % 5 == 0 else "")
    tracker_rows.append([dt, platform, hook, "Live", row[8], reach, likes, comments,
                         shares, None, clicks, note])

for i, vals in enumerate(tracker_rows):
    r = 2 + i
    for c, v in enumerate(vals, start=1):
        if v is None or v == "":
            continue
        tr.cell(row=r, column=c, value=v)
    tr.cell(row=r, column=10, value=f"=IF(F{r}=0,0,(G{r}+H{r}+I{r})/F{r})")
last_tr = 1 + len(tracker_rows)
box(tr, 2, last_tr, 1, 12, dates=(1,), ints=(6, 7, 8, 9, 11), pct=(10,))
for r in range(2, last_tr + 1):
    tr.cell(row=r, column=1).alignment = Alignment(horizontal="center")
    tr.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    tr.cell(row=r, column=10).alignment = Alignment(horizontal="center")
tr.freeze_panes = "A2"
tr.auto_filter.ref = f"A1:L{last_tr}"
dv_list(tr, PLATFORMS, "B2:B500")
dv_list(tr, ["Live", "Scheduled", "Draft", "Archived"], "D2:D500")
status_cf(tr, "D2:D500", [
    ("Live", "D4EDDA", "1E7E34", False),
    ("Scheduled", "FFF3CD", "997404", False),
    ("Draft", "E2E3E5", "6C757D", False),
    ("Archived", "F8D7DA", "A02020", False),
])
tr.conditional_formatting.add(
    f"J2:J{last_tr}",
    CellIsRule(operator="greaterThanOrEqual", formula=["0.05"],
               font=Font(name=FONT, bold=True, color="1E7E34")))
tr.conditional_formatting.add(
    f"J2:J{last_tr}",
    CellIsRule(operator="lessThan", formula=["0.02"],
               font=Font(name=FONT, color="A02020")))

# ============================================================ IDEAS BACKLOG
ib = sheet(wb, "IDEAS BACKLOG")
i_headers = ["Idea", "Pillar", "Source", "Priority (1-5)", "Effort", "Chosen?"]
i_widths = [56, 19, 22, 15, 11, 12]
for i2, (h, w) in enumerate(zip(i_headers, i_widths), start=1):
    ib.cell(row=1, column=i2, value=h)
    ib.column_dimensions[get_column_letter(i2)].width = w
hdr(ib, 1, i_headers)

ideas = [
    ("Client onboarding walkthrough (screen record)", "Educate", "Client call", 4, "M", "Yes"),
    ("Poll: which logo do you prefer?", "Entertain", "Instagram story", 2, "S", "No"),
    ("Monthly metric recap graphic", "Educate", "Analytics", 3, "S", "Yes"),
    ("Studio playlist for deep work", "Behind the scenes", "Team", 1, "S", "No"),
    ("Case study: 3x more signups", "Promote", "Portfolio", 5, "L", "Yes"),
    ("Team fail Friday (funny edit)", "Entertain", "Team", 3, "M", "No"),
    ("Founder story: the first $1k month", "Inspire", "Journal", 4, "M", "Yes"),
    ("Tool stack breakdown carousel", "Educate", "Newsletter", 5, "M", "Yes"),
    ("Timelapse of a landing page build", "Behind the scenes", "Screen recording", 4, "M", "No"),
    ("Reply to the 'why is design so expensive' comment", "Educate", "Comments", 5, "S", "Yes"),
    ("Holiday greeting with the whole team", "Behind the scenes", "Calendar", 2, "S", "No"),
    ("Before/after of a messy brand kit", "Promote", "Portfolio", 4, "M", "No"),
    ("Duet a trending audio with our take", "Entertain", "TikTok trends", 3, "S", "No"),
    ("Free template giveaway", "Promote", "Marketing plan", 5, "M", "Yes"),
    ("What I'd do differently in year one", "Inspire", "Journal", 4, "M", "No"),
    ("Myth-busting: posting every day", "Educate", "Team", 3, "S", "Yes"),
    ("Office dogs of the studio", "Behind the scenes", "Team", 1, "S", "No"),
    ("Pricing tiers explained in 30 seconds", "Educate", "Sales calls", 5, "M", "No"),
]
for i2, vals in enumerate(ideas):
    r = 2 + i2
    for c, v in enumerate(vals, start=1):
        ib.cell(row=r, column=c, value=v)
last_ib = 1 + len(ideas)
box(ib, 2, last_ib, 1, 6, ints=(4,))
for r in range(2, last_ib + 1):
    for c in (2, 4, 5, 6):
        ib.cell(row=r, column=c).alignment = Alignment(horizontal="center")
ib.freeze_panes = "A2"
ib.auto_filter.ref = f"A1:F{last_ib}"
dv_list(ib, PILLARS, "B2:B500")
dv_list(ib, ["Newsletter", "Client call", "Analytics", "Team", "Portfolio", "Journal",
             "Comments", "Competitor", "Trends", "Customer question", "Other"],
        "C2:C500", error="Pick a source")
dv_list(ib, ["S", "M", "L"], "E2:E500")
dv_list(ib, ["Yes", "No"], "F2:F500")
dv_prio = DataValidation(type="whole", operator="between", formula1="1", formula2="5",
                         allow_blank=True)
dv_prio.error = "Priority must be 1 to 5"
ib.add_data_validation(dv_prio)
dv_prio.add("D2:D500")
status_cf(ib, "F2:F500", [("Yes", "D4EDDA", "1E7E34", True), ("No", "E2E3E5", "6C757D", False)])
ib.conditional_formatting.add(
    "D2:D500",
    CellIsRule(operator="greaterThanOrEqual", formula=["5"],
               fill=PatternFill("solid", fgColor="FFF3CD"),
               font=Font(name=FONT, bold=True, color="997404")))

# ============================================================= HASHTAG BANK
hb = sheet(wb, "HASHTAG BANK")
h_headers = ["Group name", "Tags", "Size", "Notes"]
h_widths = [26, 74, 14, 44]
for i2, (h, w) in enumerate(zip(h_headers, h_widths), start=1):
    hb.cell(row=1, column=i2, value=h)
    hb.column_dimensions[get_column_letter(i2)].width = w
hdr(hb, 1, h_headers)

tag_groups = [
    ("Core brand", "#novastudio #novastudiocreative #brandwithnova", "Branded",
     "Use on every post, first line of the caption"),
    ("Design broad", "#graphicdesign #designinspiration #visualidentity #logodesign", "Broad",
     "High volume - max 3 per post"),
    ("Design niche", "#brandidentity #logodesigner #designstudio #creativestudio", "Niche",
     "Best reach for portfolio posts"),
    ("Social media tips", "#socialmediatips #contentstrategy #contentcreator", "Broad",
     "Pair with one niche tag"),
    ("Small business", "#smallbusinesstips #smallbusinessowner #shopsmall", "Broad",
     "Strong on Instagram and Pinterest"),
    ("Freelance life", "#freelancelife #freelancedesigner #workfromanywhere", "Niche",
     "Great for behind-the-scenes posts"),
    ("Reels growth", "#reelsexplainer #reelsvideo #instagramreels", "Niche",
     "Only on Reels, never on carousels"),
    ("Educate series", "#design101 #learndesign #beginnerdesigner", "Niche",
     "Every how-to carousel"),
    ("Launch / offer", "#nowbooking #designsprint #limitedspots", "Branded",
     "Promote pillar only, 1x per week max"),
    ("Seasonal", "#blackfriday #newyeargoals #summervibes", "Broad",
     "Swap in seasonally - see YEAR 2026"),
]
for i2, vals in enumerate(tag_groups):
    r = 2 + i2
    for c, v in enumerate(vals, start=1):
        hb.cell(row=r, column=c, value=v)
last_hb = 1 + len(tag_groups)
box(hb, 2, last_hb, 1, 4)
for r in range(2, last_hb + 1):
    hb.cell(row=r, column=3).alignment = Alignment(horizontal="center")
hb.freeze_panes = "A2"
hb.auto_filter.ref = f"A1:D{last_hb}"
dv_list(hb, ["Broad", "Niche", "Branded"], "C2:C500")
status_cf(hb, "C2:C500", [
    ("Broad", "FFF3CD", "997404", False),
    ("Niche", "D4EDDA", "1E7E34", False),
    ("Branded", "D1ECF1", "0C5460", True),
])

# ================================================================ ANALYTICS
an = sheet(wb, "ANALYTICS")
a_headers = ["Week", "Posts published", "Reach", "Followers gained", "Profile visits",
             "Link clicks", "Engagement rate", "Weeks streak (auto)"]
a_widths = [10, 17, 14, 17, 15, 13, 17, 19]
for i2, (h, w) in enumerate(zip(a_headers, a_widths), start=1):
    an.cell(row=1, column=i2, value=h)
    an.column_dimensions[get_column_letter(i2)].width = w
hdr(an, 1, a_headers)

week_posts = {}
week_reach = {}
for row in cc_rows:
    if row[7] not in ("Published", "Repurposed"):
        continue
    wk = row[0].isocalendar()[1]
    week_posts[wk] = week_posts.get(wk, 0) + 1
    week_reach[wk] = week_reach.get(wk, 0) + (row[12] or 0)

for wk in range(1, 53):
    r = 1 + wk
    posts = week_posts.get(wk, 0)
    reach = week_reach.get(wk, 0)
    followers = int(reach * random.uniform(0.0008, 0.004)) if reach else 0
    visits = int(reach * random.uniform(0.012, 0.05)) if reach else 0
    clicks = int(reach * random.uniform(0.004, 0.014)) if reach else 0
    an.cell(row=r, column=1, value=f"W{wk}")
    an.cell(row=r, column=2, value=posts)
    an.cell(row=r, column=3, value=reach)
    an.cell(row=r, column=4, value=followers)
    an.cell(row=r, column=5, value=visits)
    an.cell(row=r, column=6, value=clicks)
    an.cell(row=r, column=7, value=f"=IF(C{r}=0,0,(D{r}+F{r})/C{r})")
    if wk == 1:
        an.cell(row=r, column=8, value=f"=IF(B{r}>0,1,0)")
    else:
        an.cell(row=r, column=8, value=f"=IF(B{r}>0,H{r - 1}+1,0)")
last_an = 52 + 1
box(an, 2, last_an, 1, 8, ints=(2, 3, 4, 5, 6), pct=(7,))
for r in range(2, last_an + 1):
    for c in (1, 2, 4, 5, 6, 7, 8):
        an.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    an.cell(row=r, column=8).font = Font(name=FONT, size=10, color=GREY)
an.freeze_panes = "A2"
an.auto_filter.ref = f"A1:H{last_an}"
an.conditional_formatting.add(
    f"G2:G{last_an}",
    CellIsRule(operator="greaterThanOrEqual", formula=["0.05"],
               font=Font(name=FONT, bold=True, color="1E7E34")))
an.conditional_formatting.add(
    f"G2:G{last_an}",
    CellIsRule(operator="lessThan", formula=["0.02"],
               font=Font(name=FONT, color="A02020")))
an.conditional_formatting.add(
    f"B2:B{last_an}",
    CellIsRule(operator="equal", formula=["0"],
               font=Font(name=FONT, color="A02020")))

# ================================================================ DASHBOARD
db = sheet(wb, "DASHBOARD")
widths(db, {"A": 3, "B": 32, "C": 15, "D": 15, "E": 15, "F": 15, "G": 12, "H": 12,
            "I": 12, "J": 11})
db["B2"] = "CONTENT DASHBOARD"
db["B2"].font = Font(name=FONT, bold=True, size=18, color=NAVY)
db["B3"] = "Counts the CONTENT CALENDAR, POST TRACKER and ANALYTICS sheets - live formulas."
db["B3"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

CC = "'CONTENT CALENDAR'"
AN = "'ANALYTICS'"

kpi(db, 5, 2, "POSTS ON THE CALENDAR (#)",
    f'=SUMPRODUCT(({CC}!$A$2:$A$41<>"")*1)')
kpi(db, 8, 2, "PUBLISHED + REPURPOSED (#)",
    f'=COUNTIF({CC}!$H:$H,"Published")+COUNTIF({CC}!$H:$H,"Repurposed")')
kpi(db, 11, 2, "TOTAL REACH", f"=SUM({CC}!$M:$M)")
kpi(db, 14, 2, "AVG ENGAGEMENT RATE",
    f'=IF(SUM({CC}!$M$2:$M$41)=0,0,(SUM({CC}!$J$2:$J$41)+SUM({CC}!$K$2:$K$41)'
    f'+SUM({CC}!$L$2:$L$41))/SUM({CC}!$M$2:$M$41))', fmt=PCT)
kpi(db, 17, 2, "POSTING STREAK (weeks)",
    f"=SUMPRODUCT(MAX({AN}!$H$2:$H$53))")
kpi(db, 20, 2, "YEAR COVERED (days with content)",
    f'=SUMPRODUCT(({CC}!$A$2:$A$41<>"")*1)/365', fmt=PCT)

# Status breakdown
band(db, 4, 4, 6, "STATUS BREAKDOWN", fill=TEAL)
hdr(db, 5, ["Status", "Posts", "Share"], start=4, fill=NAVY)
for i, st in enumerate(STATUSES):
    r = 6 + i
    db.cell(row=r, column=4, value=st)
    db.cell(row=r, column=5, value=f'=COUNTIF({CC}!$H:$H,D{r})')
    db.cell(row=r, column=6, value=f'=IF($B$6=0,0,E{r}/$B$6)')
box(db, 6, 10, 4, 6, ints=(5,))
for r in range(6, 11):
    db.cell(row=r, column=4).alignment = Alignment(horizontal="left")
    db.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=6).number_format = PCT
    db.cell(row=r, column=6).alignment = Alignment(horizontal="center")
status_cf(db, "D6:D10", [
    ("Published", "D4EDDA", "1E7E34", True),
    ("Repurposed", "D1ECF1", "0C5460", False),
    ("Scheduled", "FFF3CD", "997404", False),
    ("Draft", "E2E3E5", "6C757D", False),
    ("Idea", "F8D7DA", "A02020", False),
])

# Platform breakdown
band(db, 12, 4, 6, "BY PLATFORM", fill=TEAL)
hdr(db, 13, ["Platform", "Posts", "Reach"], start=4, fill=NAVY)
for i, pf in enumerate(PLATFORMS):
    r = 14 + i
    db.cell(row=r, column=4, value=pf)
    db.cell(row=r, column=5, value=f'=COUNTIF({CC}!$B:$B,D{r})')
    db.cell(row=r, column=6, value=f'=SUMIF({CC}!$B:$B,D{r},{CC}!$M:$M)')
box(db, 14, 20, 4, 6, ints=(5, 6))
for r in range(14, 21):
    db.cell(row=r, column=4).alignment = Alignment(horizontal="left")
    db.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=6).alignment = Alignment(horizontal="right")

# Posts per month by platform
band(db, 23, 2, 10, "POSTS PER MONTH BY PLATFORM (COUNTIFS)")
hdr(db, 24, ["Month"] + PLATFORMS + ["Total"], start=2, fill=TEAL)
for m in range(1, 13):
    r = 24 + m
    db.cell(row=r, column=2, value=MONTHS_SHORT[m - 1])
    for p in range(7):
        col = 3 + p
        letter = get_column_letter(col)
        db.cell(row=r, column=col,
                value=f'=COUNTIFS({CC}!$B:$B,{letter}$24,{CC}!$A:$A,">="&DATE(2026,{m},1),'
                      f'{CC}!$A:$A,"<"&DATE(2026,{m + 1},1))')
    db.cell(row=r, column=10, value=f"=SUM(C{r}:I{r})")
box(db, 25, 36, 2, 10, ints=tuple(range(3, 11)))
for r in range(25, 37):
    db.cell(row=r, column=2).alignment = Alignment(horizontal="left")
    db.cell(row=r, column=2).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
    for c in range(3, 11):
        db.cell(row=r, column=c).alignment = Alignment(horizontal="center")
db.cell(row=37, column=2, value="TOTAL")
for c in range(3, 11):
    letter = get_column_letter(c)
    db.cell(row=37, column=c, value=f"=SUM({letter}25:{letter}36)")
for c in range(2, 11):
    cell = db.cell(row=37, column=c)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.font = Font(name=FONT, bold=True, color=WHITE, size=11)
    cell.border = border
    cell.alignment = Alignment(horizontal="center" if c > 2 else "left")
    if c > 2:
        cell.number_format = "#,##0"
db.conditional_formatting.add(
    "J25:J36",
    CellIsRule(operator="greaterThanOrEqual", formula=["6"],
               fill=PatternFill("solid", fgColor="D4EDDA"),
               font=Font(name=FONT, bold=True, color="1E7E34")))

db["B39"] = "Everything above recalculates from the log sheets - do not type over the formulas."
db["B39"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

# ---------------------------------------------------------------- SAVE
wb.active = 0
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Content_Calendar_and_Social_Media_Planner_2026.xlsx")
wb.save(out)
print("saved:", out)
