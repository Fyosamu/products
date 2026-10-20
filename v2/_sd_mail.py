import urllib.request, urllib.error, json, time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def jreq(url, method='GET', data=None, headers=None):
    h = {'user-agent': UA, 'accept': 'application/json'}
    if data is not None: h['content-type'] = 'application/json'
    if headers: h.update(headers)
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=30)
        raw = resp.read().decode('utf-8', 'replace')
        try: return resp.status, json.loads(raw)
        except Exception: return resp.status, raw[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300].decode('utf-8', 'replace')

st, tok = jreq('https://api.mail.tm/token', 'POST', {'address': 'promptlabhk@uberip.com', 'password': 'Dreamer#2026!PromptLab'})
TOKEN = tok.get('token')
print('token', st)
st, msgs = jreq('https://api.mail.tm/messages?page=1', 'GET', None, {'authorization': 'Bearer ' + TOKEN})
print('msgs', st, type(msgs))
items = msgs.get('hydra:member', []) if isinstance(msgs, dict) else []
print('count', len(items))
for m in items[:5]:
    print(m.get('createdAt'), m.get('from', {}).get('address'), '|', m.get('subject'), '|', m['id'])
