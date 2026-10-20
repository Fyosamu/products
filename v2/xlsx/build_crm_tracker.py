# -*- coding: utf-8 -*-
"""Build: Client CRM & Project Tracker (XLSX)"""
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


def box(ws, r1, r2, c1, c2, money=(), dates=(), pct=(), num=(), ints=(), zebra=True):
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
            elif c in num:
                cell.number_format = "#,##0.0"
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


def kpi(ws, row, col, label, formula, fmt=MONEY):
    lab = ws.cell(row=row, column=col, value=label)
    lab.font = Font(name=FONT, bold=True, size=10, color=WHITE)
    lab.fill = PatternFill("solid", fgColor=NAVY)
    lab.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    lab.border = border
    val = ws.cell(row=row + 1, column=col, value=formula)
    val.font = Font(name=FONT, bold=True, size=17, color=TEAL)
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
    "CLIENT CRM & PROJECT TRACKER",
    "Pipeline  ·  Projects  ·  Timesheet  ·  Deliverables  ·  Follow-ups  ·  Live dashboard",
    [
        "",
        "HOW TO USE THIS WORKBOOK (5 minutes to set up)",
        "",
        "1. Log every new lead in PIPELINE: company, source, stage, deal value, next action.",
        "2. Probability fills the Weighted value column - that is your real forecast number.",
        "3. When a lead says yes, add the job to PROJECTS and move the lead to Won.",
        "4. Set your hourly cost in cell B1 of PROJECTS - Profit = Value - logged hours x cost.",
        "5. Log time daily in TIMESHEET. PROJECTS pulls the hours in with SUMIF automatically.",
        "6. Track every hand-off in DELIVERABLES and every promise in FOLLOW-UPS.",
        "7. Read the DASHBOARD before your Monday planning - it is all live formulas.",
        "",
        "RULES THAT KEEP IT CLEAN",
        "",
        "- Never delete rows - move lost leads to stage Lost and closed jobs to Closed.",
        "- Use the drop-down lists (Source, Stage, Status, Channel) so the dashboard counts work.",
        "- Enter amounts as plain numbers: type 4500 not $4,500 and 0.25 for 25%.",
        "- Dates use dd-mmm-yyyy, e.g. 12-Sep-2026. The workbook uses TODAY() to spot overdue work.",
        "- Timesheet rows must use a project name from the PROJECTS sheet, exactly as written.",
        "- Give every lead a next follow-up date - blank dates are how deals quietly die.",
        "",
        "THE FOLLOW-UP RULE",
        "",
        "1. Every open lead gets a next action and a next follow-up date. No exceptions.",
        "2. Red date = you promised a call or email and today is already past it. Fix it first.",
        "3. Chase in the client's channel: Email for docs, Call for money, WhatsApp for speed.",
    ],
)

# ================================================================== PIPELINE
pl = sheet(wb, "PIPELINE")
p_headers = ["Lead", "Company", "Source", "Stage", "Deal value", "Probability",
             "Weighted value", "Owner", "Next action", "Next follow-up", "Last contact",
             "Status notes"]
p_widths = [20, 21, 15, 17, 14, 13, 16, 12, 30, 16, 15, 32]
for i, (h, w) in enumerate(zip(p_headers, p_widths), start=1):
    pl.cell(row=1, column=i, value=h)
    pl.column_dimensions[get_column_letter(i)].width = w
hdr(pl, 1, p_headers)

STAGES = ["New", "Contacted", "Discovery", "Proposal sent", "Negotiating", "Won", "Lost"]
PROB = {"New": 0.10, "Contacted": 0.20, "Discovery": 0.35, "Proposal sent": 0.50,
        "Negotiating": 0.70, "Won": 1.0, "Lost": 0.0}
