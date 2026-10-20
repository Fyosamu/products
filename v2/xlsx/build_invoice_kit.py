# -*- coding: utf-8 -*-
"""Build: Client Invoice & Quote Kit 2026 (XLSX)"""
import os, random
from datetime import date, timedelta

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule

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


def kv(ws, row, label, value, val_fmt=None, editable=False):
    """Label in column B, value in column C (form block helper)."""
    lc = ws.cell(row=row, column=2, value=label)
    lc.font = Font(name=FONT, bold=True, size=11, color=GREY)
    lc.border = border
    vc = ws.cell(row=row, column=3, value=value)
    vc.font = Font(name=FONT, size=11, color="2B2D42")
    vc.border = border
    vc.alignment = Alignment(horizontal="left", vertical="center")
    if editable:
        vc.fill = PatternFill("solid", fgColor=LIGHT)
    if val_fmt:
        vc.number_format = val_fmt
    return vc


def kpi(ws, row, col, label, formula, fmt=MONEY):
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


def money_col(ws, col, r1, r2):
    for r in range(r1, r2 + 1):
        ws.cell(row=r, column=col).number_format = MONEY
        ws.cell(row=r, column=col).alignment = Alignment(horizontal="right")


# ----------------------------------------------------------------- WORKBOOK
wb = openpyxl.Workbook()

# ================================================================= START HERE
ins = wb.active
ins.title = "Start Here"
ins.sheet_view.showGridLines = False
start_here(
    ins,
    "CLIENT INVOICE & QUOTE KIT 2026",
    "Invoice  ·  Quote  ·  Payment Tracking  ·  Client Ledger  ·  Live Dashboard",
    [
        "",
        "HOW TO USE THIS WORKBOOK (5 minutes to set up)",
        "",
        "1. Open INVOICE MAKER and replace the business details with your own name, address, email.",
        "   Keep the crypto line if you accept it: Receive crypto: USDT on BNB Smart Chain (BEP-20).",
        "2. Fill the BILL TO block, then type your line items. Amount = Qty x Rate calculates itself.",
        "3. Set Discount %, Tax % and the payment terms - TOTAL DUE updates instantly.",
        "4. Save the sheet as PDF (File > Save As > PDF) and send it to your client.",
        "5. Log every invoice you send in PAYMENT TRACKER - that sheet feeds the whole DASHBOARD.",
        "6. Add every client to CLIENT LEDGER; invoiced, paid and balance fill in by formula.",
        "7. Use QUOTE MAKER before the work starts and move Status from Draft to Sent to Accepted.",
        "",
        "RULES THAT KEEP IT CLEAN",
        "",
        "- Never delete rows in PAYMENT TRACKER - set Status to Cancelled instead.",
        "- Use the drop-down lists (Method, Status, Terms) so the totals keep working.",
        "- Enter amounts as plain numbers: type 2500 not $2500.",
        "- Invoice numbers must be unique; dates use dd-mmm-yyyy, e.g. 15-Sep-2026.",
        "- Mark an invoice Paid the day the money lands - Overdue is worked out from the due date.",
        "- The DASHBOARD reads TODAY(), so open it fresh before you chase anyone.",
        "",
        "GET PAID FASTER",
        "",
        "- Send the invoice within 24 hours of finishing the work - never wait for month end.",
        "- Use short terms (Net 7 or Net 14) and repeat the due date in your follow-up email.",
        "- Crypto clients can pay USDT on BNB Smart Chain (BEP-20): low fees, settles in minutes.",
    ],
)

# ============================================================= INVOICE MAKER
inv = sheet(wb, "INVOICE MAKER")
widths(inv, {"A": 3, "B": 26, "C": 36, "D": 36, "E": 9, "F": 15, "G": 17, "H": 14})

