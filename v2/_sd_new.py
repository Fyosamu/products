import json, re
from _sd_session import fetch

st, page, _, _ = fetch('/dashboard/products/new', accept='text/html')
print('new page', st, len(page) if isinstance(page, str) else page)
if isinstance(page, str):
    print('api refs:', sorted(set(re.findall(r'/api/[A-Za-z0-9_\-/]+', page))))
    print('scripts:', sorted(set(re.findall(r'/_next/static/chunks/[^"\']+\.js', page))))
    i = page.find('action=')
    print('form:', re.findall(r'<form[^>]*>', page))
    print('inputs:', re.findall(r'<input[^>]*>', page)[:20])
    print('textareas:', re.findall(r'<textarea[^>]*>', page)[:5])
    print('selects:', re.findall(r'<select[^>]*>', page)[:5])
    print('buttons:', re.findall(r'<button[^>]*>([^<]{0,40})', page)[:20])
