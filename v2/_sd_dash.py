import json, re
from _sd_session import fetch

st, page, _, _ = fetch('/dashboard/products', accept='text/html')
print('scripts:', sorted(set(re.findall(r'/_next/static/chunks/[^"\']+\.js', page))))
# find RSC payload referencing the page chunk
print('app chunks:', sorted(set(re.findall(r'static/chunks/app/[^"\\]+\.js', page))))
# search for "products" chunk hints
print(sorted(set(re.findall(r'"([0-9a-f]{1,6})","(static/chunks/[^"]+)"', page)))[:20])
