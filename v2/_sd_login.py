import urllib.request, urllib.error, json, re, time, http.cookiejar, urllib.parse, socket

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch(url, accept='text/html', method='GET', data=None, headers=None, ctype=None, tries=6):
    u = url if url.startswith('http') else 'https://stabledeliver.com' + url
    h = {'user-agent': UA, 'accept': accept}
    body = None
    if data is not None:
        if isinstance(data, bytes):
            body = data
        elif ctype:
            body = urllib.parse.urlencode(data).encode(); h['content-type'] = ctype
        else:
            body = json.dumps(data).encode(); h['content-type'] = 'application/json'
    if headers: h.update(headers)
    last = None
    for i in range(tries):
        try:
            r = urllib.request.Request(u, data=body, headers=h, method=method)
            resp = op.open(r, timeout=30)
            txt = resp.read().decode('utf-8', 'replace')
            try: j = json.loads(txt)
            except Exception: j = None
            return resp.status, (j if j is not None else txt), resp.headers, resp.geturl()
        except urllib.error.HTTPError as e:
            txt = e.read().decode('utf-8', 'replace')
            try: j = json.loads(txt)
            except Exception: j = txt[:600]
            return e.code, j, e.headers, ''
        except (urllib.error.URLError, socket.gaierror, ConnectionError, OSError) as e:
            last = e
            time.sleep(3 + i * 2)
    raise last

# ---- 1. mail.tm token
st, tok, _, _ = fetch('https://api.mail.tm/token', method='POST',
                      data={'address': 'promptlabhk@uberip.com', 'password': 'Dreamer#2026!PromptLab'},
                      accept='application/json')
TOKEN = tok['token']
print('mail token', st)

# ---- 2. request StableDeliver link
st, body, _, _ = fetch('/api/auth/request-link', method='POST',
                       data={'email': 'promptlabhk@uberip.com'}, accept='application/json')
print('request-link', st, body)

# ---- 3. newest sign-in mail
link_tok = None
deadline = time.time() + 90
while time.time() < deadline and not link_tok:
    time.sleep(4)
    st, msgs, _, _ = fetch('https://api.mail.tm/messages?page=1', accept='application/json',
                           headers={'authorization': 'Bearer ' + TOKEN})
    if not isinstance(msgs, list):
        continue
    for m in sorted(msgs, key=lambda x: x['createdAt'], reverse=True):
        if not m['subject'].startswith('Your StableDeliver'):
            continue
        if time.time() - 0 < 0:
            pass
        st, full, _, _ = fetch('https://api.mail.tm/messages/' + m['id'], accept='application/json',
                               headers={'authorization': 'Bearer ' + TOKEN})
        if not isinstance(full, dict):
            continue
        blob = (full.get('text') or '') + ' '.join(full.get('html') or [])
        mm = re.search(r'auth/verify\?t=([A-Za-z0-9_\-]+)', blob)
        if mm:
            link_tok = mm.group(1)
            print('mail at', m['createdAt'])
            break
print('token', link_tok)
if not link_tok:
    raise SystemExit('no link')

# ---- 4. confirm page then consume (form-urlencoded)
st, page, _, _ = fetch('/auth/verify?t=' + link_tok)
print('confirm page', st, 'has form:', '/api/auth/consume' in str(page))
st, body, hdrs, final = fetch('/api/auth/consume', method='POST', data={'t': link_tok},
                              ctype='application/x-www-form-urlencoded',
                              headers={'referer': 'https://stabledeliver.com/auth/verify?t=' + link_tok,
                                       'origin': 'https://stabledeliver.com'})
print('consume', st, 'final', final, 'len', len(body) if isinstance(body, str) else body)
print('cookies', [(c.name, c.value[:16]) for c in cj])

st, sess, _, _ = fetch('/api/auth/session', accept='application/json')
print('session', st, str(sess)[:400])

with open(r'C:\Users\USER\Documents\Default Project\products\v2\_sd_cookies.json', 'w') as f:
    json.dump([{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path} for c in cj], f, indent=1)
print('cookies saved')
