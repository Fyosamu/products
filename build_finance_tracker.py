# -*- coding: utf-8 -*-
"""Build: The Freelancer Finance Tracker 2026 (XLSX)"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from datetime import date, timedelta
import random

NAVY = "1F2A44"
TEAL = "0FA3B1"
LIGHT = "EAF4F4"
GOLD = "F4B942"
WHITE = "FFFFFF"
GREY = "8D99AE"

thin = Side(style="thin", color="D5DDE5")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(ws, row, cols, fill=NAVY):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color=WHITE, size=11, name="Calibri")
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

wb = openpyxl.Workbook()

# ---------------------------------------------------------------- INSTRUCTIONS
ins = wb.active
ins.title = "Start Here"
ins.sheet_view.showGridLines = False
ins.column_dimensions["A"].width = 3
ins.column_dimensions["B"].width = 100

title = ins["B2"]
title.value = "THE FREELANCER FINANCE TRACKER 2026"
title.font = Font(bold=True, size=20, color=NAVY)
ins["B3"].value = "Income  ·  Expenses  ·  Tax Reserve  ·  Profit Dashboard"
ins["B3"].font = Font(size=12, color=TEAL, italic=True)

steps = [
    "",
    "HOW TO USE THIS WORKBOOK (5 minutes to set up)",
    "",
    "1. Open the DASHBOARD sheet. Set your currency symbol in cell B3 (default is $).",
    "2. Log every payment you receive in the INCOME LOG sheet (client, project, amount, method).",
    "   Tip: USDT / BTC / PayPal / bank transfer all go here - just pick the method.",
    "3. Log every business expense in the EXPENSE LOG sheet.",
    "4. The TAX RESERVE sheet automatically calculates what you should set aside.",
    "5. Check the DASHBOARD weekly - it updates itself, no formulas to touch.",
    "",
    "RULES THAT KEEP THE NUMBERS CLEAN",
    "",
    "- Never delete rows. Mark cancelled income as 'Cancelled' in the Status column instead.",
    "- Use the drop-down lists (colored cells) so your totals keep working.",
    "- Enter amounts as plain numbers: type 250 not $250.",
    "- Work on the 'How to use' sheet first, then rename it or hide it if you like.",
    "",
    "THE 1-2-3 RULE OF FREELANCE MONEY",
    "",
    "1. Move your income into this tracker the same day it lands.",
    "2. Set aside 25-30% for tax IMMEDIATELY (the Tax Reserve sheet does the math).",
    "3. Pay yourself a fixed monthly 'salary' from what's left - never spend randomly.",
]
r = 5
for line in steps:
    c = ins.cell(row=r, column=2, value=line)
    if line.isupper() and len(line) > 3:
        c.font = Font(bold=True, size=12, color=TEAL)
    elif line and line[0].isdigit() and "." in line[:3]:
        c.font = Font(size=11, color="2B2D42")
    else:
        c.font = Font(size=11, color="2B2D42")
    r += 1

# ---------------------------------------------------------------- DASHBOARD
dash = wb.create_sheet("DASHBOARD")
dash.sheet_view.showGridLines = False
dash.column_dimensions["A"].width = 3
for col, w in zip("BCDEFG", [30, 16, 16, 16, 16, 16]):
    dash.column_dimensions[col].width = w

dash["B2"] = "FINANCE DASHBOARD"
dash["B2"].font = Font(bold=True, size=18, color=NAVY)
dash["B3"] = "Currency symbol:"
dash["B3"].font = Font(bold=True, size=10, color=GREY)
dash["C3"] = "$"
dash["C3"].font = Font(bold=True, size=12, color=TEAL)
dash["C3"].fill = PatternFill("solid", fgColor=LIGHT)
dash["C3"].border = border
dash["C3"].alignment = Alignment(horizontal="center")

kpis = [
    ("B5", "TOTAL INCOME", '=SUMIF(\'Income Log\'!I:I,"Received",\'Income Log\'!F:F)'),
    ("D5", "TOTAL EXPENSES", "=SUM('Expense Log'!E:E)"),
    ("B8", "NET PROFIT", "=B6-D6"),
    ("D8", "TAX TO SET ASIDE (25%)", "=MAX(B6-D6,0)*0.25"),
    ("B11", "TAKE-HOME (after tax reserve)", "=MAX(B6-D6,0)*0.75"),
    ("D11", "OUTSTANDING INVOICES", '=SUMIF(\'Income Log\'!I:I,"Pending",\'Income Log\'!F:F)'),
]
for anchor, label, formula in kpis:
    cell = dash[anchor]
    cell.value = label
    cell.font = Font(bold=True, size=10, color=WHITE)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = border
    # value cell = one row below, merged two columns
    col = anchor[0]
    row = int(anchor[1:])
    val_cell = dash.cell(row=row + 1, column=dash[anchor].column)
    val_cell.value = formula
    val_cell.font = Font(bold=True, size=20, color=TEAL)
    val_cell.fill = PatternFill("solid", fgColor=LIGHT)
    val_cell.alignment = Alignment(horizontal="center", vertical="center")
    val_cell.border = border
    val_cell.number_format = '"$"#,##0.00'
    dash.merge_cells(start_row=row, start_column=dash[anchor].column, end_row=row, end_column=dash[anchor].column + 1)
    dash.merge_cells(start_row=row + 1, start_column=dash[anchor].column, end_row=row + 1, end_column=dash[anchor].column + 1)
    dash.cell(row=row, column=dash[anchor].column + 1).border = border
    dash.cell(row=row + 1, column=dash[anchor].column + 1).border = border

# Monthly table
dash["B15"] = "INCOME VS EXPENSE BY MONTH"
dash["B15"].font = Font(bold=True, size=12, color=NAVY)
hdr = ["Month", "Income", "Expenses", "Net", "Tax 25%"]
for i, h in enumerate(hdr):
    dash.cell(row=16, column=2 + i, value=h)
style_header(dash, 16, 6)
for c in range(2, 7):
    dash.cell(row=16, column=c).fill = PatternFill("solid", fgColor=TEAL)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i, m in enumerate(months):
    r = 17 + i
    dash.cell(row=r, column=2, value=m + " 2026")
    dash.cell(row=r, column=3,
              value=f'=SUMPRODUCT((TEXT(\'Income Log\'!$A$2:$A$200,"mmm")="{m}")*(YEAR(\'Income Log\'!$A$2:$A$200)=2026)*(\'Income Log\'!$I$2:$I$200="Received")*\'Income Log\'!$F$2:$F$200)')
    dash.cell(row=r, column=4,
              value=f'=SUMPRODUCT((TEXT(\'Expense Log\'!$A$2:$A$200,"mmm")="{m}")*(YEAR(\'Expense Log\'!$A$2:$A$200)=2026)*\'Expense Log\'!$E$2:$E$200)')
    dash.cell(row=r, column=5, value=f"=C{r}-D{r}")
    dash.cell(row=r, column=6, value=f"=MAX(E{r},0)*0.25")
    for c in range(2, 7):
        cell = dash.cell(row=r, column=c)
        cell.border = border
        if c > 2:
            cell.number_format = '"$"#,##0.00'
        if i % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="F7FAFC")

dash.conditional_formatting.add(
    "E17:E28",
    CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))

# ---------------------------------------------------------------- INCOME LOG
inc = wb.create_sheet("Income Log")
headers = ["Date", "Client / Platform", "Project", "Category", "Currency",
           "Amount", "Fee", "Net Received", "Status", "Method", "Notes"]
widths = [12, 24, 26, 16, 10, 12, 10, 14, 12, 16, 30]
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    inc.cell(row=1, column=i, value=h)
    inc.column_dimensions[get_column_letter(i)].width = w
style_header(inc, 1, len(headers))

random.seed(7)
clients = [("Nova Studio", "Logo design"), ("Binance Blog", "SEO article"),
           ("Acme SaaS", "Landing page"), ("Loop Agency", "UI redesign"),
           ("CoinDesk", "Newsletter copy"), ("Pixelworks", "Social pack"),
           ("Orbit CRM", "Website dev")]
cats = ["Design", "Development", "Writing", "Marketing", "Consulting"]
methods = ["USDT (BEP20)", "USDT (TRC20)", "BTC", "PayPal", "Bank", "Wise"]
statuses = ["Received"] * 7 + ["Pending", "Cancelled"]

start = date(2026, 1, 6)
for n in range(24):
    r = 2 + n
    d = start + timedelta(days=n * 7 + random.randint(0, 3))
    cl, pr = clients[n % len(clients)]
    inc.cell(row=r, column=1, value=d).number_format = "yyyy-mm-dd"
    inc.cell(row=r, column=2, value=cl)
    inc.cell(row=r, column=3, value=pr)
    inc.cell(row=r, column=4, value=cats[n % len(cats)])
    inc.cell(row=r, column=5, value="USD")
    amt = random.choice([150, 250, 400, 600, 850, 1200])
    inc.cell(row=r, column=6, value=amt)
    inc.cell(row=r, column=7, value=round(amt * random.choice([0, 0.02, 0.05]), 2))
    inc.cell(row=r, column=8, value=f"=F{r}-G{r}")
    st = statuses[n % len(statuses)]
    inc.cell(row=r, column=9, value=st)
    inc.cell(row=r, column=10, value=methods[n % len(methods)])
    inc.cell(row=r, column=11, value="")

for r in range(2, 60):
    for c in range(1, len(headers) + 1):
        cell = inc.cell(row=r, column=c)
        cell.border = border
        if c in (6, 7, 8):
            cell.number_format = '#,##0.00'
        if r == 2:
            pass
    if r % 2 == 0:
        for c in range(1, len(headers) + 1):
            if not inc.cell(row=r, column=c).fill.fgColor.rgb or inc.cell(row=r, column=c).fill.patternType is None:
                inc.cell(row=r, column=c).fill = PatternFill("solid", fgColor="F7FAFC")

dv_status = DataValidation(type="list", formula1='"Received,Pending,Cancelled"', allow_blank=True)
dv_status.error = "Pick a status from the list"
inc.add_data_validation(dv_status)
dv_status.add("I2:I500")

dv_cat = DataValidation(type="list", formula1='"Design,Development,Writing,Marketing,Consulting,Other"', allow_blank=True)
inc.add_data_validation(dv_cat)
dv_cat.add("D2:D500")

dv_cur = DataValidation(type="list", formula1='"USD,EUR,GBP,USDT"', allow_blank=True)
inc.add_data_validation(dv_cur)
dv_cur.add("E2:E500")

inc.freeze_panes = "A2"
inc.auto_filter.ref = f"A1:K1"
inc.conditional_formatting.add("I2:I500", CellIsRule(operator="equal", formula=['"Received"'],
                              fill=PatternFill("solid", fgColor="D4EDDA"), font=Font(color="1E7E34")))
inc.conditional_formatting.add("I2:I500", CellIsRule(operator="equal", formula=['"Pending"'],
                              fill=PatternFill("solid", fgColor="FFF3CD"), font=Font(color="997404")))
inc.conditional_formatting.add("I2:I500", CellIsRule(operator="equal", formula=['"Cancelled"'],
                              fill=PatternFill("solid", fgColor="F8D7DA"), font=Font(color="A02020")))

# ---------------------------------------------------------------- EXPENSE LOG
exp = wb.create_sheet("Expense Log")
eheaders = ["Date", "Vendor", "Category", "Description", "Amount", "Payment Method", "Deductible?", "Notes"]
ewidths = [12, 22, 18, 30, 12, 16, 14, 28]
for i, (h, w) in enumerate(zip(eheaders, ewidths), start=1):
    exp.cell(row=1, column=i, value=h)
    exp.column_dimensions[get_column_letter(i)].width = w
style_header(exp, 1, len(eheaders))

vendors = [("Adobe", "Software", "Creative Cloud subscription"),
           ("Figma", "Software", "Professional plan"),
           ("Google Workspace", "Software", "Email + storage"),
           ("Upwork", "Fees", "Service fee"),
           ("Coworking Hub", "Office", "Day pass"),
           ("Internet Provider", "Office", "Monthly internet"),
           ("Canva", "Software", "Pro plan"),
           ("Freelancer Insurance", "Insurance", "Liability cover"),
           ("Online Course", "Education", "Skill course")]
pays = ["Card", "PayPal", "USDT (BEP20)", "Bank"]
for n in range(18):
    r = 2 + n
    d = date(2026, 1, 8) + timedelta(days=n * 11 + random.randint(0, 4))
    v, cat2, desc = vendors[n % len(vendors)]
    exp.cell(row=r, column=1, value=d).number_format = "yyyy-mm-dd"
    exp.cell(row=r, column=2, value=v)
    exp.cell(row=r, column=3, value=cat2)
    exp.cell(row=r, column=4, value=desc)
    exp.cell(row=r, column=5, value=random.choice([12, 29, 45, 60, 99, 150]))
    exp.cell(row=r, column=6, value=pays[n % len(pays)])
    exp.cell(row=r, column=7, value="Yes")
    exp.cell(row=r, column=8, value="")

for r in range(2, 60):
    for c in range(1, len(eheaders) + 1):
        cell = exp.cell(row=r, column=c)
        cell.border = border
        if c == 5:
            cell.number_format = '#,##0.00'
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="F7FAFC")

dv_ecat = DataValidation(type="list", formula1='"Software,Office,Fees,Marketing,Education,Insurance,Hardware,Other"', allow_blank=True)
exp.add_data_validation(dv_ecat)
dv_ecat.add("C2:C500")
dv_ded = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
exp.add_data_validation(dv_ded)
dv_ded.add("G2:G500")

exp.freeze_panes = "A2"
exp.auto_filter.ref = "A1:H1"

# ---------------------------------------------------------------- TAX RESERVE
tax = wb.create_sheet("Tax Reserve")
tax.sheet_view.showGridLines = False
tax.column_dimensions["A"].width = 3
for col, w in zip("BCDEF", [34, 18, 18, 18, 18]):
    tax.column_dimensions[col].width = w

tax["B2"] = "TAX RESERVE CALCULATOR"
tax["B2"].font = Font(bold=True, size=18, color=NAVY)
tax["B4"] = "Your tax rate (%):"
tax["B4"].font = Font(bold=True, size=11)
tax["C4"] = 25
tax["C4"].fill = PatternFill("solid", fgColor=LIGHT)
tax["C4"].border = border
tax["C4"].font = Font(bold=True, size=12, color=TEAL)
tax["C4"].alignment = Alignment(horizontal="center")

rows = [
    ("Annual income (received)", '=SUMIF(\'Income Log\'!I:I,"Received",\'Income Log\'!F:F)'),
    ("Annual deductible expenses", '=SUMIF(\'Expense Log\'!G:G,"Yes",\'Expense Log\'!E:E)'),
    ("Taxable profit", "=C6-C7"),
    ("You should set aside", "=MAX(C8,0)*(C4/100)"),
    ("Set aside per month", "=C9/12"),
    ("Set aside per week", "=C9/52"),
]
for i, (label, formula) in enumerate(rows):
    r = 6 + i
    tax.cell(row=r, column=2, value=label).font = Font(bold=(i >= 2), size=11, color="2B2D42")
    c = tax.cell(row=r, column=3, value=formula)
    c.number_format = '#,##0.00'
    c.border = border
    c.alignment = Alignment(horizontal="right")
    c.font = Font(bold=True, size=12, color=TEAL if i >= 2 else "2B2D42")
    if i >= 2:
        c.fill = PatternFill("solid", fgColor=LIGHT)
    tax.cell(row=r, column=2).border = border

tax["B13"] = "QUARTERLY PAYMENT CALENDAR - move this amount to a separate savings account"
tax["B13"].font = Font(bold=True, size=11, color=NAVY)
qhdr = ["Quarter", "Period", "Reserve to move"]
for i, h in enumerate(qhdr):
    tax.cell(row=14, column=2 + i, value=h)
for c in range(2, 5):
    cell = tax.cell(row=14, column=c)
    cell.font = Font(bold=True, color=WHITE)
    cell.fill = PatternFill("solid", fgColor=TEAL)
    cell.alignment = Alignment(horizontal="center")
    cell.border = border
quarters = [("Q1", "Jan - Mar"), ("Q2", "Apr - Jun"), ("Q3", "Jul - Sep"), ("Q4", "Oct - Dec")]
for i, (q, per) in enumerate(quarters):
    r = 15 + i
    tax.cell(row=r, column=2, value=q)
    tax.cell(row=r, column=3, value=per)
    tax.cell(row=r, column=4, value="=$C$9/4")
    for c in range(2, 5):
        cell = tax.cell(row=r, column=c)
        cell.border = border
        if c == 4:
            cell.number_format = '#,##0.00'
        if i % 2 == 0:
            cell.fill = PatternFill("solid", fgColor="F7FAFC")

# reorder sheets: Start Here first, then Dashboard
wb._sheets = [wb["Start Here"], wb["DASHBOARD"], wb["Income Log"], wb["Expense Log"], wb["Tax Reserve"]]
wb.active = 0

import os
os.makedirs(os.path.dirname(__file__), exist_ok=True)
out = os.path.join(os.path.dirname(__file__), "Freelancer_Finance_Tracker_2026.xlsx")
wb.save(out)
print("saved:", out)
