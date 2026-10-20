"""Extract checkout /c/<uuid> links for the 10 second-batch packs."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

KEYS = ['aiart', 'course', 'email', 'entertain', 'events',
        'finance', 'hrlegal', 'local', 'sales', 'social']

st, page, _, _ = fetch('/dashboard/products', accept='text/html')
print('status', st, 'len', len(page) if isinstance(page, str) else type(page))

blocks = re.split(r'(?=<div class="rounded-xl border)', page)
found = {}
for b in blocks[1:]:
    ids = re.findall(r'/c/([0-9a-f-]{36})', b)
    if not ids:
        continue
    txt = re.sub(r'<[^>]+>', ' ', b)
    txt = re.sub(r'\s+', ' ', txt).strip()
    found[ids[0]] = txt[:220]

print('cards with checkout id:', len(found))
for k in KEYS:
    hit = [i for i, t in found.items() if t.lower().startswith(k) or (' ' + k) in t.lower()[:40]]
    for i in hit:
        print('%-10s https://stabledeliver.com/c/%s' % (k, i))
    if not hit:
        print('%-10s NOT FOUND' % k)

print('\n-- all $4.99 cards --')
for i, t in found.items():
    if '4.99' in t:
        print(i, '|', t[:110])
