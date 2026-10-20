import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

for path in ('/dashboard/orders', '/dashboard/invoices', '/dashboard', '/dashboard/reconciliation'):
    st, page, _, _ = fetch(path, accept='text/html', tries=3)
    if not isinstance(page, str):
        print(path, '->', st, str(page)[:100])
        continue
    txt = re.sub(r'<script.*?</script>', ' ', page, flags=re.S | re.I)
    txt = html.unescape(re.sub(r'<[^>]+>', ' | ', txt))
    txt = re.sub(r'(\s*\|\s*)+', ' | ', txt)
    # keep only the main area (after the h1)
    i = txt.find('Orders')
    print('=' * 60)
    print(path, st, len(page))
    print(txt[:1200])