SOURCES = ["Referral", "Instagram", "Upwork", "Cold email", "Repeat", "Other"]
OWNERS = ["Alex", "Priya", "Sam"]
leads = [
    ("Maya Chen", "Bluebird Retail", "Referral", "Negotiating", 9500, "Alex",
     "Send revised scope + payment plan", date(2026, 9, 29), date(2026, 9, 8),
     "Wants 3 payment instalments"),
    ("Daniel Ortiz", "Zenith Fitness", "Instagram", "Proposal sent", 6400, "Priya",
     "Follow up on proposal", date(2026, 9, 24), date(2026, 9, 18),
     "Proposal opened twice"),
    ("Ruth Kimani", "Nova Education", "Upwork", "Discovery", 4200, "Sam",
     "Book discovery call", date(2026, 9, 30), date(2026, 9, 21),
     "Budget confirmed at 4k"),
    ("Tom Whitfield", "Harbor Labs", "Repeat", "Won", 7800, "Alex",
     "Kick-off booked", date(2026, 9, 12), date(2026, 9, 2),
     "Signed - deposit invoice sent"),
    ("Sofia Almeida", "Loop Agency", "Referral", "Contacted", 3600, "Priya",
     "Send portfolio pack", date(2026, 10, 2), date(2026, 9, 22),
     "Warm intro from Maya"),
    ("Noah Patel", "Orbit CRM", "Cold email", "New", 2800, "Sam",
     "First outreach email", date(2026, 10, 6), date(2026, 9, 25),
     "Opened email, no reply yet"),
    ("Grace Adeyemi", "Pixelworks", "Instagram", "Proposal sent", 5200, "Alex",
     "Chase signed quote", date(2026, 9, 19), date(2026, 9, 11),
     "Waiting on finance approval"),
    ("Lukas Meyer", "Acme SaaS", "Repeat", "Negotiating", 12000, "Priya",
     "Confirm retainer terms", date(2026, 9, 29), date(2026, 9, 23),
     "Retainer discussion, month 2"),
    ("Ivy Zhang", "Copper & Co", "Upwork", "Lost", 3100, "Sam",
     "No action - archived", date(2026, 8, 14), date(2026, 8, 14),
     "Went with an in-house hire"),
    ("Omar Haddad", "Fern Health", "Cold email", "Discovery", 4800, "Alex",
     "Send discovery deck", date(2026, 9, 29), date(2026, 9, 20),
     "Clinic chain, 4 locations"),
    ("Ella Novak", "Trailhead App", "Instagram", "New", 2400, "Priya",
     "Reply to DM with pricing", date(2026, 10, 1), date(2026, 9, 26),
     "Asked for a one-pager"),
    ("Marcus Bell", "Bell & Sons", "Referral", "Won", 5600, "Sam",
     "Deposit received, start 1 Oct", date(2026, 9, 18), date(2026, 9, 14),
     "Referral from Tom"),
    ("Priyanka Rao", "Bluebird Retail", "Repeat", "Proposal sent", 7200, "Alex",
     "Send phase 2 proposal", date(2026, 9, 21), date(2026, 9, 16),
     "Phase 1 delivered on time"),
    ("Felix Braun", "Kraft Studio", "Upwork", "Contacted", 1900, "Priya",
     "Qualify budget on call", date(2026, 9, 10), date(2026, 9, 4),
     "Small logo job"),
    ("Amara Osei", "Zenith Fitness", "Referral", "New", 3300, "Sam",
     "Intro call invite", date(2026, 10, 3), date(2026, 9, 12),
     "From the same gym"),
    ("Henry Ford II", "Motor Works", "Other", "Lost", 8800, "Alex",
     "No action - archived", date(2026, 7, 22), date(2026, 7, 22),
     "Price objection"),
    ("Nina Kowalski", "Sunrise Bakery", "Instagram", "Discovery", 1500, "Priya",
     "Send menu redesign ideas", date(2026, 9, 28), date(2026, 9, 23),
     "Small local business"),
    ("Victor Silva", "Acme SaaS", "Cold email", "Proposal sent", 4500, "Sam",
     "Send proposal PDF", date(2026, 10, 8), date(2026, 9, 24),
     "Docs site restructure"),
    ("Leila Farouk", "Nova Education", "Repeat", "Negotiating", 6800, "Alex",
     "Agree payment schedule", date(2026, 9, 29), date(2026, 9, 19),
     "Repeat client, 3rd project"),
    ("Jack Turner", "Trailhead App", "Upwork", "New", 2600, "Priya",
     "Send availability", date(2026, 10, 13), date(2026, 9, 26),
     "Needs 2 weeks notice"),
    ("Rosa Martinez", "Copper & Co", "Referral", "Contacted", 3900, "Sam",
     "Send case studies", date(2026, 10, 1), date(2026, 9, 17),
     "Retail brand refresh"),
    ("Ben Carter", "Fern Health", "Instagram", "Discovery", 5400, "Alex",
     "Scope the app screens", date(2026, 10, 5), date(2026, 9, 22),
     "Second contact from clinic"),
    ("Aiko Tanaka", "Kraft Studio", "Other", "New", 2100, "Priya",
     "Qualify on WhatsApp", date(2026, 9, 9), date(2026, 9, 2),
     "Came from a workshop"),
    ("Sean Murphy", "Bell & Sons", "Repeat", "Won", 3400, "Sam",
     "Kick-off notes shared", date(2026, 9, 30), date(2026, 9, 25),
     "Repeat after phase 1"),
    ("Zoe Fischer", "Motor Works", "Cold email", "Lost", 4700, "Alex",
     "No action - archived", date(2026, 8, 31), date(2026, 8, 31),
     "No budget until Q1 2027"),
]
for i, (lead, comp, src, stage, value, owner, action, next_f, last_c, notes) in enumerate(leads):
    r = 2 + i
    pl.cell(row=r, column=1, value=lead)
    pl.cell(row=r, column=2, value=comp)
    pl.cell(row=r, column=3, value=src)
    pl.cell(row=r, column=4, value=stage)
    pl.cell(row=r, column=5, value=value)
    pl.cell(row=r, column=6, value=PROB[stage])
    pl.cell(row=r, column=7, value=f"=E{r}*F{r}")
    pl.cell(row=r, column=8, value=owner)
    pl.cell(row=r, column=9, value=action)
    pl.cell(row=r, column=10, value=next_f)
    pl.cell(row=r, column=11, value=last_c)
    pl.cell(row=r, column=12, value=notes)
last_pl = 1 + len(leads)
box(pl, 2, last_pl, 1, 12, money=(5, 7), dates=(10, 11), pct=(6,))
for r in range(2, last_pl + 1):
    for c in (3, 4, 6, 8, 10, 11):
        pl.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    pl.cell(row=r, column=1).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
