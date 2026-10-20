# -*- coding: utf-8 -*-
"""Build: The Ultimate Wedding Planner Spreadsheet 2026 (XLSX)"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from datetime import date, timedelta
import random

BLUSH = "D4849A"   # rose
CREAM = "FDF6F0"
DARK = "3B2F3A"
GREEN = "5B8C5A"
LIGHTG = "EAF3EA"
GOLD = "C9A227"

thin = Side(style="thin", color="E5D9D2")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def hdr(ws, row, cols, fill=BLUSH):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

wb = openpyxl.Workbook()

# ============================================================= WELCOME
w = wb.active
w.title = "Welcome"
w.sheet_view.showGridLines = False
w.column_dimensions["A"].width = 3
w.column_dimensions["B"].width = 100

w["B2"] = "THE ULTIMATE WEDDING PLANNER 2026"
w["B2"].font = Font(bold=True, size=20, color=DARK)
w["B3"] = "Budget  ·  Guests  ·  Vendors  ·  Timeline  ·  Seating"
w["B3"].font = Font(size=12, color=BLUSH, italic=True)

lines = [
    "",
    "SET UP IN 4 STEPS (about 10 minutes)",
    "",
    "1. BUDGET SHEET: set your total budget in cell C3, then adjust the category split — everything recalculates.",
    "2. GUEST LIST: add names as they come in. The budget automatically shows cost per guest.",
    "3. TIMELINE: change the wedding date on the Budget sheet and the 12-month countdown updates.",
    "4. VENDOR LIST: track quotes side by side before you book. Never pay without comparing three.",
    "",
    "SHEETS IN THIS WORKBOOK",
    "",
    "Budget       - total budget, category targets, actual spending, what's left",
    "Guest List   - RSVPs, meal choices, plus-ones, address and table assignment",
    "Vendors      - quotes, deposits, balances and payment dates in one place",
    "Timeline     - month-by-month checklist counting down to the wedding day",
    "Seating Plan - table by table, drag guests into seats and count heads",
    "",
    "TIPS FROM REAL WEDDINGS",
    "",
    "- Keep a 5% contingency. Something always changes; this is the line that saves the day.",
    "- Record EVERY verbal quote in the Vendor sheet the same day you hear it.",
    "- Pay deposits from one account only — it makes tracking the Budget sheet effortless.",
    "- Final guest count is usually due 2 weeks before the date — the Timeline reminds you.",
]
r = 5
for line in lines:
    c = w.cell(row=r, column=2, value=line)
    if line.isupper() and len(line) > 3:
        c.font = Font(bold=True, size=12, color=BLUSH)
    else:
        c.font = Font(size=11, color="3B2F3A")
    r += 1

# ============================================================= BUDGET
b = wb.create_sheet("Budget")
b.sheet_view.showGridLines = False
widths = {"A": 3, "B": 26, "C": 16, "D": 16, "E": 16, "F": 16, "G": 30}
for col, wd in widths.items():
    b.column_dimensions[col].width = wd

b["B2"] = "BUDGET OVERVIEW"
b["B2"].font = Font(bold=True, size=18, color=DARK)
b["B4"] = "Total budget:"
b["B4"].font = Font(bold=True, size=11)
b["C4"] = 15000
b["C4"].number_format = '"$"#,##0'
b["C4"].font = Font(bold=True, size=14, color=BLUSH)
b["C4"].fill = PatternFill("solid", fgColor=CREAM)
b["C4"].border = border
b["C4"].alignment = Alignment(horizontal="center")

b["E4"] = "Wedding date:"
b["E4"].font = Font(bold=True, size=11)
b["F4"] = date(2026, 9, 19)
b["F4"].number_format = "yyyy-mm-dd"
b["F4"].font = Font(bold=True, size=12, color=BLUSH)
b["F4"].fill = PatternFill("solid", fgColor=CREAM)
b["F4"].border = border
b["F4"].alignment = Alignment(horizontal="center")

# KPI strip
kpis = [
    ("B6", "TOTAL PLANNED", "=SUM(C11:C24)"),
    ("C6", "TOTAL PAID", "=SUM(D11:D24)"),
    ("D6", "STILL OWED", "=SUM(E11:E24)"),
    ("E6", "REMAINING BUDGET", "=C4-SUM(D11:D24)"),
]
b.merge_cells("B6:B6")
for anchor, label, formula in kpis:
    cell = b[anchor]
    cell.value = label
    cell.font = Font(bold=True, size=9, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=DARK)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = border
    vc = b.cell(row=7, column=cell.column)
    vc.value = formula
    vc.number_format = '"$"#,##0'
    vc.font = Font(bold=True, size=15, color=DARK)
    vc.fill = PatternFill("solid", fgColor=CREAM)
    vc.alignment = Alignment(horizontal="center", vertical="center")
    vc.border = border
b.row_dimensions[6].height = 28
b.row_dimensions[7].height = 30

b["B9"] = "CATEGORY BREAKDOWN"
b["B9"].font = Font(bold=True, size=12, color=DARK)
cats = [
    ("Venue & Catering", 4500, 4500),
    ("Photography & Video", 2200, 1400),
    ("Attire & Beauty", 1500, 900),
    ("Music & Entertainment", 900, 0),
    ("Flowers & Decor", 1300, 650),
    ("Cake & Desserts", 450, 0),
    ("Stationery & Invites", 350, 350),
    ("Transportation", 500, 0),
    ("Rings", 2000, 2000),
    ("Gifts & Favours", 400, 150),
    ("Officiant & Licence", 400, 400),
    ("Honeymoon", 3000, 800),
    ("Contingency (5%)", 1000, 0),
]
cols = ["Category", "Planned", "Paid", "Remaining", "% Used", "Notes"]
for i, h in enumerate(cols):
    b.cell(row=10, column=2 + i, value=h)
for c in range(2, 8):
    cell = b.cell(row=10, column=c)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=BLUSH)
    cell.alignment = Alignment(horizontal="center")
    cell.border = border

for i, (cat, planned, paid) in enumerate(cats):
    r = 11 + i
    b.cell(row=r, column=2, value=cat)
    b.cell(row=r, column=3, value=planned).number_format = '#,##0'
    b.cell(row=r, column=4, value=paid).number_format = '#,##0'
    b.cell(row=r, column=5, value=f"=C{r}-D{r}").number_format = '#,##0'
    b.cell(row=r, column=6, value=f"=IF(C{r}=0,0,D{r}/C{r})").number_format = '0%'
    b.cell(row=r, column=7, value="")
    for c in range(2, 8):
        cell = b.cell(row=r, column=c)
        cell.border = border
        if i % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="FBF7F4")

b.conditional_formatting.add("F11:F24", CellIsRule(operator="greaterThan", formula=["1"],
    fill=PatternFill("solid", fgColor="F8D7DA"), font=Font(color="A02020", bold=True)))
b.conditional_formatting.add("F11:F24", CellIsRule(operator="between", formula=["0.8", "1"],
    fill=PatternFill("solid", fgColor="FFF3CD")))

# per-guest
b["B26"] = "Cost per guest (paid ÷ confirmed guests):"
b["B26"].font = Font(bold=True, size=11, color=DARK)
b.merge_cells("B26:D26")
b["E26"] = '=IF(COUNTIF(\'Guest List\'!F:F,"Yes")=0,0,SUM(D11:D24)/COUNTIF(\'Guest List\'!F:F,"Yes"))'
b["E26"].number_format = '"$"#,##0.00'
b["E26"].font = Font(bold=True, size=13, color=BLUSH)
b["E26"].fill = PatternFill("solid", fgColor=CREAM)
b["E26"].border = border
b["E26"].alignment = Alignment(horizontal="center")

b["B28"] = "Days until the wedding:"
b["B28"].font = Font(bold=True, size=11, color=DARK)
b["C28"] = '=MAX(F4-TODAY(),0)'
b["C28"].font = Font(bold=True, size=14, color=GREEN)
b["C28"].fill = PatternFill("solid", fgColor=LIGHTG)
b["C28"].border = border
b["C28"].alignment = Alignment(horizontal="center")

# ============================================================= GUEST LIST
g = wb.create_sheet("Guest List")
gh = ["#", "Guest Name", "Side", "Party Size", "Address", "RSVP", "Meal Choice",
      "Dietary Needs", "Gift Received", "Table", "Thank-you Sent"]
gw = [5, 24, 14, 10, 30, 10, 16, 20, 14, 8, 14]
for i, (h, wd) in enumerate(zip(gh, gw), start=1):
    g.cell(row=1, column=i, value=h)
    g.column_dimensions[get_column_letter(i)].width = wd
hdr(g, 1, len(gh))

random.seed(11)
first = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "Lucas",
         "Mia", "James", "Harper", "Benjamin", "Ella", "Daniel", "Grace", "Henry", "Chloe", "Jack",
         "Lily", "Owen", "Zoe", "Samuel", "Nora", "Ryan", "Lily", "Nathan", "Hannah", "Julian",
         "Aria", "Leo", "Ruby", "Isaac", "Elena", "Aaron", "Stella", "Marcus", "Ivy", "Theo"]
last = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Moore", "Martin", "Garcia", "Lee"]
sides = ["Bride", "Groom", "Mutual"]
rsvp = ["Yes"] * 26 + ["No"] * 6 + ["Pending"] * 8
meals = ["Chicken", "Beef", "Vegetarian", "Vegan", "Fish"]
random.shuffle(rsvp)

for n in range(40):
    r = 2 + n
    g.cell(row=r, column=1, value=n + 1)
    g.cell(row=r, column=2, value=f"{first[n]} {random.choice(last)}")
    g.cell(row=r, column=3, value=sides[n % 3])
    g.cell(row=r, column=4, value=random.choice([1, 1, 1, 2, 2]))
    g.cell(row=r, column=5, value=f"{random.randint(1,999)} {random.choice(['Oak','Maple','Cedar','Pine'])} St, {random.choice(['Springfield','Riverton','Fairview'])}")
    g.cell(row=r, column=6, value=rsvp[n])
    g.cell(row=r, column=7, value=random.choice(meals))
    g.cell(row=r, column=8, value=random.choice(["", "", "", "Gluten-free", "Nut allergy", "No shellfish"]))
    g.cell(row=r, column=9, value=random.choice(["Yes", "No"]))
    g.cell(row=r, column=10, value=random.randint(1, 6) if rsvp[n] == "Yes" else "")
    g.cell(row=r, column=11, value="No")

for r in range(2, 101):
    for c in range(1, len(gh) + 1):
        cell = g.cell(row=r, column=c)
        cell.border = border
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="FBF7F4")

dv = DataValidation(type="list", formula1='"Yes,No,Pending"', allow_blank=True)
g.add_data_validation(dv); dv.add("F2:F500")
dv2 = DataValidation(type="list", formula1='"Bride,Groom,Mutual"', allow_blank=True)
g.add_data_validation(dv2); dv2.add("C2:C500")
dv3 = DataValidation(type="list", formula1='"Chicken,Beef,Fish,Vegetarian,Vegan,Kids meal"', allow_blank=True)
g.add_data_validation(dv3); dv3.add("G2:G500")
dv4 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
g.add_data_validation(dv4); dv4.add("I2:I500")
g.add_data_validation(dv4); dv4.add("K2:K500")

g.freeze_panes = "A2"
g.auto_filter.ref = f"A1:{get_column_letter(len(gh))}1"
g.conditional_formatting.add("F2:F500", CellIsRule(operator="equal", formula=['"Yes"'],
    fill=PatternFill("solid", fgColor="D4EDDA"), font=Font(color="1E7E34", bold=True)))
g.conditional_formatting.add("F2:F500", CellIsRule(operator="equal", formula=['"No"'],
    fill=PatternFill("solid", fgColor="F8D7DA"), font=Font(color="A02020")))
g.conditional_formatting.add("F2:F500", CellIsRule(operator="equal", formula=['"Pending"'],
    fill=PatternFill("solid", fgColor="FFF3CD")))

# summary
g["M1"] = "SUMMARY"
g["M1"].font = Font(bold=True, color="FFFFFF")
g["M1"].fill = PatternFill("solid", fgColor=DARK)
g["M1"].border = border
g["M2"] = "Invited";   g["N2"] = "=SUM(D2:D100)"
g["M3"] = "Confirmed"; g["N3"] = '=SUMIF(F:F,"Yes",D:D)'
g["M4"] = "Declined";  g["N4"] = '=SUMIF(F:F,"No",D:D)'
g["M5"] = "Awaiting";  g["N5"] = '=SUMIF(F:F,"Pending",D:D)'
g["M6"] = "Tables needed"; g["N6"] = '=ROUNDUP(COUNTIFS(J:J,">0")/8,0)'
for rr in range(2, 7):
    g.cell(row=rr, column=13).border = border
    g.cell(row=rr, column=13).font = Font(bold=True, color=DARK)
    cell = g.cell(row=rr, column=14)
    cell.font = Font(bold=True, color=BLUSH, size=12)
    cell.border = border
    cell.alignment = Alignment(horizontal="center")
g.column_dimensions["M"].width = 16
g.column_dimensions["N"].width = 10

# ============================================================= VENDORS
v = wb.create_sheet("Vendors")
vh = ["Service", "Vendor Name", "Quote 1", "Quote 2", "Quote 3", "Chosen Price",
      "Deposit Paid", "Balance Due", "Contact", "Phone / Email", "Booked?"]
vw = [20, 26, 12, 12, 12, 14, 13, 13, 20, 26, 10]
for i, (h, wd) in enumerate(zip(vh, vw), start=1):
    v.cell(row=1, column=i, value=h)
    v.column_dimensions[get_column_letter(i)].width = wd
hdr(v, 1, len(vh), fill=GREEN)

services = [
    ("Venue", 4500), ("Caterer", 3800), ("Photographer", 2200), ("Videographer", 1800),
    ("Florist", 1300), ("DJ / Band", 900), ("Baker (cake)", 450), ("Officiant", 400),
    ("Hair & Makeup", 600), ("Stationery", 350), ("Transport", 500), ("Rentals", 800),
]
for n, (svc, base) in enumerate(services):
    r = 2 + n
    q1 = base
    q2 = int(base * random.uniform(0.85, 1.25))
    q3 = int(base * random.uniform(0.9, 1.3))
    v.cell(row=r, column=1, value=svc)
    v.cell(row=r, column=2, value=f"{svc.split()[0]} & Co." if n % 3 else f"The {svc.split()[0]} House")
    v.cell(row=r, column=3, value=q1).number_format = '#,##0'
    v.cell(row=r, column=4, value=q2).number_format = '#,##0'
    v.cell(row=r, column=5, value=q3).number_format = '#,##0'
    chosen = min(q1, q2, q3)
    v.cell(row=r, column=6, value=chosen).number_format = '#,##0'
    dep = int(chosen * 0.3) if n % 2 == 0 else 0
    v.cell(row=r, column=7, value=dep).number_format = '#,##0'
    v.cell(row=r, column=8, value=f"=F{r}-G{r}").number_format = '#,##0'
    v.cell(row=r, column=9, value="")
    v.cell(row=r, column=10, value="")
    v.cell(row=r, column=11, value="Yes" if n % 2 == 0 else "No")

for r in range(2, 40):
    for c in range(1, len(vh) + 1):
        cell = v.cell(row=r, column=c)
        cell.border = border
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="F4FAF4")

dv5 = DataValidation(type="list", formula1='"Yes,No,Contacted"', allow_blank=True)
v.add_data_validation(dv5); dv5.add("K2:K200")
v.freeze_panes = "A2"
v.auto_filter.ref = "A1:K1"

# ============================================================= TIMELINE
t = wb.create_sheet("Timeline")
th = ["When", "Task", "Who", "Status", "Notes"]
tw = [22, 58, 16, 14, 30]
for i, (h, wd) in enumerate(zip(th, tw), start=1):
    t.cell(row=1, column=i, value=h)
    t.column_dimensions[get_column_letter(i)].width = wd
hdr(t, 1, len(th), fill=GOLD)

tasks = [
    ("12+ months out", "Set the overall budget and guest list draft", "Both", "Done"),
    ("12+ months out", "Choose wedding date and season", "Both", "Done"),
    ("11 months out", "Tour and book the venue (biggest item)", "Both", "Done"),
    ("10 months out", "Book photographer and videographer", "Both", "In progress"),
    ("9 months out", "Book caterer and schedule tasting", "Both", "In progress"),
    ("8 months out", "Choose wedding party and ask them formally", "Both", "Not started"),
    ("8 months out", "Start dress / suit shopping", "One", "Not started"),
    ("7 months out", "Book florist and send inspiration board", "One", "Not started"),
    ("6 months out", "Send save-the-dates", "One", "Not started"),
    ("6 months out", "Book officiant", "Both", "Not started"),
    ("5 months out", "Plan honeymoon and check passports", "Both", "Not started"),
    ("4 months out", "Order cake and book tasting", "One", "Not started"),
    ("4 months out", "Book DJ / band", "Both", "Not started"),
    ("3 months out", "Send invitations (8 weeks before)", "One", "Not started"),
    ("3 months out", "Order suits and book hair & makeup trial", "One", "Not started"),
    ("2 months out", "Apply for marriage licence", "Both", "Not started"),
    ("6 weeks out", "Finalise guest list and confirm numbers with venue", "Both", "Not started"),
    ("1 month out", "Confirm final counts and seating plan", "One", "Not started"),
    ("1 month out", "Pay remaining vendor balances", "Both", "Not started"),
    ("2 weeks out", "Final dress fitting", "One", "Not started"),
    ("1 week out", "Confirm timeline with all vendors", "Both", "Not started"),
    ("1 week out", "Prepare vendor tips and payments envelopes", "Both", "Not started"),
    ("3 days out", "Pack for honeymoon and delegate wedding-day tasks", "Both", "Not started"),
    ("Wedding week", "Rehearsal dinner and hand phone to bridesmaid", "Both", "Not started"),
    ("THE DAY", "Breathe. You did the work — now enjoy it.", "Both", "Not started"),
    ("1 week after", "Send thank-you notes and return rentals", "One", "Not started"),
    ("2 weeks after", "Final payment to venue, review vendors", "Both", "Not started"),
]
for n, (when, task, who, status) in enumerate(tasks):
    r = 2 + n
    t.cell(row=r, column=1, value=when)
    t.cell(row=r, column=2, value=task)
    t.cell(row=r, column=3, value=who)
    t.cell(row=r, column=4, value=status)
    t.cell(row=r, column=5, value="")

for r in range(2, 60):
    for c in range(1, len(th) + 1):
        cell = t.cell(row=r, column=c)
        cell.border = border
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="FDFBF7")

dv6 = DataValidation(type="list", formula1='"Not started,In progress,Done,Skipped"', allow_blank=True)
t.add_data_validation(dv6); dv6.add("D2:D300")
dv7 = DataValidation(type="list", formula1='"Both,One"', allow_blank=True)
t.add_data_validation(dv7); dv7.add("C2:C300")
t.freeze_panes = "A2"
t.conditional_formatting.add("D2:D300", CellIsRule(operator="equal", formula=['"Done"'],
    fill=PatternFill("solid", fgColor="D4EDDA"), font=Font(color="1E7E34", bold=True)))
t.conditional_formatting.add("D2:D300", CellIsRule(operator="equal", formula=['"In progress"'],
    fill=PatternFill("solid", fgColor="FFF3CD"), font=Font(color="997404")))

# ============================================================= SEATING
s = wb.create_sheet("Seating Plan")
sh = ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6", "Unassigned"]
for i, h in enumerate(sh, start=1):
    s.cell(row=1, column=i, value=h)
    s.column_dimensions[get_column_letter(i)].width = 22
hdr(s, 1, len(sh), fill=DARK)
guests_by_side = [f"{first[i]} {random.choice(last)}" for i in range(34)]
for r in range(2, 12):
    for c in range(1, len(sh) + 1):
        cell = s.cell(row=r, column=c)
        cell.border = border
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="FBF7F4")
idx = 0
for c in range(1, 7):
    for r in range(2, 7):
        if idx < len(guests_by_side):
            s.cell(row=r, column=c, value=guests_by_side[idx])
            idx += 1
while idx < len(guests_by_side):
    s.cell(row=2 + (idx % 10), column=7, value=guests_by_side[idx])
    idx += 1
s["A14"] = "Tip: copy names from the Guest List sheet (only guests marked 'Yes') and paste into your table columns."
s["A14"].font = Font(italic=True, color="8D99AE")

# order
wb._sheets = [wb["Welcome"], wb["Budget"], wb["Guest List"], wb["Vendors"], wb["Timeline"], wb["Seating Plan"]]
wb.active = 0

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ultimate_Wedding_Planner_2026.xlsx")
wb.save(out)
print("saved:", out)
