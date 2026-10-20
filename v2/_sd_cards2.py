"""Print the dashboard card status badge for the 10 second-batch products."""
import html as htmllib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

IDS = {
    'aiart': 'd810d9aa-3c22-4be3-8ecd-0cfbfa5d5703',
    'course': '9fbd4054-4e52-4699-90d2-9946f0f7d7f8',
    'email': '54f74806-34ee-4011-a6b2-f0868f285c00',
    'entertain': 'd63b51cb-e143-40d4-8be8-148c616038a5',
    'events': 'efc7fa8a-6fec-4dd4-a7cc-fa3a77b75ba5',
    'finance': '473c0d21-22af-4792-94c8-ac961f75f873',
    'hrlegal': '577df1b7-64fd-46cd-9b43-badd28e3603f',
    'local': 'dd48700b-e105-46c2-a90b-7c3369bf12a3',
    'sales': 'b158e917-4e22-49ea-8d02-993e3f5132be',
    'social': '4dffb1fd-3f58-4376-a977-fe909d904701',
}

st, page, _, _ = fetch('/dashboard/products', accept='text/html')
blocks = re.split(r'(?=<div class="rounded-xl border)', page)
by_id = {}
for b in blocks[1:]:
    ids = re.findall(r'/c/([0-9a-f-]{36})', b)
    for i in ids:
        by_id.setdefault(i, b)

for k, i in sorted(IDS.items()):
    b = by_id.get(i, '')
    txt = htmllib.unescape(re.sub(r'<[^>]+>', ' | ', b))
    txt = re.sub(r'(\s*\|\s*)+', ' | ', txt).strip(' |')
    print('%-10s %s' % (k, txt[:260]))
    print()