pl.freeze_panes = "A2"
pl.auto_filter.ref = f"A1:L{last_pl}"

dv_list(pl, SOURCES, "C2:C400")
dv_list(pl, STAGES, "D2:D400")
dv_list(pl, OWNERS, "H2:H400")
status_cf(pl, "D2:D400", [
    ("Won", "D4EDDA", "1E7E34", True),
    ("Lost", "F8D7DA", "A02020", True),
    ("Negotiating", "FFF3CD", "997404", True),
    ("Proposal sent", "D1ECF1", "0C5460", False),
    ("Discovery", "E2E3E5", "6C757D", False),
    ("Contacted", "E2E3E5", "6C757D", False),
    ("New", "E2E3E5", "6C757D", False),
])
pl.conditional_formatting.add(
    "J2:J400",
    FormulaRule(formula=['AND($J2<>"",$J2<TODAY(),$D2<>"Won",$D2<>"Lost")'],
                fill=PatternFill("solid", fgColor="F8D7DA"),
                font=Font(name=FONT, bold=True, color="A02020")))
pl.conditional_formatting.add(
    "J2:J400",
    FormulaRule(formula=['AND($J2<>"",$J2>=TODAY(),$J2<=TODAY()+3,$D2<>"Won",$D2<>"Lost")'],
                fill=PatternFill("solid", fgColor="FFF3CD"),
                font=Font(name=FONT, bold=True, color="997404")))
pl.conditional_formatting.add(
    f"G2:G{last_pl}",
    DataBarRule(start_type="num", start_value=0, end_type="max", color=TEAL))

# ================================================================= PROJECTS
pj = sheet(wb, "PROJECTS")
lb = pj.cell(row=1, column=1, value="Your hourly cost:")
lb.font = Font(name=FONT, bold=True, size=11, color=GREY)
lb.border = border
rate_cell = pj.cell(row=1, column=2, value=75)
rate_cell.font = Font(name=FONT, bold=True, size=12, color=TEAL)
rate_cell.fill = PatternFill("solid", fgColor=LIGHT)
rate_cell.border = border
rate_cell.number_format = MONEY
rate_cell.alignment = Alignment(horizontal="center")
for c in range(3, 12):
    pj.cell(row=1, column=c).border = border
pj.cell(row=1, column=3, value="(edit this - Profit = Value - logged hours x cost)")
pj.cell(row=1, column=3).font = Font(name=FONT, size=10, color=GREY, italic=True)

j_headers = ["Project", "Client", "Status", "Start", "Deadline", "Budget hours",
             "Logged hours", "% complete", "Value", "Profit", "Notes"]
j_widths = [28, 20, 13, 13, 13, 14, 14, 13, 14, 14, 34]
for i, (h, w) in enumerate(zip(j_headers, j_widths), start=1):
    pj.cell(row=2, column=i, value=h)
    pj.column_dimensions[get_column_letter(i)].width = w
hdr(pj, 2, j_headers)

projects = [
    ("Website redesign", "Acme SaaS", "Active", date(2026, 6, 1), date(2026, 10, 15), 120, 9800,
     "Phase 2 - pricing page in review"),
    ("Brand refresh", "Loop Agency", "Review", date(2026, 7, 6), date(2026, 9, 30), 60, 5200,
     "Client reviewing the final logo suite"),
    ("CRM onboarding", "Orbit CRM", "Active", date(2026, 8, 3), date(2026, 10, 2), 80, 6400,
     "Migration weekend booked for 3 Oct"),
    ("Social pack Q3", "Pixelworks", "Delivered", date(2026, 5, 4), date(2026, 6, 12), 45, 3600,
     "Delivered 10 Jun, invoice paid"),
    ("Landing page sprint", "Harbor Labs", "Active", date(2026, 9, 7), date(2026, 9, 24), 40, 3200,
     "Deadline slipped - client copy late"),
    ("SEO content engine", "Bluebird Retail", "Active", date(2026, 4, 1), date(2026, 12, 18), 150,
     11000, "8 articles a month, retainer"),
    ("Mobile app UI", "Zenith Fitness", "On hold", date(2026, 3, 2), date(2026, 11, 13), 200, 14500,
     "Paused while they raise funding"),
    ("Course platform", "Nova Education", "Planned", date(2026, 10, 5), date(2026, 12, 4), 90, 7200,
     "Starts after the October release"),
    ("Email automation", "Acme SaaS", "Delivered", date(2026, 2, 2), date(2026, 3, 6), 35, 2800,
     "Delivered 4 Mar, paid in full"),
    ("Annual report design", "Orbit CRM", "Closed", date(2026, 1, 12), date(2026, 2, 20), 50, 4000,
     "Closed - files archived"),
    ("Video edit series", "Pixelworks", "Active", date(2026, 8, 17), date(2026, 10, 9), 55, 4400,
     "12 edits, 4 delivered so far"),
    ("Ecommerce audit", "Bluebird Retail", "Review", date(2026, 8, 24), date(2026, 9, 18), 30, 2400,
     "Report sent, awaiting feedback"),
]
for i, (name, client, status, start, deadline, budget, value, notes) in enumerate(projects):
    r = 3 + i
    pj.cell(row=r, column=1, value=name)
    pj.cell(row=r, column=2, value=client)
    pj.cell(row=r, column=3, value=status)
    pj.cell(row=r, column=4, value=start)
    pj.cell(row=r, column=5, value=deadline)
    pj.cell(row=r, column=6, value=budget)
    pj.cell(row=r, column=7, value=f"=SUMIF('TIMESHEET'!$B:$B,$A{r},'TIMESHEET'!$D:$D)")
    pj.cell(row=r, column=8, value=f"=IF(F{r}=0,0,G{r}/F{r})")
    pj.cell(row=r, column=9, value=value)
    pj.cell(row=r, column=10, value=f"=I{r}-G{r}*$B$1")
    pj.cell(row=r, column=11, value=notes)
