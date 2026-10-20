import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

st, page, _, _ = fetch('/dashboard/products', accept='text/html')
open('_sd_dash2.html', 'w', encoding='utf-8').write(page)
links = re.findall(r'href="(/c/[0-9a-f\-]{36})"', page)
print('checkout links:', len(links))

# product cards are rounded-xl blocks; extract name-ish text
seg = re.findall(r'<div class="rounded-xl border[^"]*">(.*?)</div></div></div>', page, re.S)
print('cards:', len(seg))
for s in seg:
    txt = re.sub(r'<[^>]+>', '|', s)
    txt = re.sub(r'\|+', ' | ', txt)
    print(' *', txt[:250])
