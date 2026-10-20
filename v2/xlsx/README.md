# Spreadsheet Products — `products/v2/xlsx`

Four sellable XLSX products, built with **Python 3.12 + openpyxl 3.1.5 only**
(no pandas, no macros, no external links, no network calls).

Shared visual language (same as `products/build_finance_tracker.py`):
**NAVY `1F2A44` · TEAL `0FA3B1` · LIGHT `EAF4F4` · GOLD `F4B942` · GREY `8D99AE`**, Calibri,
thin `D5DDE5` borders on every data cell, navy/white-bold centred header rows, frozen panes
below header rows, gridlines **off** on every sheet, alternating `F7FAFC` zebra rows,
currency `$#,##0.00`, dates `dd-mmm-yyyy`, **zero merged cells**.

---

## 1. `Client_Invoice_and_Quote_Kit_2026.xlsx` — 17,867 bytes

Sheets: `Start Here | INVOICE MAKER | QUOTE MAKER | PAYMENT TRACKER | CLIENT LEDGER | DASHBOARD`

- **INVOICE MAKER** — reusable freelancer invoice: business block (incl.
  *Receive crypto: USDT on BNB Smart Chain (BEP-20)*), BILL TO block, 10 line-item rows with
  `Amount = Qty × Rate`, Subtotal / Discount % / Tax % / TOTAL DUE formulas, payment terms,
  issue + due date (live `=G3+14`).
- **QUOTE MAKER** — same structure + `Draft/Sent/Viewed/Accepted/Declined` dropdown and
  Valid-until date (green Accepted, red Declined).
- **PAYMENT TRACKER** — 24 sample invoices (Jan–Sep 2026): Date, Invoice #, Client, Amount,
  Due date, Method (Bank/PayPal/Cash/Card/USDT-BEP20), Status, `Days late = MAX(0, TODAY()-due)`,
  Notes. Red CF on `Overdue`, green on `Paid`.
- **CLIENT LEDGER** — 8 clients, `SUMIF` invoiced, `SUMIFS` paid, balance, auto status.
- **DASHBOARD** — total invoiced / collected / outstanding, overdue count + value,
  avg days to pay, collection rate, top 5 clients by revenue (`VLOOKUP` ranking), billed by
  month for the last 6 months (`SUMIFS`).

Build: `build_invoice_kit.py`

## 2. `Content_Calendar_and_Social_Media_Planner_2026.xlsx` — 39,311 bytes

Sheets: `Start Here | YEAR 2026 | CONTENT CALENDAR | POST TRACKER | IDEAS BACKLOG | HASHTAG BANK | ANALYTICS | DASHBOARD`

- **YEAR 2026** — all **365 dates** of 2026 with week no, month, day, weekday (computed in
  Python, not formulas) and **22 marked key dates** (New Year, MLK Day, Super Bowl LX 8 Feb,
  Valentine's, Presidents' Day, Ramadan ~18 Feb, IWD, Pi Day, Eid al-Fitr ~20 Mar, Easter,
  Mother's Day, Memorial Day, Eid al-Adha, Father's Day, Independence Day, Labor Day,
  Halloween, Thanksgiving, Black Friday 27 Nov, Cyber Monday, Christmas, NYE).
- **CONTENT CALENDAR** — 40 posts (Jan–Sep 2026) × 13 columns: platform/pillar/format/
  status dropdowns, hook, caption, CTA, link, likes/comments/shares/reach (data bars).
- **POST TRACKER** — 24 live posts with auto engagement % + % thresholds CF.
- **IDEAS BACKLOG** (18) · **HASHTAG BANK** (10 groups) · **ANALYTICS** (W1–W52 with
  engagement-rate formulas and a streak helper column).
- **DASHBOARD** — status breakdown, per-platform counts/reach, posts per month × platform
  (`COUNTIFS` × 12 months × 7 platforms), total reach, avg engagement, posting streak,
  % of year covered.

Build: `build_content_calendar.py`