last_pj = 2 + len(projects)
box(pj, 3, last_pj, 1, 11, money=(9, 10), dates=(4, 5), pct=(8,), num=(6, 7))
for r in range(3, last_pj + 1):
    pj.cell(row=r, column=1).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
    for c in (3, 4, 5, 8):
        pj.cell(row=r, column=c).alignment = Alignment(horizontal="center")
pj.freeze_panes = "A3"
pj.auto_filter.ref = f"A2:K{last_pj}"
dv_list(pj, ["Planned", "Active", "On hold", "Review", "Delivered", "Closed"], "C3:C400")
status_cf(pj, "C3:C400", [
    ("Active", "D1ECF1", "0C5460", True),
    ("Delivered", "D4EDDA", "1E7E34", True),
    ("Closed", "E2E3E5", "6C757D", False),
    ("On hold", "F8D7DA", "A02020", True),
    ("Review", "FFF3CD", "997404", False),
    ("Planned", "E2E3E5", "6C757D", False),
])
pj.conditional_formatting.add(
    f"E3:E{last_pj}",
    FormulaRule(formula=['AND($E3<>"",$E3<TODAY(),$C3<>"Closed",$C3<>"Delivered")'],
                fill=PatternFill("solid", fgColor="F8D7DA"),
                font=Font(name=FONT, bold=True, color="A02020")))
pj.conditional_formatting.add(
    f"E3:E{last_pj}",
    FormulaRule(formula=['AND($E3<>"",$E3>=TODAY(),$E3<=TODAY()+7,$C3<>"Closed",'
                         '$C3<>"Delivered")'],
                fill=PatternFill("solid", fgColor="FFF3CD"),
                font=Font(name=FONT, bold=True, color="997404")))
pj.conditional_formatting.add(
    f"H3:H{last_pj}",
    CellIsRule(operator="greaterThan", formula=["1"],
               fill=PatternFill("solid", fgColor="F8D7DA"),
               font=Font(name=FONT, bold=True, color="A02020")))

# ================================================================ TIMESHEET
ts = sheet(wb, "TIMESHEET")
t_headers = ["Date", "Project", "Task", "Hours", "Billable", "Rate", "Amount",
             "Invoiced?", "Notes"]
t_widths = [13, 26, 32, 10, 12, 11, 13, 12, 28]
for i, (h, w) in enumerate(zip(t_headers, t_widths), start=1):
    ts.cell(row=1, column=i, value=h)
    ts.column_dimensions[get_column_letter(i)].width = w
hdr(ts, 1, t_headers)

tasks = ["Discovery call", "Wireframes", "Visual design", "Copywriting", "Client revisions",
         "Stand-up + notes", "Build / QA", "Analytics setup", "Asset export", "Proposal writing"]
plan = [
    ("Website redesign", date(2026, 6, 1), date(2026, 9, 25), 8, 95),
    ("CRM onboarding", date(2026, 8, 3), date(2026, 9, 24), 6, 95),
    ("Landing page sprint", date(2026, 9, 7), date(2026, 9, 25), 5, 110),
    ("SEO content engine", date(2026, 4, 1), date(2026, 9, 23), 7, 85),
    ("Video edit series", date(2026, 8, 17), date(2026, 9, 22), 4, 90),
    ("Brand refresh", date(2026, 7, 6), date(2026, 9, 17), 4, 100),
    ("Social pack Q3", date(2026, 5, 4), date(2026, 6, 10), 2, 80),
    ("Email automation", date(2026, 2, 2), date(2026, 3, 4), 2, 95),
    ("Ecommerce audit", date(2026, 8, 24), date(2026, 9, 16), 2, 110),
]
hours_by_project = {
    "Landing page sprint": [9.0, 8.5, 10.0, 8.0, 9.0],
    "Website redesign": [6.5, 4.0, 7.5, 5.0, 6.0, 3.5, 5.5, 4.5],
    "CRM onboarding": [5.0, 4.5, 6.0, 3.5, 5.5, 4.0],
    "SEO content engine": [4.5, 6.0, 3.5, 5.0, 4.0, 5.5, 4.5],
    "Video edit series": [5.5, 4.5, 6.0, 5.0],
    "Brand refresh": [4.0, 5.5, 3.5, 4.5],
    "Social pack Q3": [4.5, 5.0],
    "Email automation": [3.5, 3.0],
    "Ecommerce audit": [6.5, 5.5],
}
random.seed(7)
ts_rows = []
for proj, d_start, d_end, count, rate in plan:
    hours = hours_by_project[proj]
    span = (d_end - d_start).days
    for i in range(count):
        d = d_start + timedelta(days=int(span * (i + 0.5) / count) + random.randint(0, 1))
        billable = "No" if (proj == "CRM onboarding" and i == 2) else "Yes"
        if d < date(2026, 7, 1):
            invoiced = "Yes"
        elif d < date(2026, 9, 1):
            invoiced = "Yes" if i % 3 else "Partial"
        else:
            invoiced = "No" if i % 2 else "Partial"
        ts_rows.append([d, proj, tasks[(i + len(proj)) % len(tasks)], hours[i], billable,
                        rate, None, invoiced, ""])
