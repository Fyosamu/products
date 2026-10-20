"""Cross-post the 10 second-batch niche prompt packs ($4.99) to StableDeliver.

Names + descriptions are parsed from prompt-shop/listings-packs2-ready.md
(the same file used for the Getly listings), delivery links come from
_prompto_links2.json next to this script (filled after the Proton Drive
public shares were created).

Idempotent: titles that already exist on the account are skipped.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))          # .../Default Project
LISTINGS = os.path.join(ROOT, 'prompt-shop', 'listings-packs2-ready.md')
LINKS = os.path.join(HERE, '_sd_proton_links2.json')

PRICE = 4.99


def html_to_text(h):
    h = re.sub(r'</(p|li|h1|h2|h3|h4|div|ul|ol|tr)>', '\n', h, flags=re.I)
    h = re.sub(r'<br\s*/?>', '\n', h, flags=re.I)
    h = re.sub(r'<li[^>]*>', '- ', h, flags=re.I)
    h = re.sub(r'<[^>]+>', '', h)
    lines = [re.sub(r'[ \t]+', ' ', s).strip() for s in html.unescape(h).split('\n')]
    out, prev = [], None
    for s in lines:
        if s == '' and prev == '':
            continue
        out.append(s)
        prev = s
    return '\n'.join(out).strip()


def parse_listings():
    src = open(LISTINGS, encoding='utf-8-sig').read()
    blocks = re.split(r'^## \d+\. ', src, flags=re.M)[1:]
    items = {}
    for b in blocks:
        key = b.split()[0].strip().lower()
        nm = re.search(r'\*\*Name:\*\*\s*(.+)', b)
        dm = re.search(r'\*\*Description \(HTML\):\*\*\s*```html\s*(.*?)\s*```', b, re.S)
        if nm and dm:
            items[key] = {'name': nm.group(1).strip(), 'desc': html_to_text(dm.group(1))}
    return items


def existing_names():
    st, page, _, _ = fetch('/dashboard/products', accept='text/html')
    if not isinstance(page, str):
        return set()
    out = set()
    starts = [m.start() for m in re.finditer(r'<div class="rounded-xl border', page)]
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(page)
        txt = re.sub(r'<[^>]+>', ' | ', page[s:e])
        txt = re.sub(r'(\s*\|\s*)+', ' | ', txt).strip(' |')
        m = re.match(r'(.*?)\s*\|\s*(?:\$|live|draft|paused)', txt)
        if m:
            out.add(html.unescape(m.group(1)).strip())
    return out


def main():
    items = parse_listings()
    links = json.load(open(LINKS, encoding='utf-8'))
    print('listings parsed:', sorted(items))
    print('proton links   :', sorted(links))
    have = existing_names()
    print('existing on StableDeliver:', len(have))

    created, skipped, failed, nolink = [], [], [], []
    for key, it in sorted(items.items()):
        link = links.get(key)
        if not link:
            nolink.append(key)
            continue
        if it['name'] in have:
            skipped.append(key)
            continue
        body = {
            'name': it['name'],
            'description': it['desc'],
            'price': '%.2f' % PRICE,
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
            created.append([key, resp.get('id') if isinstance(resp, dict) else resp])
            have.add(it['name'])
        else:
            failed.append([key, st, str(resp)[:250]])

    print('CREATED', len(created))
    for c in created:
        print('  +', c)
    print('SKIPPED (already live)', skipped)
    print('NO LINK YET', nolink)
    print('FAILED', failed)


if __name__ == '__main__':
    main()