## 3. `Personal_Budget_and_Savings_Tracker_2026.xlsx` — 25,005 bytes

Sheets: `Start Here | DASHBOARD | MONTHLY BUDGET | EXPENSE LOG | SAVINGS GOALS | DEBT SNOWBALL | NET WORTH`

- **MONTHLY BUDGET** — 14 categories (6 Fixed + 8 Variable) × Jan–Dec planned (editable,
  light-blue), an ACTUAL block fed by `SUMIFS` from the expense log, plus Actual total /
  Plan / Plan-to-date / Variance / **% used** with red CF above 100 %, and a
  **50/30/20 Needs-Wants-Savings scorecard** with `IF` status.
- **EXPENSE LOG** — 50 realistic transactions (Jan–May 2026), 4 dropdowns, data bars.
- **SAVINGS GOALS** — 6 goals with auto Remaining, Progress % (red→yellow→green 3-colour
  scale + data bars), monthly needed and On track/Behind/Complete status.
- **DEBT SNOWBALL** — 6 debts, payoff order by smallest balance (`SUMPRODUCT`), months to
  payoff (amortisation formula), interest saved, status; helper columns for the comparison.
- **NET WORTH** — 5 assets + 3 liabilities Jan–Jun, net-worth row, latest vs January delta.
- **DASHBOARD** — income / spent / saved for the selectable reporting month (cell C4),
  savings rate, biggest category (`VLOOKUP` on a ranking helper), budget health,
  categories over plan, avg goals progress, debt-free date, top-5 categories,
  income vs spend for all 12 months.

Build: `build_budget_tracker.py`

## 4. `Client_CRM_and_Project_Tracker.xlsx` — 24,689 bytes

Sheets: `Start Here | PIPELINE | PROJECTS | TIMESHEET | DELIVERABLES | FOLLOW-UPS | DASHBOARD`

- **PIPELINE** — 25 leads: source/stage/owner dropdowns, weighted value `=value×probability`,
  red CF when *Next follow-up* < `TODAY()` and stage is not Won/Lost, amber within 3 days.
- **PROJECTS** — 12 projects with hourly-cost cell in `B1`, logged hours (`SUMIF` from the
  timesheet), % complete, profit `= value − logged × cost`, red/amber deadline CF.
- **TIMESHEET** — 40 rows, `Amount = IF(billable="No",0,hours×rate)`, invoiced dropdown.
- **DELIVERABLES** — 16 items with status dropdown + overdue-date CF.
- **FOLLOW-UPS** — 18 log rows, channel/outcome dropdowns, red/amber next-date CF.
- **DASHBOARD** — pipeline value by stage (`SUMIF`), weighted pipeline, win rate, active
  projects + value, hours logged this month (`SUMIFS`), unbilled value, overdue follow-ups,
  overdue deliverables, hours & billing summary, top clients by project value.

Build: `build_crm_tracker.py`

---

## Rebuild & verify

```powershell
cd "C:\Users\USER\Documents\Default Project\products\v2\xlsx"
python build_invoice_kit.py
python build_content_calendar.py
python build_budget_tracker.py
python build_crm_tracker.py
python verify.py
```

`verify.py` opens all four workbooks with `openpyxl(data_only=False)` and checks:
required sheet names + order, **no merged cells anywhere**, gridlines off, `Start Here` first,
DASHBOARD holds live formulas, no banned functions (`IFS`, `XLOOKUP`, `TEXTJOIN`, `FILTER`,
`UNIQUE`, `SORT`, `SEQUENCE`, `LET`), all cross-sheet references resolve, 15–60 sample rows in
each main log sheet, and dropdowns + conditional formatting present.

Dashboard formulas are limited to `SUM` / `SUMIF` / `SUMIFS` / `COUNTIF` / `COUNTIFS` /
`SUMPRODUCT` / `VLOOKUP` / `IF` (+ `DATE`, `TODAY`, `MAX` for date maths) so they work in
older Excel and Google Sheets.
