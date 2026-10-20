import re, io, json
js = io.open('_sd_products_chunk.js', encoding='utf-8').read()
print('methods:', sorted(set(re.findall(r'method:\s*"([A-Z]+)"', js))))
for kw in ['DELETE', 'Deactivate', 'deactivate', 'archive', 'delete']:
    for m in list(re.finditer(kw, js))[:3]:
        print('==', kw, '==')
        print(js[max(0, m.start() - 350):m.start() + 250].replace('\n', ' '))
        print()