inv["B2"] = "INVOICE"
inv["B2"].font = Font(name=FONT, bold=True, size=20, color=NAVY)
inv["B3"] = "Nova Studio Creative"
inv["B3"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

for r, (lab, val, fmt) in enumerate([
    ("Invoice #", "INV-2026-001", None),
    ("Issue date", date(2026, 9, 15), DATEF),
    ("Due date", "=G3+14", DATEF),
    ("Terms", "Net 14", None),
], start=2):
    lc = inv.cell(row=r, column=6, value=lab)
    lc.font = Font(name=FONT, bold=True, size=10, color=GREY)
    lc.alignment = Alignment(horizontal="right")
    lc.border = border
    vc = inv.cell(row=r, column=7, value=val)
    vc.font = Font(name=FONT, bold=True, size=11, color=NAVY)
    vc.fill = PatternFill("solid", fgColor=LIGHT)
    vc.border = border
    vc.alignment = Alignment(horizontal="center")
    if fmt:
        vc.number_format = fmt

band(inv, 7, 2, 3, "FROM - YOUR BUSINESS")
kv(inv, 8, "Business name", "Nova Studio Creative", editable=True)
kv(inv, 9, "Address", "12 Harbour Lane, Austin TX 78701", editable=True)
kv(inv, 10, "Email", "billing@novastudio.co", editable=True)
kv(inv, 11, "Phone", "+1 512 555 0148", editable=True)
kv(inv, 12, "Receive crypto", "USDT on BNB Smart Chain (BEP-20)", editable=True)

band(inv, 14, 2, 3, "BILL TO")
kv(inv, 15, "Client / company", "Acme SaaS Inc.", editable=True)
kv(inv, 16, "Billing address", "88 Market Street, Denver CO 80202", editable=True)
kv(inv, 17, "Email", "ap@acmesaas.com", editable=True)

inv["B19"] = "LINE ITEMS"
inv["B19"].font = Font(name=FONT, bold=True, size=12, color=TEAL)
hdr(inv, 19, ["Description", "Qty", "Rate", "Amount"], start=4)
for i in range(10):
    r = 20 + i
    inv.cell(row=r, column=5, value=None)
    inv.cell(row=r, column=7, value=f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})')
box(inv, 20, 29, 4, 7, money=(6, 7), ints=(5,))
for r in range(20, 30):
    inv.cell(row=r, column=4).alignment = Alignment(horizontal="left", vertical="center")
    inv.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    inv.cell(row=r, column=6).alignment = Alignment(horizontal="right")
    inv.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    inv.cell(row=r, column=5).fill = PatternFill("solid", fgColor=LIGHT)
    inv.cell(row=r, column=6).fill = PatternFill("solid", fgColor=LIGHT)
    inv.cell(row=r, column=4).fill = PatternFill("solid", fgColor=LIGHT)

totals = [
    ("Subtotal", "=SUM(G20:G29)", MONEY, False),
    ("Discount %", 0.05, PCT, True),
    ("Discount", "=G31*G32", MONEY, False),
    ("Tax %", 0.08, PCT, True),
    ("Tax", "=(G31-G33)*G34", MONEY, False),
    ("TOTAL DUE", "=G31-G33+G35", MONEY, "big"),
]
for i, (lab, val, fmt, kind) in enumerate(totals):
    r = 31 + i
    lc = inv.cell(row=r, column=6, value=lab)
    lc.alignment = Alignment(horizontal="right", vertical="center")
    lc.font = Font(name=FONT, bold=True, size=11, color=GREY if kind is not True else NAVY)
    lc.border = border
    vc = inv.cell(row=r, column=7, value=val)
    vc.number_format = fmt
    vc.alignment = Alignment(horizontal="right", vertical="center")
    vc.border = border
    if kind is True:
        vc.fill = PatternFill("solid", fgColor=LIGHT)
        vc.font = Font(name=FONT, bold=True, size=11, color=TEAL)
        lc.fill = PatternFill("solid", fgColor=BAND)
    elif kind == "big":
        vc.fill = PatternFill("solid", fgColor=NAVY)
        vc.font = Font(name=FONT, bold=True, size=14, color=WHITE)
        lc.fill = PatternFill("solid", fgColor=NAVY)
        lc.font = Font(name=FONT, bold=True, size=11, color=WHITE)
        inv.row_dimensions[r].height = 26
    else:
        vc.font = Font(name=FONT, size=11, color="2B2D42")

band(inv, 38, 2, 3, "PAYMENT TERMS")
kv(inv, 39, "Terms", "Net 14 - 50% deposit for new clients", editable=True)
kv(inv, 40, "Due date", "=G4", DATEF, editable=False)
kv(inv, 41, "Pay by bank", "Chase 4471 / routing 021000021", editable=True)
kv(inv, 42, "Pay by PayPal", "paypal.me/novastudio", editable=True)
kv(inv, 43, "Pay in crypto", "USDT BEP-20 wallet 0x7f4c...a91b", editable=True)
kv(inv, 44, "Note to client", "Thank you for your business!", editable=True)

