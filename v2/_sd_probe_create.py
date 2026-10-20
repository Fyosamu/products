"""Probe StableDeliver's create-product validation (never creates a real product).

Sends intentionally incomplete bodies and prints the error text, which reveals
what fields the API expects (e.g. whether a hosted-file delivery type exists).
"""
import json
import sys

sys.path.insert(0, r"C:\Users\USER\Documents\Default Project\products\v2")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from _sd_session import fetch  # noqa: E402

HDRS = {"origin": "https://stabledeliver.com",
        "referer": "https://stabledeliver.com/dashboard/products"}

probes = [
    ("missing everything", {}),
    ("file delivery, no file", {"name": "probe", "description": "d", "price": "1.00",
                                "priceCurrency": "USD", "asset": "USDT", "chain": "bsc",
                                "deliveryType": "file"}),
    ("link delivery, no link", {"name": "probe", "description": "d", "price": "1.00",
                                "priceCurrency": "USD", "asset": "USDT", "chain": "bsc",
                                "deliveryType": "link"}),
]

for label, body in probes:
    st, resp, _, _ = fetch("/api/dashboard/products", method="POST", data=body,
                           headers=HDRS)
    print("==", label, "->", st)
    print("   ", json.dumps(resp, ensure_ascii=False)[:400] if not isinstance(resp, str)
          else resp[:400])
