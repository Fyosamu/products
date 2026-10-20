import io, re, json

src = io.open(r'C:\Users\USER\Documents\Default Project\products\v2\LISTINGS_V2.md', encoding='utf-8').read()
secs = re.split(r'\n## ', src)
out = []
for s in secs[1:]:
    head = s.split('\n')[0]
    price = re.search(r'\*\*Price:\*\* \$([0-9.]+)', s)
    title = re.search(r'\*\*Title:\*\*\n(.+)', s)
    desc = re.search(r'\*\*Description:\*\*\n(.+?)(?=\n\n)', s, re.S)
    zfile = re.search(r'\*\*File:\*\* `([^`]+)`', s)
    out.append({
        'head': head.strip(),
        'price': price.group(1) if price else None,
        'title': title.group(1).strip() if title else None,
        'file': zfile.group(1) if zfile else None,
        'desc': desc.group(1).strip() if desc else None,
    })
print(json.dumps(out, ensure_ascii=False, indent=1))