dv_terms = DataValidation(
    type="list", formula1='"On receipt,Net 7,Net 14,Net 30,Net 45,50% deposit"', allow_blank=True
)
dv_terms.error = "Pick payment terms from the list"
inv.add_data_validation(dv_terms)
dv_terms.add("G5")

# ============================================================== QUOTE MAKER
qt = sheet(wb, "QUOTE MAKER")
widths(qt, {"A": 3, "B": 26, "C": 36, "D": 36, "E": 9, "F": 15, "G": 17, "H": 14})

qt["B2"] = "QUOTE"
qt["B2"].font = Font(name=FONT, bold=True, size=20, color=NAVY)
qt["B3"] = "Nova Studio Creative - valid for 30 days"
qt["B3"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

for r, (lab, val, fmt) in enumerate([
    ("Quote #", "QUO-2026-014", None),
    ("Issue date", date(2026, 9, 10), DATEF),
    ("Valid until", "=G3+30", DATEF),
    ("Status", "Draft", None),
], start=2):
    lc = qt.cell(row=r, column=6, value=lab)
    lc.font = Font(name=FONT, bold=True, size=10, color=GREY)
    lc.alignment = Alignment(horizontal="right")
    lc.border = border
    vc = qt.cell(row=r, column=7, value=val)
    vc.font = Font(name=FONT, bold=True, size=11, color=NAVY)
    vc.fill = PatternFill("solid", fgColor=LIGHT)
    vc.border = border
    vc.alignment = Alignment(horizontal="center")
    if fmt:
        vc.number_format = fmt

band(qt, 7, 2, 3, "FROM - YOUR BUSINESS")
kv(qt, 8, "Business name", "Nova Studio Creative", editable=True)
kv(qt, 9, "Address", "12 Harbour Lane, Austin TX 78701", editable=True)
kv(qt, 10, "Email", "billing@novastudio.co", editable=True)
kv(qt, 11, "Phone", "+1 512 555 0148", editable=True)
kv(qt, 12, "Receive crypto", "USDT on BNB Smart Chain (BEP-20)", editable=True)

band(qt, 14, 2, 3, "QUOTE FOR")
kv(qt, 15, "Client / company", "Harbor Labs", editable=True)
kv(qt, 16, "Contact address", "5 Pier Road, Seattle WA 98101", editable=True)
kv(qt, 17, "Email", "hello@harborlabs.io", editable=True)

qt["B19"] = "LINE ITEMS"
qt["B19"].font = Font(name=FONT, bold=True, size=12, color=TEAL)
hdr(qt, 19, ["Description", "Qty", "Rate", "Amount"], start=4)
for i in range(10):
    r = 20 + i
    qt.cell(row=r, column=7, value=f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})')
box(qt, 20, 29, 4, 7, money=(6, 7), ints=(5,))
for r in range(20, 30):
    qt.cell(row=r, column=4).alignment = Alignment(horizontal="left", vertical="center")
    qt.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    qt.cell(row=r, column=6).alignment = Alignment(horizontal="right")
    qt.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    for c in (4, 5, 6):
        qt.cell(row=r, column=c).fill = PatternFill("solid", fgColor=LIGHT)

qtotals = [
    ("Subtotal", "=SUM(G20:G29)", MONEY, False),
    ("Discount %", 0.05, PCT, True),
    ("Discount", "=G31*G32", MONEY, False),
    ("Tax %", 0.08, PCT, True),
    ("Tax", "=(G31-G33)*G34", MONEY, False),
    ("QUOTE TOTAL", "=G31-G33+G35", MONEY, "big"),
]
for i, (lab, val, fmt, kind) in enumerate(qtotals):
    r = 31 + i
    lc = qt.cell(row=r, column=6, value=lab)
    lc.alignment = Alignment(horizontal="right", vertical="center")
    lc.font = Font(name=FONT, bold=True, size=11, color=GREY if kind is not True else NAVY)
    lc.border = border
    vc = qt.cell(row=r, column=7, value=val)
    vc.number_format = fmt
    vc.alignment = Alignment(horizontal="right", vertical="center")
    vc.border = border
    if kind is True:
        vc.fill = PatternFill("solid", fgColor=LIGHT)
        vc.font = Font(name=FONT, bold=True, size=11, color=TEAL)
        lc.fill = PatternFill("solid", fgColor=BAND)
    elif kind == "big":
        vc.fill = PatternFill("solid", fgColor=NAVY)
        vc.font = Font(name=FONT, bold=True, size=14, color=WHITE)
        lc.fill = PatternFill("solid", fgColor=NAVY)
        lc.font = Font(name=FONT, bold=True, size=11, color=WHITE)
        qt.row_dimensions[r].height = 26
    else:
        vc.font = Font(name=FONT, size=11, color="2B2D42")

