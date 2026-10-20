"""Create the 10 batch-v2 products on StableDeliver (0% fee, USDT/BEP-20 -> Trust Wallet).

Idempotent: skips product names that already exist on the account.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

HERE = os.path.dirname(os.path.abspath(__file__))
payload = json.load(open(os.path.join(HERE, '_sd_payload.json'), encoding='utf-8'))
links = json.load(open(os.path.join(HERE, '_sd_proton_links.json'), encoding='utf-8'))


def existing_names():
    st, page, _, _ = fetch('/dashboard/products', accept='text/html')
    if not isinstance(page, str):
        return set()
    out = set()
    for s in re.findall(r'<div class="rounded-xl border[^"]*">(.*?)</div></div></div>', page, re.S):
        txt = re.sub(r'<[^>]+>', '', s).strip()
        m = re.match(r'\s*(.+?)\s*(?:live|draft|paused|inactive)', txt)
        if m:
            out.add(m.group(1).strip())
    return out


have = existing_names()
print('existing products:', len(have))

created, skipped, failed = [], [], []
for item in payload:
    if item['title'] in have:
        skipped.append(item['file'])
        continue
    link = links.get(item['file'])
    if not link:
        failed.append([item['file'], 'no proton link'])
        continue
    body = {
        'name': item['title'],
        'description': item['desc'],
        'price': '%.2f' % item['price'],
        'priceCurrency': 'USD',
        'asset': 'USDT',
        'chain': 'bsc',
        'deliveryType': 'link',
        'link': link,
        'keys': '',
        'telegramGroup': '',
    }
    st, resp, _, _ = fetch('/api/dashboard/products', method='POST', data=body,
                           headers={'origin': 'https://stabledeliver.com',
                                    'referer': 'https://stabledeliver.com/dashboard/products'})
    if st in (200, 201):
        created.append([item['file'], st])
        have.add(item['title'])
    else:
        failed.append([item['file'], st, str(resp)[:300]])

print('CREATED', len(created))
for r in created:
    print('  +', r)
print('SKIPPED(already there)', len(skipped), skipped)
print('FAILED', len(failed))
for r in failed:
    print('  !', r)