ts_rows.sort(key=lambda x: x[0])
assert len(ts_rows) == 40, len(ts_rows)
for i, vals in enumerate(ts_rows):
    r = 2 + i
    for c, v in enumerate(vals, start=1):
        if v is None:
            continue
        ts.cell(row=r, column=c, value=v)
    ts.cell(row=r, column=7, value=f'=IF(E{r}="No",0,D{r}*F{r})')
last_ts = 1 + len(ts_rows)
box(ts, 2, last_ts, 1, 9, money=(6, 7), dates=(1,), num=(4,))
for r in range(2, last_ts + 1):
    for c in (5, 8):
        ts.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    ts.cell(row=r, column=4).alignment = Alignment(horizontal="center")
ts.freeze_panes = "A2"
ts.auto_filter.ref = f"A1:I{last_ts}"
dv_list(ts, [p[0] for p in plan] + ["Mobile app UI", "Course platform",
                                    "Annual report design"], "B2:B500")
dv_list(ts, ["Yes", "No"], "E2:E500")
dv_list(ts, ["Yes", "No", "Partial"], "H2:H500")
status_cf(ts, "E2:E500", [("Yes", "D4EDDA", "1E7E34", False),
                          ("No", "E2E3E5", "6C757D", False)])
status_cf(ts, "H2:H500", [("Yes", "D4EDDA", "1E7E34", False),
                          ("Partial", "FFF3CD", "997404", False),
                          ("No", "F8D7DA", "A02020", False)])
ts.conditional_formatting.add(
    f"G2:G{last_ts}",
    DataBarRule(start_type="num", start_value=0, end_type="max", color=TEAL))
ts.conditional_formatting.add(
    f"D2:D{last_ts}",
    CellIsRule(operator="greaterThan", formula=["8"],
               fill=PatternFill("solid", fgColor="FFF3CD"),
               font=Font(name=FONT, bold=True, color="997404")))

# ============================================================= DELIVERABLES
dl = sheet(wb, "DELIVERABLES")
d_headers = ["Deliverable", "Project", "Owner", "Due date", "Status", "Version", "Notes"]
d_widths = [34, 26, 12, 14, 17, 10, 34]
for i, (h, w) in enumerate(zip(d_headers, d_widths), start=1):
    dl.cell(row=1, column=i, value=h)
    dl.column_dimensions[get_column_letter(i)].width = w
hdr(dl, 1, d_headers)
deliverables = [
    ("Home page wireframes", "Website redesign", "Priya", date(2026, 6, 12), "Approved", "v3",
     "Signed off by Maya"),
    ("Design system tokens", "Website redesign", "Alex", date(2026, 9, 29), "In progress", "v1",
     "Colour + spacing scales"),
    ("Pricing page copy", "Website redesign", "Sam", date(2026, 9, 22), "Client review", "v2",
     "Waiting on client feedback"),
    ("Logo suite", "Brand refresh", "Alex", date(2026, 9, 8), "Approved", "v4", "Final files sent"),
    ("Brand guidelines PDF", "Brand refresh", "Priya", date(2026, 10, 2), "In progress", "v1",
     "24 pages so far"),
    ("Contact import map", "CRM onboarding", "Sam", date(2026, 8, 14), "Approved", "v2", ""),
    ("Pipeline automation", "CRM onboarding", "Alex", date(2026, 10, 1), "In progress", "v1",
     "Stage change triggers"),
    ("Launch landing page", "Landing page sprint", "Priya", date(2026, 9, 20), "Rejected", "v1",
     "Client wants a different hero"),
    ("A/B test plan", "Landing page sprint", "Sam", date(2026, 9, 30), "Not started", "", ""),
    ("8 SEO articles", "SEO content engine", "Sam", date(2026, 9, 15), "Approved", "v1",
     "September batch"),
    ("Keyword map Q4", "SEO content engine", "Sam", date(2026, 10, 6), "Not started", "", ""),
    ("Edit - product teaser", "Video edit series", "Priya", date(2026, 9, 11), "Approved", "v2",
     "Delivered to client"),
    ("Edit - founder interview", "Video edit series", "Priya", date(2026, 9, 28),
     "Client review", "v1", "Colour grade pending"),
    ("Social pack - October", "Social pack Q3", "Alex", date(2026, 6, 5), "Approved", "v2", ""),
    ("Automation report", "Email automation", "Alex", date(2026, 3, 4), "Approved", "v1", ""),
    ("Audit findings deck", "Ecommerce audit", "Sam", date(2026, 9, 17), "Client review", "v1",
     "Sent 17 Sep, chasing feedback"),
]
for i, vals in enumerate(deliverables):
    r = 2 + i
    for c, v in enumerate(vals, start=1):
        dl.cell(row=r, column=c, value=v)