band(qt, 38, 2, 3, "SCOPE & TERMS")
kv(qt, 39, "Lead time", "Start within 10 working days", editable=True)
kv(qt, 40, "Valid until", "=G4", DATEF, editable=False)
kv(qt, 41, "Payment terms", "50% up front, 50% on delivery", editable=True)
kv(qt, 42, "Includes", "2 revision rounds, source files", editable=True)
kv(qt, 43, "Excludes", "Stock assets, paid plugins", editable=True)
kv(qt, 44, "Note to client", "Questions? Just reply to this quote.", editable=True)

dv_qstatus = DataValidation(
    type="list", formula1='"Draft,Sent,Viewed,Accepted,Declined"', allow_blank=True
)
dv_qstatus.error = "Pick a status from the list"
qt.add_data_validation(dv_qstatus)
dv_qstatus.add("G5")
for op, fill, fc in [
    ("Accepted", "D4EDDA", "1E7E34"),
    ("Declined", "F8D7DA", "A02020"),
    ("Sent", "FFF3CD", "997404"),
    ("Viewed", "FFF3CD", "997404"),
    ("Draft", "E2E3E5", "6C757D"),
]:
    qt.conditional_formatting.add(
        "G5",
        CellIsRule(operator="equal", formula=[f'"{op}"'],
                   fill=PatternFill("solid", fgColor=fill), font=Font(name=FONT, bold=True, color=fc)),
    )

# ========================================================== PAYMENT TRACKER
pt = sheet(wb, "PAYMENT TRACKER")
p_headers = ["Date", "Invoice #", "Client", "Amount", "Due date", "Method",
             "Status", "Days late", "Notes"]
p_widths = [13, 15, 20, 14, 13, 15, 13, 11, 34]
for i, (h, w) in enumerate(zip(p_headers, p_widths), start=1):
    pt.cell(row=1, column=i, value=h)
    pt.column_dimensions[get_column_letter(i)].width = w
hdr(pt, 1, p_headers)

pt_clients = ["Acme SaaS", "Loop Agency", "Orbit CRM", "Pixelworks",
              "Harbor Labs", "Bluebird Retail", "Zenith Fitness", "Nova Education"]
methods = ["Bank", "PayPal", "Card", "USDT-BEP20", "Cash"]
amounts = [450, 650, 900, 1100, 1500, 1850, 2400, 3200, 4800]
notes_cycle = ["Retainer", "", "", "Part of 3-phase project", "", "Rush job",
               "", "Balance after deposit", "", "Change request billed", "", "Monthly retainer",
               "", "", "Second phase", "", "Add-on scope", "", "", "Final milestone",
               "", "Discovery workshop", "", ""]

past_status = ["Paid", "Paid", "Overdue", "Paid", "Partial", "Paid", "Overdue", "Cancelled",
               "Paid", "Paid", "Partial", "Paid", "Overdue", "Paid", "Paid", "Paid",
               "Paid", "Partial", "Paid", "Overdue"]
future_status = ["Due", "Paid", "Due", "Due", "Partial"]

random.seed(21)
rows = []
pi = fi = 0
for n in range(24):
    d = date(2026, 1, 9) + timedelta(days=n * 11 + random.randint(0, 4))
    terms = random.choice([7, 14, 30])
    due = d + timedelta(days=terms)
    if due < TODAY:
        st = past_status[pi % len(past_status)]
        pi += 1
    else:
        st = future_status[fi % len(future_status)]
        fi += 1
    rows.append([
        d, f"INV-2026-{n + 1:03d}", pt_clients[n % len(pt_clients)],
        random.choice(amounts), due, methods[n % len(methods)], st,
        None, notes_cycle[n % len(notes_cycle)],
    ])

for n, rowvals in enumerate(rows):
    r = 2 + n
    for c, v in enumerate(rowvals, start=1):
        if v is None:
            continue
        pt.cell(row=r, column=c, value=v)
    pt.cell(row=r, column=8,
            value=f'=IF(OR($G{r}="Paid",$G{r}="Cancelled"),"",MAX(0,TODAY()-$E{r}))')

