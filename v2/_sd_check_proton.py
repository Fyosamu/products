import json, urllib.request, os

links = json.load(open('_sd_proton_links.json', encoding='utf-8'))
ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36'}
for f, u in links.items():
    try:
        r = urllib.request.Request(u.split('#')[0], headers=ua, method='GET')
        resp = urllib.request.urlopen(r, timeout=30)
        st = resp.status
        body = resp.read(4000).decode('utf-8', 'replace')
        hint = 'share-page' if ('drive.proton.me' in body or 'Proton' in body) else body[:60].replace('\n', ' ')
        print(st, f[:46].ljust(46), hint)
    except Exception as e:
        print('ERR', f, e)