last_dl = 1 + len(deliverables)
box(dl, 2, last_dl, 1, 7, dates=(4,))
for r in range(2, last_dl + 1):
    for c in (3, 4, 5, 6):
        dl.cell(row=r, column=c).alignment = Alignment(horizontal="center")
dl.freeze_panes = "A2"
dl.auto_filter.ref = f"A1:G{last_dl}"
dv_list(dl, ["Not started", "In progress", "Client review", "Approved", "Rejected"],
        "E2:E400")
dv_list(dl, OWNERS, "C2:C400")
dv_list(dl, ["v1", "v2", "v3", "v4", "v5"], "F2:F400")
status_cf(dl, "E2:E400", [
    ("Approved", "D4EDDA", "1E7E34", True),
    ("Rejected", "F8D7DA", "A02020", True),
    ("Client review", "FFF3CD", "997404", False),
    ("In progress", "D1ECF1", "0C5460", False),
    ("Not started", "E2E3E5", "6C757D", False),
])
dl.conditional_formatting.add(
    f"D2:D{last_dl}",
    FormulaRule(formula=['AND($D2<>"",$D2<TODAY(),$E2<>"Approved",$E2<>"Rejected")'],
                fill=PatternFill("solid", fgColor="F8D7DA"),
                font=Font(name=FONT, bold=True, color="A02020")))

# ================================================================ FOLLOW-UPS
fu = sheet(wb, "FOLLOW-UPS")
f_headers = ["Date", "Contact", "Company", "Channel", "What was discussed", "Outcome",
             "Next step", "Next date"]
f_widths = [13, 18, 21, 14, 42, 24, 34, 14]
for i, (h, w) in enumerate(zip(f_headers, f_widths), start=1):
    fu.cell(row=1, column=i, value=h)
    fu.column_dimensions[get_column_letter(i)].width = w
hdr(fu, 1, f_headers)
CHANNELS = ["Email", "Call", "WhatsApp", "DM"]
followups = [
    (date(2026, 9, 25), "Maya Chen", "Bluebird Retail", "Call", "Payment plan and revised scope",
     "Waiting on client", "Send revised proposal", date(2026, 9, 28)),
    (date(2026, 9, 24), "Daniel Ortiz", "Zenith Fitness", "Email", "Proposal questions",
     "Proposal sent", "Chase signature", date(2026, 9, 22)),
    (date(2026, 9, 21), "Ruth Kimani", "Nova Education", "WhatsApp", "Discovery call booked",
     "Booked", "Send calendar invite", date(2026, 9, 29)),
    (date(2026, 9, 18), "Grace Adeyemi", "Pixelworks", "Email", "Quote status",
     "Waiting on client", "Follow up again", date(2026, 9, 16)),
    (date(2026, 9, 17), "Lukas Meyer", "Acme SaaS", "Call", "Retainer month 2",
     "Closed won", "Send month 2 invoice", date(2026, 9, 30)),
    (date(2026, 9, 16), "Priyanka Rao", "Bluebird Retail", "Email", "Phase 1 handover",
     "Proposal sent", "Draft phase 2 proposal", date(2026, 9, 21)),
    (date(2026, 9, 14), "Marcus Bell", "Bell & Sons", "WhatsApp", "Deposit confirmation",
     "Closed won", "Book kick-off", None),
    (date(2026, 9, 12), "Omar Haddad", "Fern Health", "Call", "Clinic chain requirements",
     "Booked", "Send discovery deck", date(2026, 9, 26)),
    (date(2026, 9, 10), "Felix Braun", "Kraft Studio", "DM", "Budget qualification",
     "No reply", "Qualify on WhatsApp", None),
    (date(2026, 9, 8), "Nina Kowalski", "Sunrise Bakery", "WhatsApp", "Menu redesign ideas",
     "Proposal sent", "Send quote", date(2026, 10, 2)),
    (date(2026, 9, 5), "Sofia Almeida", "Loop Agency", "Email", "Portfolio pack sent",
     "Waiting on client", "Follow up politely", date(2026, 10, 7)),
    (date(2026, 9, 3), "Victor Silva", "Acme SaaS", "Email", "Docs site restructure",
     "Proposal sent", "Send proposal PDF", date(2026, 10, 9)),
    (date(2026, 8, 28), "Aiko Tanaka", "Kraft Studio", "WhatsApp", "Workshop follow-up",
     "Waiting on client", "Qualify timeline", date(2026, 9, 30)),
    (date(2026, 8, 26), "Ben Carter", "Fern Health", "Call", "App screen scope",
     "Booked", "Scope the screens", date(2026, 9, 30)),
    (date(2026, 8, 20), "Leila Farouk", "Nova Education", "Email", "Payment schedule options",
     "Waiting on client", "Agree 50/50 schedule", date(2026, 10, 5)),
    (date(2026, 8, 18), "Rosa Martinez", "Copper & Co", "Email", "Case studies requested",
     "Waiting on client", "Book intro call", date(2026, 10, 1)),
    (date(2026, 8, 12), "Tom Whitfield", "Harbor Labs", "Call", "Project kick-off",
     "Closed won", "Share kick-off notes", None),
    (date(2026, 8, 6), "Ivy Zhang", "Copper & Co", "Email", "Feedback on estimate",
     "Closed lost", "Close the lead", None),
]
for i, vals in enumerate(followups):
    r = 2 + i
    for c, v in enumerate(vals, start=1):
        fu.cell(row=r, column=c, value=v)
