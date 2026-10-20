# -*- coding: utf-8 -*-
"""Fetch the newest sign-in link from the mail.tm inbox (no third-party deps).

Usage:
  python _getly_login.py token     # print the mail.tm API token
  python _getly_login.py poll 10   # poll up to 10 times, print newest message + links
"""
import json
import sys
import time
import urllib.request

ADDR = "promptlabhk@uberip.com"
PASS = "Dreamer#2026!PromptLab"
API = "https://api.mail.tm"


def req(method, url, body=None, token=None, ctype="application/json"):
    data = None
    if body is not None:
        data = json.dumps(body).encode()
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", ctype)
    if token:
        r.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(r, timeout=30) as resp:
        raw = resp.read()
        try:
            return json.loads(raw)
        except Exception:
            return raw.decode("utf-8", "replace")


def get_token():
    return req("POST", f"{API}/token", {"address": ADDR, "password": PASS})["token"]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if cmd == "token":
        print(get_token())
        return

    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    tok = get_token()
    for i in range(tries):
        msgs = req("GET", f"{API}/messages?page=1", token=tok)
        items = msgs.get("hydra:member", [])
        if items:
            newest = items[0]
            full = req("GET", f"{API}/messages/{newest['id']}", token=tok)
            print("SUBJECT:", full.get("subject"))
            print("FROM:", full.get("from", {}).get("address"))
            print("DATE:", full.get("createdAt"))
            text = full.get("text", "") or ""
            html = full.get("html", "") or ""
            blob = text + "\n" + ("\n".join(html) if isinstance(html, list) else str(html))
            links = []
            for part in blob.replace("=", "").split():
                pass
            import re
            for u in re.findall(r"https?://[^\s\"'<>)]+", blob):
                if "getly" in u and u not in links:
                    links.append(u)
            print("LINKS:")
            for u in links:
                print("  ", u)
            if links:
                return
        print(f"  attempt {i+1}/{tries}: no mail yet")
        time.sleep(5)
    print("NO MAIL")


if __name__ == "__main__":
    main()
