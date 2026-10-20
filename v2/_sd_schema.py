# -*- coding: utf-8 -*-
"""Where is the SD product editor, and does it expose an image field?"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

st, page, _, _ = fetch('/dashboard/products', accept='text/html')
if not isinstance(page, str):
    print('page fail', st, page)
    raise SystemExit(1)
hrefs = sorted(set(re.findall(r'href="([^"]*)"', page)))
print('hrefs with product:', [h for h in hrefs if 'product' in h.lower()][:20])
print('any /dashboard/ hrefs:', [h for h in hrefs if h.startswith('/dashboard')][:25])

# the row markup (used by _sd_create_packs2.py)
i = page.find('<div class="rounded-xl border')
print('\nrow markup sample:\n', re.sub(r'\s+', ' ', page[i:i + 900])[:900])

# buttons / onclick that open an editor
for pat in (r'onclick="([^"]{0,140})"', r'data-[a-z\-]*id="([^"]+)"',
            r'href="/dashboard/product[^"]*"'):
    m = list(dict.fromkeys(re.findall(pat, page)))[:8]
    if m:
        print('\n%s ->' % pat[:30], m)
