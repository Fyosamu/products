# -*- coding: utf-8 -*-
"""Does StableDeliver support a product cover image, and how is it set?"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

st, page, _, url = fetch('/dashboard/products', accept='text/html')
print('dashboard:', st, len(page) if isinstance(page, str) else page, url)
if not isinstance(page, str):
    raise SystemExit(1)

ids = list(dict.fromkeys(re.findall(r'/dashboard/products/([0-9a-f\-]{8,})', page)))
print('product ids on page:', len(ids), ids[:5])

if ids:
    st2, edit, _, url2 = fetch('/dashboard/products/%s/edit' % ids[0], accept='text/html')
    print('edit page:', st2, len(edit) if isinstance(edit, str) else edit, url2)
    if isinstance(edit, str):
        for kw in ('type="file"', 'coverImage', 'thumbnail', 'imageUrl', 'image',
                   'upload', 'logo', 'banner', 'dropzone'):
            n = edit.lower().count(kw.lower())
            if n:
                print('   %-14s x%d' % (kw, n))
        for m in list(re.finditer(r'<input[^>]*type="file"[^>]*>', edit))[:3]:
            print('   input:', m.group(0)[:220])
        # api routes referenced
        routes = sorted(set(re.findall(r'/api/[a-zA-Z0-9_\-/{}$]+', edit)))
        print('   routes in edit html:', routes[:20])

# scan the app chunks for an image upload route
found = set()
for page_url in ('/dashboard/products', '/dashboard/products/new'):
    st3, html3, _, _ = fetch(page_url, accept='text/html')
    if not isinstance(html3, str):
        continue
    for c in sorted(set(re.findall(r'/_next/static/chunks/[^"\']+\.js', html3)))[:40]:
        st4, js, _, _ = fetch(c, accept='application/javascript')
        if not isinstance(js, str) or len(js) < 200:
            continue
        for m in re.finditer(r'/api/[a-zA-Z0-9_\-/]*(?:upload|image|media|file)[a-zA-Z0-9_\-/]*',
                             js):
            found.add(m.group(0))
        for kw in ('coverImage', 'thumbnailUrl', 'imageUrl', 'productImage', 'image:'):
            if kw in js:
                i = js.find(kw)
                seg = re.sub(r'\s+', ' ', js[max(0, i - 260):i + 260])
                found.add('SEG %s :: %s' % (kw, seg[:380]))
print('\nimage routes found:')
for f in sorted(found):
    print('  -', f[:400])