last_pt = 25  # header + 24 rows
box(pt, 2, last_pt, 1, 9, money=(4,), dates=(1, 5), ints=(8,))
for r in range(2, last_pt + 1):
    pt.cell(row=r, column=6).alignment = Alignment(horizontal="center")
    pt.cell(row=r, column=7).alignment = Alignment(horizontal="center")
    pt.cell(row=r, column=8).alignment = Alignment(horizontal="center")
pt.freeze_panes = "A2"
pt.auto_filter.ref = f"A1:I{last_pt}"

dv_method = DataValidation(type="list", formula1='"Bank,PayPal,Cash,Card,USDT-BEP20"',
                           allow_blank=True)
dv_method.error = "Pick a payment method"
pt.add_data_validation(dv_method)
dv_method.add("F2:F400")

dv_status = DataValidation(type="list", formula1='"Paid,Partial,Due,Overdue,Cancelled"',
                           allow_blank=True)
dv_status.error = "Pick a status from the list"
pt.add_data_validation(dv_status)
dv_status.add("G2:G400")

dv_client = DataValidation(
    type="list",
    formula1='"Acme SaaS,Loop Agency,Orbit CRM,Pixelworks,Harbor Labs,Bluebird Retail,Zenith Fitness,Nova Education"',
    allow_blank=True)
dv_client.error = "Pick a client from the list"
pt.add_data_validation(dv_client)
dv_client.add("C2:C400")

for op, fill, fc, bold in [
    ("Paid", "D4EDDA", "1E7E34", False),
    ("Overdue", "F8D7DA", "A02020", True),
    ("Partial", "FFF3CD", "997404", False),
    ("Due", "FFF3CD", "997404", False),
    ("Cancelled", "E2E3E5", "6C757D", False),
]:
    pt.conditional_formatting.add(
        "G2:G400",
        CellIsRule(operator="equal", formula=[f'"{op}"'],
                   fill=PatternFill("solid", fgColor=fill),
                   font=Font(name=FONT, color=fc, bold=bold)))
pt.conditional_formatting.add(
    "H2:H400",
    FormulaRule(formula=["AND(ISNUMBER($H2),$H2>0)"],
                font=Font(name=FONT, color="A02020", bold=True),
                fill=PatternFill("solid", fgColor="F8D7DA")))

# ============================================================ CLIENT LEDGER
cl = sheet(wb, "CLIENT LEDGER")
c_headers = ["Client", "Contact", "Email", "Hourly rate", "Invoiced", "Paid",
             "Balance", "Last invoice date", "Status"]
c_widths = [20, 16, 28, 13, 15, 15, 15, 17, 14]
for i, (h, w) in enumerate(zip(c_headers, c_widths), start=1):
    cl.cell(row=1, column=i, value=h)
    cl.column_dimensions[get_column_letter(i)].width = w
hdr(cl, 1, c_headers)

ledger_rows = [
    ("Acme SaaS", "Dana Reyes", "ap@acmesaas.com", 95),
    ("Loop Agency", "Marcus Hill", "accounts@loopagency.co", 110),
    ("Orbit CRM", "Priya Nair", "priya@orbitcrm.io", 105),
    ("Pixelworks", "Tom Becker", "tom@pixelworks.design", 85),
    ("Harbor Labs", "Elena Voss", "hello@harborlabs.io", 120),
    ("Bluebird Retail", "Sam Okafor", "sam@bluebirdretail.com", 90),
    ("Zenith Fitness", "Chris Lang", "chris@zenithfit.app", 80),
    ("Nova Education", "Aisha Karim", "aisha@novaedu.org", 95),
]
for n, (client, contact, email, rate) in enumerate(ledger_rows):
    r = 2 + n
    inv_dates = [row[0] for row in rows if row[2] == client]
    last_inv = max(inv_dates) if inv_dates else None
    cl.cell(row=r, column=1, value=client)
    cl.cell(row=r, column=2, value=contact)
    cl.cell(row=r, column=3, value=email)
    cl.cell(row=r, column=4, value=rate)
    cl.cell(row=r, column=5, value=f"=SUMIF('PAYMENT TRACKER'!$C:$C,$A{r},'PAYMENT TRACKER'!$D:$D)")
    cl.cell(row=r, column=6,
            value=f"=SUMIFS('PAYMENT TRACKER'!$D:$D,'PAYMENT TRACKER'!$C:$C,$A{r},"
                  f"'PAYMENT TRACKER'!$G:$G,\"Paid\")")
    cl.cell(row=r, column=7, value=f"=E{r}-F{r}")
    cl.cell(row=r, column=8, value=last_inv)
    cl.cell(row=r, column=9,
            value=f'=IF(E{r}=0,"No invoices",IF(G{r}<=0,"Settled",'
                  f"IF(COUNTIFS('PAYMENT TRACKER'!$C:$C,$A{r},'PAYMENT TRACKER'!$G:$G,\"Overdue\")>0,"
                  f'"Overdue","Open")))')
