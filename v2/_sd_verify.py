import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

DUP = '09621caf-c433-4957-ace9-df6e20bf9322'   # probe-created duplicate of Client Invoice kit
st, resp, _, _ = fetch('/api/dashboard/products/' + DUP, method='PATCH',
                       data={'active': False},
                       headers={'origin': 'https://stabledeliver.com',
                                'referer': 'https://stabledeliver.com/dashboard/products'})
print('deactivate', st, str(resp)[:200])

# verify full list with prices + status
st, page, _, _ = fetch('/dashboard/products', accept='text/html')
starts = [m.start() for m in re.finditer(r'<div class="rounded-xl border', page)]
rows = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else len(page)
    seg = page[s:e]
    txt = re.sub(r'<[^>]+>', ' | ', seg)
    txt = re.sub(r'(\s*\|\s*)+', ' | ', txt).strip(' |')
    ck = re.search(r'/c/[0-9a-f\-]{36}', seg)
    price = re.search(r'\$([0-9]+\.[0-9]{2})', txt)
    status = re.search(r'\|\s*(live|draft|paused|inactive|deactivated)\b', txt)
    nm = re.match(r'(.*?)\s*\|\s*(?:\$|live|draft|paused)', txt)
    rows.append({
        'checkout': 'https://stabledeliver.com' + ck.group(0) if ck else None,
        'status': status.group(1) if status else '?',
        'price': price.group(1) if price else '?',
        'name': (nm.group(1) if nm else txt)[:70],
    })

print('total:', len(rows))
for r in rows:
    print(' %-10s $%-6s %s  %s' % (r['status'], r['price'], (r['checkout'] or '')[-36:], r['name']))
json.dump(rows, open('_sd_products_now.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
