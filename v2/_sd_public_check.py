# -*- coding: utf-8 -*-
"""Does the public StableDeliver checkout page render any product image?"""
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

st, page, _, url = fetch('/c/4dffb1fd-3f58-4376-a977-fe909d904701', accept='text/html')
print('checkout:', st, len(page) if isinstance(page, str) else page, url)
if not isinstance(page, str):
    raise SystemExit(1)
for prop in ('og:image', 'og:title', 'og:description', 'twitter:image'):
    m = (re.findall(r'<meta property="%s" content="([^"]*)"' % prop, page) or
         re.findall(r'<meta name="%s" content="([^"]*)"' % prop, page))
    print('   %-16s %s' % (prop, (m[0][:110] if m else '-')))
imgs = re.findall(r'<img[^>]*src="([^"]+)"', page)
print('   <img> count:', len(imgs))
for s in imgs[:8]:
    print('      ', s[:130])
# any hero/placeholder div suggesting the design has an image slot
for kw in ('background-image', 'cover', 'thumbnail', 'productImage'):
    n = page.lower().count(kw.lower())
    if n:
        print('   kw %-16s x%d' % (kw, n))
