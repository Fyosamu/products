"""Reusable StableDeliver HTTP session (no browser needed).

Loads the `__Host-sd_session` cookie produced by _sd_login.py.
If the session expires, re-run _sd_login.py (magic link -> mail.tm -> /api/auth/consume).
"""
import urllib.request, urllib.error, json, time, http.cookiejar, urllib.parse, socket, os

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
BASE = 'https://stabledeliver.com'
COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_sd_cookies.json')


def _make_opener():
    cj = http.cookiejar.CookieJar()
    if os.path.exists(COOKIE_FILE):
        for c in json.load(open(COOKIE_FILE)):
            cj.set_cookie(http.cookiejar.Cookie(
                version=0, name=c['name'], value=c['value'], port=None, port_specified=False,
                domain=c['domain'], domain_specified=True, domain_initial_dot=c['domain'].startswith('.'),
                path=c['path'], path_specified=True, secure=c['domain'] == '.stabledeliver.com' or True,
                expires=None, discard=True, comment=None, comment_url=None, rest={}, rfc2109=False))
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)), cj


op, cj = _make_opener()


def fetch(url, accept='application/json', method='GET', data=None, headers=None, ctype=None, tries=6):
    u = url if url.startswith('http') else BASE + url
    h = {'user-agent': UA, 'accept': accept}
    body = None
    if data is not None:
        if isinstance(data, bytes):
            body = data
        elif ctype:
            body = urllib.parse.urlencode(data).encode(); h['content-type'] = ctype
        else:
            body = json.dumps(data).encode(); h['content-type'] = 'application/json'
    if headers:
        h.update(headers)
    last = None
    for i in range(tries):
        try:
            r = urllib.request.Request(u, data=body, headers=h, method=method)
            resp = op.open(r, timeout=40)
            txt = resp.read().decode('utf-8', 'replace')
            try:
                return resp.status, json.loads(txt), resp.headers, resp.geturl()
            except Exception:
                return resp.status, txt, resp.headers, resp.geturl()
        except urllib.error.HTTPError as e:
            txt = e.read().decode('utf-8', 'replace')
            try:
                return e.code, json.loads(txt), e.headers, ''
            except Exception:
                return e.code, txt[:800], e.headers, ''
        except (urllib.error.URLError, socket.gaierror, ConnectionError, OSError) as e:
            last = e
            time.sleep(3 + i * 2)
    raise last


def save_cookies():
    json.dump([{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path} for c in cj],
              open(COOKIE_FILE, 'w'), indent=1)


if __name__ == '__main__':
    st, page, _, url = fetch('/dashboard/products', accept='text/html')
    print('dashboard', st, len(page) if isinstance(page, str) else page, url)
