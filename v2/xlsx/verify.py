# -*- coding: utf-8 -*-
"""Verify the 4 sellable workbooks in products/v2/xlsx (openpyxl, data_only=False)."""
import os
import re
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))

REQUIRED_SHEETS = {
    "Client_Invoice_and_Quote_Kit_2026.xlsx": [
        "Start Here", "INVOICE MAKER", "QUOTE MAKER", "PAYMENT TRACKER",
        "CLIENT LEDGER", "DASHBOARD",
    ],
    "Content_Calendar_and_Social_Media_Planner_2026.xlsx": [
        "Start Here", "YEAR 2026", "CONTENT CALENDAR", "POST TRACKER",
        "IDEAS BACKLOG", "HASHTAG BANK", "ANALYTICS", "DASHBOARD",
    ],
    "Personal_Budget_and_Savings_Tracker_2026.xlsx": [
        "Start Here", "DASHBOARD", "MONTHLY BUDGET", "EXPENSE LOG",
        "SAVINGS GOALS", "DEBT SNOWBALL", "NET WORTH",
    ],
    "Client_CRM_and_Project_Tracker.xlsx": [
        "Start Here", "PIPELINE", "PROJECTS", "TIMESHEET", "DELIVERABLES",
        "FOLLOW-UPS", "DASHBOARD",
    ],
}

# main log sheet per workbook -> (sheet, header row, label)
MAIN_LOG = {
    "Client_Invoice_and_Quote_Kit_2026.xlsx": "PAYMENT TRACKER",
    "Content_Calendar_and_Social_Media_Planner_2026.xlsx": "CONTENT CALENDAR",
    "Personal_Budget_and_Savings_Tracker_2026.xlsx": "EXPENSE LOG",
    "Client_CRM_and_Project_Tracker.xlsx": "PIPELINE",
}

# every formula-function that older Excel / Google Sheets choke on
BANNED = re.compile(r"\b(IFS|XLOOKUP|TEXTJOIN|FILTER|UNIQUE|SORTBY|SEQUENCE|LET)\s*\(")
# also catch dynamic-array / modern spill functions written without parens in ranges
BANNED_RANGE = re.compile(r"\b(SORT|UNIQUE|SEQUENCE)\s*\(")

DASH_CELL = re.compile(r"^[=]")


def count_rows(ws, header_row):
    n = 0
    for r in range(header_row + 1, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if v not in (None, ""):
            n += 1
    return n


def formulas_in(ws):
    out = []
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                out.append((c.coordinate, c.value))
    return out


def main():
    total_formulas = 0
    problems = []

    for fname, required in REQUIRED_SHEETS.items():
        path = os.path.join(HERE, fname)
        assert os.path.exists(path), f"MISSING FILE: {fname}"
        size = os.path.getsize(path)
        wb = openpyxl.load_workbook(path, data_only=False)
        names = wb.sheetnames
        print("=" * 78)
        print(f"FILE: {fname}")
        print(f"  bytes: {size:,}")
        print(f"  sheets ({len(names)}): {names}")

        # 1. required sheets present, in order
        assert names == required, f"{fname}: sheet order/content mismatch\n got {names}\n want {required}"
        print("  [OK] required sheets present and in order")

        # 2. no merged cells anywhere
        merged = {ws.title: len(ws.merged_cells.ranges) for ws in wb}
        assert all(v == 0 for v in merged.values()), f"{fname}: merged cells found: {merged}"
        print("  [OK] no merged cells on any sheet")

        # 3. gridlines off everywhere
        grid_on = [ws.title for ws in wb if ws.sheet_view.showGridLines]
        assert not grid_on, f"{fname}: gridlines visible on {grid_on}"
        print("  [OK] gridlines off on every sheet")

        # 4. Start Here first, DASHBOARD present and holds live formulas
        assert names[0] == "Start Here", f"{fname}: Start Here is not first"
        dash = wb["DASHBOARD"]
        dash_formulas = formulas_in(dash)
        assert dash_formulas, f"{fname}: DASHBOARD has no formulas"
        total_formulas += len(dash_formulas)
        print(f"  [OK] DASHBOARD contains {len(dash_formulas)} live formulas "
              f"(e.g. {dash_formulas[0][0]} = {dash_formulas[0][1][:48]}...)")

        # 5. only old-Excel-safe functions in the whole workbook
        bad = []
        all_formula_count = 0
        for ws in wb:
            for coord, f in formulas_in(ws):
                all_formula_count += 1
                if BANNED.search(f) or BANNED_RANGE.search(f):
                    bad.append(f"{ws.title}!{coord}: {f}")
        assert not bad, f"{fname}: banned functions used: {bad}"
        total_formulas += all_formula_count - len(dash_formulas)
        print(f"  [OK] {all_formula_count} formulas total, no IFS/XLOOKUP/TEXTJOIN/"
              f"dynamic-array functions")

        # 5b. every sheet name quoted in a formula actually exists
        ref_re = re.compile(r"'([^']+)'!")
        missing = []
        for ws in wb:
            for coord, f in formulas_in(ws):
                for ref in ref_re.findall(f):
                    if ref not in names:
                        missing.append(f"{ws.title}!{coord} -> '{ref}'")
                if "#REF" in f:
                    missing.append(f"{ws.title}!{coord} contains #REF")
        assert not missing, f"{fname}: broken sheet references: {missing}"
        print(f"  [OK] all cross-sheet references resolve")

        # 6. sample rows in the main log sheet
        log_name = MAIN_LOG[fname]
        header_row = 2 if log_name == "PROJECTS" else 1
        rows = count_rows(wb[log_name], header_row)
        assert 15 <= rows <= 60, f"{fname}: {log_name} has {rows} sample rows (want 15-60)"
        print(f"  [OK] {log_name}: {rows} sample rows")

        # 7. dropdowns + conditional formatting on the main log sheet
        log = wb[log_name]
        n_dv = len(log.data_validations.dataValidation)
        n_cf = len(log.conditional_formatting._cf_rules)
        assert n_dv >= 1, f"{fname}: no data validation dropdowns on {log_name}"
        assert n_cf >= 1, f"{fname}: no conditional formatting on {log_name}"
        print(f"  [OK] {log_name}: {n_dv} dropdowns, {n_cf} conditional-format ranges, "
              f"freeze={log.freeze_panes}")

    print("=" * 78)
    print(f"ALL CHECKS PASSED - 4 workbooks, {total_formulas} formulas verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
