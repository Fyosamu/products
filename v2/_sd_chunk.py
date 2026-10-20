import json, re
from _sd_session import fetch

st, js, _, _ = fetch('/_next/static/chunks/app/dashboard/products/page-6c6418d1a445dd75.js', accept='*/*')
print('status', st, 'len', len(js) if isinstance(js, str) else js)
if isinstance(js, str):
    open('_sd_products_chunk.js', 'w', encoding='utf-8').write(js)
    print('api refs:', sorted(set(re.findall(r'["\'`](/?api/[A-Za-z0-9_\-/{}\.]+)["\'`]', js))))
    print('fetch calls:')
    for m in re.finditer(r'fetch\(\s*([^,]+),\s*\{([^}]{0,300})', js):
        print('  ', m.group(1)[:80], '=>', m.group(2)[:200].replace('\n', ' '))
