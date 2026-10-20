# -*- coding: utf-8 -*-
"""Build preview.html showing covers + real spreadsheet content + listing copy."""
import json, html, os
from openpyxl import load_workbook

BASE = os.path.dirname(os.path.abspath(__file__))


def sheet_preview(path, max_rows=14, max_cols=7):
    wb = load_workbook(path, data_only=False)
    out = []
    for ws in wb.worksheets:
        rows = []
        for r in ws.iter_rows(min_row=1, max_row=min(max_rows, ws.max_row),
                              max_col=min(max_cols, ws.max_column), values_only=True):
            cells = ["" if v is None else str(v) for v in r]
            while cells and cells[-1] == "":
                cells.pop()
            rows.append(cells)
        out.append({"name": ws.title, "dims": f"{ws.max_row} rows x {ws.max_column} cols",
                    "rows": rows})
    return out


data = {
    "finance": sheet_preview(os.path.join(BASE, "Freelancer_Finance_Tracker_2026.xlsx")),
    "wedding": sheet_preview(os.path.join(BASE, "Ultimate_Wedding_Planner_2026.xlsx")),
}
with open(os.path.join(BASE, "_sheets.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("sheets:", [s["name"] for s in data["finance"]], "|", [s["name"] for s in data["wedding"]])