last_fu = 1 + len(followups)
box(fu, 2, last_fu, 1, 8, dates=(1, 8))
for r in range(2, last_fu + 1):
    for c in (4, 8):
        fu.cell(row=r, column=c).alignment = Alignment(horizontal="center")
fu.freeze_panes = "A2"
fu.auto_filter.ref = f"A1:H{last_fu}"
dv_list(fu, CHANNELS, "D2:D400")
dv_list(fu, ["Booked", "Proposal sent", "Waiting on client", "Closed won", "Closed lost",
             "No reply"], "F2:F400", error="Pick an outcome")
fu.conditional_formatting.add(
    f"H2:H{last_fu}",
    FormulaRule(formula=['AND($H2<>"",$H2<TODAY())'],
                fill=PatternFill("solid", fgColor="F8D7DA"),
                font=Font(name=FONT, bold=True, color="A02020")))
fu.conditional_formatting.add(
    f"H2:H{last_fu}",
    FormulaRule(formula=['AND($H2<>"",$H2>=TODAY(),$H2<=TODAY()+3)'],
                fill=PatternFill("solid", fgColor="FFF3CD"),
                font=Font(name=FONT, bold=True, color="997404")))

# ================================================================ DASHBOARD
db = sheet(wb, "DASHBOARD")
widths(db, {"A": 3, "B": 32, "C": 16, "D": 30, "E": 16, "F": 3,
            "G": 10, "H": 26, "I": 16})
