import sys, os, re, html, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

PAIRS = [
    ('preexisting', '971acce3-abeb-428e-8fe4-f404a421a963', 'cf10ac7b-ce34-45bc-9010-552d3cf27bd7'),   # etsy
    ('preexisting', 'f0936e40-fbba-4582-ad55-0d517009e83f', '2538fbbb-1834-448c-a00d-408e56591d66'),   # food
]

def text(pid):
    st, page, _, _ = fetch('/c/' + pid, accept='text/html', tries=3)
    if not isinstance(page, str):
        return st, None
    body = re.sub(r'<script.*?</script>', ' ', page, flags=re.S | re.I)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', '\n', body)
    t = html.unescape(t)
    t = re.sub(r'\n{2,}', '\n', t)
    return st, t.strip()

for label, old, new in PAIRS:
    print('=' * 70)
    for tag, pid in (('OLD', old), ('NEW', new)):
        st, t = text(pid)
        print(tag, pid, 'status', st, 'chars', len(t) if t else None)
        if t:
            print('   head:', t[:400].replace('\n', ' | '))
            print('   has proton link:', 'drive.proton.me' in t, '| price mentions:', bool(re.search(r'\$4\.99', t)))