last_cl = 1 + len(ledger_rows)
box(cl, 2, last_cl, 1, 9, money=(4, 5, 6, 7), dates=(8,))
for r in range(2, last_cl + 1):
    cl.cell(row=r, column=4).number_format = MONEY
    cl.cell(row=r, column=9).alignment = Alignment(horizontal="center")
cl.freeze_panes = "A2"
cl.auto_filter.ref = f"A1:I{last_cl}"

dv_rate = DataValidation(type="decimal", operator="between", formula1="1", formula2="1000",
                         allow_blank=True)
cl.add_data_validation(dv_rate)
dv_rate.add("D2:D100")

for op, fill, fc in [
    ("Settled", "D4EDDA", "1E7E34"),
    ("Overdue", "F8D7DA", "A02020"),
    ("Open", "FFF3CD", "997404"),
    ("No invoices", "E2E3E5", "6C757D"),
]:
    cl.conditional_formatting.add(
        "I2:I100",
        CellIsRule(operator="equal", formula=[f'"{op}"'],
                   fill=PatternFill("solid", fgColor=fill), font=Font(name=FONT, color=fc)))

# ================================================================ DASHBOARD
db = sheet(wb, "DASHBOARD")
widths(db, {"A": 3, "B": 30, "C": 17, "D": 30, "E": 17, "F": 10, "G": 26, "H": 16})
db["B2"] = "INVOICE KIT DASHBOARD"
db["B2"].font = Font(name=FONT, bold=True, size=18, color=NAVY)
db["B3"] = "Live formulas only - reads PAYMENT TRACKER and CLIENT LEDGER. Nothing to refresh."
db["B3"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

PT = "'PAYMENT TRACKER'"
CLG = "'CLIENT LEDGER'"

kpi(db, 5, 2, "TOTAL INVOICED", f"=SUM({PT}!$D:$D)")
kpi(db, 8, 2, "TOTAL COLLECTED", f'=SUMIF({PT}!$G:$G,"Paid",{PT}!$D:$D)')
kpi(db, 11, 2, "OUTSTANDING",
    f'=SUMIF({PT}!$G:$G,"Due",{PT}!$D:$D)+SUMIF({PT}!$G:$G,"Overdue",{PT}!$D:$D)'
    f'+SUMIF({PT}!$G:$G,"Partial",{PT}!$D:$D)')
kpi(db, 14, 2, "OVERDUE VALUE", f'=SUMIF({PT}!$G:$G,"Overdue",{PT}!$D:$D)')
kpi(db, 17, 2, "AVG DAYS TO PAY (issue to due)",
    f'=IF(COUNTIF({PT}!$G$2:$G$25,"Paid")=0,0,SUMPRODUCT(({PT}!$G$2:$G$25="Paid")'
    f'*({PT}!$E$2:$E$25-{PT}!$A$2:$A$25))/COUNTIF({PT}!$G$2:$G$25,"Paid"))', fmt="0.0")
kpi(db, 20, 2, "AVERAGE INVOICE VALUE",
    f'=IF(COUNTIF({PT}!$D$2:$D$25,">0")=0,0,SUM({PT}!$D$2:$D$25)/COUNTIF({PT}!$D$2:$D$25,">0"))')

kpi(db, 5, 4, "COLLECTION RATE", "=IF(B6=0,0,B9/B6)", fmt=PCT)
kpi(db, 8, 4, "PAID INVOICES (#)", f'=COUNTIF({PT}!$G:$G,"Paid")', fmt="#,##0")
kpi(db, 11, 4, "OVERDUE INVOICES (#)", f'=COUNTIF({PT}!$G:$G,"Overdue")', fmt="#,##0")
kpi(db, 14, 4, "ACTIVE CLIENTS",
    f'=SUMPRODUCT(({CLG}!$A$2:$A$9<>"")*1)', fmt="#,##0")
kpi(db, 17, 4, "CANCELLED VALUE", f'=SUMIF({PT}!$G:$G,"Cancelled",{PT}!$D:$D)')

# Top 5 clients
band(db, 24, 2, 5, "TOP 5 CLIENTS BY REVENUE")
hdr(db, 25, ["Client", "Revenue", "Share of revenue", "Invoices"], start=2, fill=TEAL)
for i in range(5):
    r = 26 + i
    k = i + 1
    db.cell(row=r, column=2, value=f"=VLOOKUP({k},$F$46:$H$53,2,FALSE)")
    db.cell(row=r, column=3, value=f"=VLOOKUP({k},$F$46:$H$53,3,FALSE)")
    db.cell(row=r, column=4, value=f"=IF($B$6=0,0,C{r}/$B$6)")
    db.cell(row=r, column=5,
            value=f"=COUNTIF({PT}!$C:$C,B{r})")
box(db, 26, 30, 2, 5, money=(3,), zebra=True)
for r in range(26, 31):
    db.cell(row=r, column=4).number_format = PCT
    db.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=5).number_format = "#,##0"
    db.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=2).font = Font(name=FONT, size=11, color="2B2D42", bold=True)

