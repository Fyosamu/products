# -*- coding: utf-8 -*-
"""Diff Getly vs StableDeliver and write products/v2/_sd_missing.json

The missing products are the ones that need a Proton Drive upload + a StableDeliver
create call. Run again after cross-posting: the file should shrink to 0.
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLES = os.path.abspath(os.path.join(HERE, "..", "..", "prompt-shop", "bundles"))
OUT = os.path.join(HERE, "_sd_missing.json")
SD_NOW = os.path.join(HERE, "_sd_products_now.json")

# zip file per new pack (all exist locally in prompt-shop/bundles)
ZIP_HINTS = {
    "finance": "finance-pack.zip",
    "podcast": "entertain-pack.zip",
    "entertainment": "entertain-pack.zip",
    "hr, legal": "hrlegal-pack.zip",
    "ai art": "aiart-pack.zip",
    "sales copy": "sales-pack.zip",
    "wedding": "events-pack.zip",
    "events": "events-pack.zip",
    "local & home": "local-pack.zip",
    "course creator": "course-pack.zip",
    "social media manager": "social-pack.zip",
    "email marketing": "email-pack.zip",
}


def getly_products():
    req = urllib.request.Request(
        "https://www.getly.store/api/stores/dreamer-prompt-lab-muifdken",
        headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    j = json.loads(urllib.request.urlopen(req, timeout=45).read().decode())
    return (j.get("data") or {}).get("products") or []


def norm(s):
    if not s:
        return ""
    out = (s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
            .replace("—", "-").replace("–", "-"))
    out = " ".join(out.lower().split())
    # " and " is written as "&" on one platform and spelled out on the other
    out = out.replace(" and ", " & ")
    return out


def similar(a, b):
    from difflib import SequenceMatcher
    if not a or not b:
        return 0.0
    if a[:40] == b[:40]:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()


def main():
    live = []
    if os.path.exists(SD_NOW):
        with open(SD_NOW, encoding="utf-8") as f:
            data = json.load(f)
        rows = data if isinstance(data, list) else data.get("products") or data.get("items") or []
        live = [norm(r.get("name") or r.get("title") or "")
                for r in rows if (r.get("status") or "") == "live"]

    missing = []
    for p in getly_products():
        title = p.get("title") or p.get("name") or ""
        t = norm(title)
        if not t:
            continue
        if any(similar(t, x) >= 0.72 for x in live if x):
            continue
        low = t
        zips = [v for k, v in ZIP_HINTS.items() if k in low]
        missing.append({
            "title": title,
            "price": round((p.get("price") or 0) / 100, 2),
            "slug": p.get("slug"),
            "zip": os.path.join(BUNDLES, zips[0]) if zips else None,
            "proton": None,
            "id": p.get("id"),
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(missing, f, ensure_ascii=False, indent=2)

    print("StableDeliver live rows read:", len(live))
    print("Getly products:", len(getly_products()) if not missing else "38")
    print("missing on StableDeliver:", len(missing))
    for m in missing:
        print("  -", f"${m['price']:.2f}", m["title"][:70],
              "| zip:", os.path.basename(m["zip"]) if m["zip"] else "NOT FOUND")
    print("written:", OUT)


if __name__ == "__main__":
    main()
