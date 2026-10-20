"""Print slug/price/status for the 10 batch-2 packs on Getly (+ totals)."""
import json
import urllib.request

URL = 'https://www.getly.store/api/stores/dreamer-prompt-lab-muifdken'
req = urllib.request.Request(URL, headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'accept': 'application/json',
})
data = json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace'))['data']
products = data['products']

MINE = ['Email Marketing', 'Social Media Manager', 'Course Creator', 'Local & Home Services',
        'Wedding, Events', 'Sales Copy', 'AI Art, Midjourney', 'HR, Legal',
        'Podcast, Music', 'Finance, Fundraising']

print('total products:', len(products))
active = [p for p in products if p.get('status') == 'active']
print('active:', len(active), 'statuses:',
      {s: sum(1 for p in products if p.get('status') == s) for s in set(p.get('status') for p in products)})
print()
for m in MINE:
    hit = [p for p in products if p.get('name', '').startswith(m)]
    for p in hit:
        print('%-6s %-8s %s' % (p.get('price'), p.get('status'), p.get('name')[:70]))
        print('        https://www.getly.store/product/%s?sref=dreamer-prompt-lab-muifdken' % p['slug'])
    if not hit:
        print(m, '-> NOT FOUND')
