import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

HDR = {'origin': 'https://stabledeliver.com',
       'referer': 'https://stabledeliver.com/dashboard/products'}

pairs = [
    ('preexisting (em dash)', '971acce3-abeb-428e-8fe4-f404a421a963'),
    ('mine (hyphen)        ', 'cf10ac7b-ce34-45bc-9010-552d3cf27bd7'),
    ('preexisting2         ', 'f0936e40-fbba-4582-ad55-0d517009e83f'),
    ('mine2                ', '2538fbbb-1834-448c-a00d-408e56591d66'),
]
for label, pid in pairs:
    for path in ('/api/dashboard/products/' + pid, '/api/dashboard/products?id=' + pid):
        st, resp, _, _ = fetch(path, accept='application/json')
        if st == 200 and isinstance(resp, dict) and resp.get('error') is None:
            d = resp.get('product') or resp
            print(label, path, '->')
            print('   keys:', sorted(d.keys()))
            print('   name:', str(d.get('name'))[:60])
            print('   link:', d.get('link'))
            print('   desc len:', len(str(d.get('description') or '')), 'price:', d.get('price'), 'active:', d.get('active'))
            break
    else:
        print(label, 'no working GET', st, str(resp)[:120])
