import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

rows = json.load(open('_sd_products_now.json', encoding='utf-8'))
live = [r for r in rows if r['status'] == 'live']
print('live products:', len(live))
bad = []
for r in live:
    path = r['checkout'].replace('https://stabledeliver.com', '')
    st, page, _, url = fetch(path, accept='text/html', tries=3)
    ok = st == 200
    # confirm price appears on the public page
    has_price = isinstance(page, str) and ('$' + r['price']) in page
    if not ok or not has_price:
        bad.append((r['checkout'], st, has_price))
    print(' ', st, 'price-visible' if has_price else 'PRICE-MISSING', r['checkout'], r['price'])
print('PROBLEMS:', bad)
