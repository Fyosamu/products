"""Check active/inactive status of the 10 second-batch StableDeliver products."""
import json
import os
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

for path in ('/api/dashboard/products', '/api/products', '/api/dashboard/products?page=1'):
    st, resp, _, _ = fetch(path, accept='application/json')
    print(path, '->', st, type(resp).__name__,
          (list(resp)[:6] if isinstance(resp, dict) else str(resp)[:120]))
    if st == 200 and isinstance(resp, dict):
        data = resp.get('products') or resp.get('items') or resp.get('data') or []
        print('  count', len(data))
        if data:
            print('  keys', sorted(data[0].keys()))
            for p in data:
                pid = p.get('id') or p.get('_id')
                for k, v in IDS.items():
                    if pid == v:
                        flags = {f: p.get(f) for f in
                                 ('status', 'active', 'isActive', 'state', 'live', 'hidden', 'deactivated')
                                 if f in p}
                        print('  %-10s %s %s' % (k, p.get('name', '')[:50], flags))
        break
