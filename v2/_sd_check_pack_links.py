import urllib.request, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_create_packs import PROTON, LIVE

ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36'}
bad = []
for k, u in PROTON.items():
    try:
        r = urllib.request.Request(u.split('#')[0], headers=ua, method='GET')
        resp = urllib.request.urlopen(r, timeout=30)
        print(resp.status, k.ljust(11), u)
        if resp.status != 200:
            bad.append(k)
    except Exception as e:
        print('ERR', k, e)
        bad.append(k)
print('DEAD LINKS:', bad)