# Last 6 months billed
band(db, 32, 2, 5, "BILLED - LAST 6 MONTHS (Apr to Sep 2026)")
hdr(db, 33, ["Month", "Billed", "Collected", "Share of total"], start=2, fill=TEAL)
six = [(2026, 4, "Apr 2026"), (2026, 5, "May 2026"), (2026, 6, "Jun 2026"),
       (2026, 7, "Jul 2026"), (2026, 8, "Aug 2026"), (2026, 9, "Sep 2026")]
for i, (y, m, label) in enumerate(six):
    r = 34 + i
    nm = m + 1
    db.cell(row=r, column=2, value=label)
    db.cell(row=r, column=3,
            value=f'=SUMIFS({PT}!$D:$D,{PT}!$A:$A,">="&DATE({y},{m},1),'
                  f'{PT}!$A:$A,"<"&DATE({y},{nm},1))')
    db.cell(row=r, column=4,
            value=f'=SUMIFS({PT}!$D:$D,{PT}!$A:$A,">="&DATE({y},{m},1),'
                  f'{PT}!$A:$A,"<"&DATE({y},{nm},1),{PT}!$G:$G,"Paid")')
    db.cell(row=r, column=5, value=f"=IF($B$6=0,0,C{r}/$B$6)")
box(db, 34, 39, 2, 5, money=(3, 4))
for r in range(34, 40):
    db.cell(row=r, column=5).number_format = PCT
    db.cell(row=r, column=5).alignment = Alignment(horizontal="center")
    db.cell(row=r, column=2).font = Font(name=FONT, bold=True, size=11, color="2B2D42")

db["B41"] = "Auto-calculated from PAYMENT TRACKER and CLIENT LEDGER - do not type over formulas."
db["B41"].font = Font(name=FONT, size=11, color=TEAL, italic=True)

# Ranking workings (feeds the Top 5 table)
db["F44"] = "RANKING WORKINGS (auto)"
db["F44"].font = Font(name=FONT, bold=True, size=10, color=GREY)
hdr(db, 45, ["Rank", "Client", "Revenue"], start=6, fill=GREY)
for n, (client, _contact, _email, _rate) in enumerate(ledger_rows):
    r = 46 + n
    db.cell(row=r, column=6,
            value=f"=SUMPRODUCT(($H$46:$H$53>H{r})*1)+COUNTIF($H$46:H{r},H{r})")
    db.cell(row=r, column=7, value=client)
    db.cell(row=r, column=8, value=f"=VLOOKUP(G{r},{CLG}!$A:$E,5,FALSE)")
box(db, 46, 53, 6, 8, money=(8,), zebra=False)
for r in range(46, 54):
    for c in (6, 7, 8):
        db.cell(row=r, column=c).font = Font(name=FONT, size=9, color=GREY)
    db.cell(row=r, column=6).alignment = Alignment(horizontal="center")

# ---------------------------------------------------------------- SAVE
wb.active = 0
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Client_Invoice_and_Quote_Kit_2026.xlsx")
wb.save(out)
print("saved:", out)