db["B2"] = "CRM & PROJECT DASHBOARD"
db["B2"].font = Font(name=FONT, bold=True, size=18, color=NAVY)
db["B3"] = "Live formulas from PIPELINE, PROJECTS, TIMESHEET, DELIVERABLES and FOLLOW-UPS."
db["B3"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

PL = "'PIPELINE'"
PJ = "'PROJECTS'"
TS = "'TIMESHEET'"
DL = "'DELIVERABLES'"
FU = "'FOLLOW-UPS'"

kpi(db, 5, 2, "TOTAL PIPELINE VALUE", f"=SUM({PL}!$E:$E)")
kpi(db, 8, 2, "WEIGHTED PIPELINE", f"=SUM({PL}!$G:$G)")
kpi(db, 11, 2, "WIN RATE",
    f'=IF(COUNTIF({PL}!$D:$D,"Won")+COUNTIF({PL}!$D:$D,"Lost")=0,0,'
    f'COUNTIF({PL}!$D:$D,"Won")/(COUNTIF({PL}!$D:$D,"Won")+COUNTIF({PL}!$D:$D,"Lost")))',
    fmt=PCT)
kpi(db, 14, 2, "DEALS WON (#)", f'=COUNTIF({PL}!$D:$D,"Won")', fmt="#,##0")
kpi(db, 17, 2, "ACTIVE PROJECTS (#)", f'=COUNTIF({PJ}!$C:$C,"Active")', fmt="#,##0")
kpi(db, 20, 2, "HOURS LOGGED THIS MONTH",
    f'=SUMIFS({TS}!$D:$D,{TS}!$A:$A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1),'
    f'{TS}!$A:$A,"<"&DATE(YEAR(TODAY()),MONTH(TODAY())+1,1))', fmt="#,##0.0")

kpi(db, 5, 4, "UNBILLED VALUE", f'=SUMIF({TS}!$H:$H,"No",{TS}!$G:$G)')
kpi(db, 8, 4, "OVERDUE FOLLOW-UPS (#)",
    f'=COUNTIFS({FU}!$H$2:$H$40,">0",{FU}!$H$2:$H$40,"<"&TODAY())', fmt="#,##0")
kpi(db, 11, 4, "OPEN DEALS (#)",
    f'=SUMPRODUCT(({PL}!$D$2:$D$26<>"Won")*({PL}!$D$2:$D$26<>"Lost")*1)', fmt="#,##0")
kpi(db, 14, 4, "AVERAGE DEAL SIZE",
    f'=IF(COUNTIF({PL}!$E$2:$E$26,">0")=0,0,SUM({PL}!$E$2:$E$26)/'
    f'COUNTIF({PL}!$E$2:$E$26,">0"))')
kpi(db, 17, 4, "ACTIVE PROJECT VALUE",
    f'=SUMIF({PJ}!$C:$C,"Active",{PJ}!$I:$I)')
kpi(db, 20, 4, "OVERDUE DELIVERABLES (#)",
    f'=SUMPRODUCT(({DL}!$D$2:$D$20<>"")*({DL}!$D$2:$D$20<TODAY())*'
    f'({DL}!$E$2:$E$20<>"Approved")*({DL}!$E$2:$E$20<>"Rejected")*1)', fmt="#,##0")

# Pipeline by stage
band(db, 24, 2, 5, "PIPELINE VALUE BY STAGE (SUMIF)")
hdr(db, 25, ["Stage", "Deals", "Value", "Weighted"], start=2, fill=TEAL)
for i, stage in enumerate(STAGES):
    r = 26 + i
    db.cell(row=r, column=2, value=stage)
    db.cell(row=r, column=3, value=f'=COUNTIF({PL}!$D:$D,$B{r})')
    db.cell(row=r, column=4, value=f'=SUMIF({PL}!$D:$D,$B{r},{PL}!$E:$E)')
    db.cell(row=r, column=5, value=f'=SUMIF({PL}!$D:$D,$B{r},{PL}!$G:$G)')
box(db, 26, 32, 2, 5, money=(4, 5), ints=(3,))
for r in range(26, 33):
    db.cell(row=r, column=2).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
    db.cell(row=r, column=3).alignment = Alignment(horizontal="center")
status_cf(db, "B26:B32", [("Won", "D4EDDA", "1E7E34", True),
                          ("Lost", "F8D7DA", "A02020", True)])

# Hours & billing
band(db, 34, 2, 4, "HOURS & BILLING (TIMESHEET)")
hdr(db, 35, ["Metric", "Value", "Source"], start=2, fill=TEAL)
billing = [
    ("Total hours logged", f"=SUM({TS}!$D:$D)", "#,##0.0", "TIMESHEET column D"),
    ("Billable hours", f'=SUMIF({TS}!$E:$E,"Yes",{TS}!$D:$D)', "#,##0.0", "Billable = Yes"),
    ("Non-billable hours", f'=SUMIF({TS}!$E:$E,"No",{TS}!$D:$D)', "#,##0.0", "Billable = No"),
    ("Billable value", f"=SUM({TS}!$G:$G)", MONEY, "Hours x Rate"),
    ("Invoiced value", f'=SUMIF({TS}!$H:$H,"Yes",{TS}!$G:$G)', MONEY, "Invoiced? = Yes"),
    ("Unbilled value", f'=SUMIF({TS}!$H:$H,"No",{TS}!$G:$G)', MONEY, "Invoiced? = No"),
]
for i, (label, formula, fmt, source) in enumerate(billing):
    r = 36 + i
    db.cell(row=r, column=2, value=label)
    c = db.cell(row=r, column=3, value=formula)
    c.number_format = fmt
    db.cell(row=r, column=4, value=source)
box(db, 36, 41, 2, 4, zebra=True)
for r in range(36, 42):
    db.cell(row=r, column=2).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
    db.cell(row=r, column=3).alignment = Alignment(horizontal="right")
    db.cell(row=r, column=3).font = Font(name=FONT, bold=True, size=11, color=TEAL)
    db.cell(row=r, column=4).font = Font(name=FONT, size=10, color=GREY, italic=True)

# Top clients
band(db, 43, 2, 5, "TOP CLIENTS BY PROJECT VALUE")
hdr(db, 44, ["Client", "Projects", "Project value", "Share"], start=2, fill=TEAL)
for i in range(5):
    r = 45 + i
    db.cell(row=r, column=2, value=f"=VLOOKUP({i + 1},$G$5:$I$12,2,FALSE)")
    db.cell(row=r, column=3, value=f'=COUNTIF({PJ}!$B:$B,B{r})')
    db.cell(row=r, column=4, value=f"=VLOOKUP({i + 1},$G$5:$I$12,3,FALSE)")
    db.cell(row=r, column=5,
            value=f'=IF(SUM({PJ}!$I:$I)=0,0,D{r}/SUM({PJ}!$I:$I))')
box(db, 45, 49, 2, 5, money=(4,), ints=(3,))
for r in range(45, 50):
    db.cell(row=r, column=2).font = Font(name=FONT, bold=True, size=11, color="2B2D42")
    db.cell(row=r, column=3).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=5).number_format = PCT
    db.cell(row=r, column=5).alignment = Alignment(horizontal="center")

db["B51"] = "Nothing on this sheet is typed by hand - add rows to the log sheets and it updates."
db["B51"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

# Client ranking workings
clients = sorted({p[1] for p in projects})
db["G3"] = "CLIENT RANKINGS (auto)"
db["G3"].font = Font(name=FONT, bold=True, size=10, color=GREY)
hdr(db, 4, ["Rank", "Client", "Value"], start=7, fill=GREY)
for i, client in enumerate(clients):
    r = 5 + i
    db.cell(row=r, column=7,
            value=f"=SUMPRODUCT(($I$5:$I$12>I{r})*1)+COUNTIF($I$5:I{r},I{r})")
    db.cell(row=r, column=8, value=client)
    db.cell(row=r, column=9, value=f'=SUMIF({PJ}!$B:$B,H{r},{PJ}!$I:$I)')
box(db, 5, 12, 7, 9, money=(9,), zebra=False)
for r in range(5, 13):
    for c in (7, 8, 9):
        db.cell(row=r, column=c).font = Font(name=FONT, size=9, color=GREY)
    db.cell(row=r, column=7).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=9).alignment = Alignment(horizontal="right")

# ---------------------------------------------------------------- SAVE
wb._sheets = [wb["Start Here"], wb["PIPELINE"], wb["PROJECTS"], wb["TIMESHEET"],
              wb["DELIVERABLES"], wb["FOLLOW-UPS"], wb["DASHBOARD"]]
wb.active = 0
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Client_CRM_and_Project_Tracker.xlsx")
wb.save(out)
print("saved:", out)
