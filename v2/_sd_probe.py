import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

p = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_sd_payload.json'), encoding='utf-8'))[0]
lk = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_sd_proton_links.json'), encoding='utf-8'))
body = {
    'name': p['title'],
    'description': p['desc'],
    'price': '%.2f' % p['price'],
    'priceCurrency': 'USD',
    'asset': 'USDT',
    'chain': 'bsc',
    'deliveryType': 'link',
    'link': lk[p['file']],
    'keys': '',
    'telegramGroup': '',
}
variants = {
    'origin+referer': {'origin': 'https://stabledeliver.com', 'referer': 'https://stabledeliver.com/dashboard/products'},
    'x-requested': {'x-requested-with': 'XMLHttpRequest', 'origin': 'https://stabledeliver.com'},
    'sec-fetch': {'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'origin': 'https://stabledeliver.com'},
}
for label, extra in variants.items():
    st, resp, _, _ = fetch('/api/dashboard/products', method='POST', data=body,
                           headers=extra, accept='application/json')
    print(label, '->', st, str(resp)[:200])
    if st in (200, 201):
        break
