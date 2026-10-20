"""Cross-post the 10 niche prompt packs ($4.99) from Getly to StableDeliver.

Titles/prices come from the live Getly store (hard-coded below, captured 28 Sep 2026),
descriptions from prompt-shop/listings-packs-ready.md (HTML -> plain text),
delivery links = the existing Proton Drive public links from credentials.md §3b.

Idempotent: skips titles that already exist on the account.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _sd_session import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))          # .../Default Project
LISTINGS = os.path.join(ROOT, 'prompt-shop', 'listings-packs-ready.md')

LIVE = {
    'food': "Food, Restaurant & Hospitality Prompt Pack - 368 Prompts for Menus, Recipes, Cafes, Craft Drinks, Hotels & Airbnb",
    'ecommerce': "Ecommerce, Amazon & Shopify Growth Prompt Pack - 546 Prompts for Listings, Product Copy, Dropshipping & Cart Recovery",
    'creative': "Fiction, Screenwriting & Creative Writing Prompt Pack - 702 Prompts for Novels, Comics, D&D, Poetry, Game Dialogue & Podcasts",
    'saas': "SaaS, Startup & AI Tech Marketing Prompt Pack - 631 Prompts for B2B, Pitch Decks, Launches, Market Research & AI Agents",
    'fashion': "Fashion, Beauty & Salon Brand Prompt Pack - 362 Prompts for Streetwear, apparel, makeup, jewelry, barbershop & med-spa marketing",
    'fitness': "Fitness, Wellness & Coaching Prompt Pack - 250 Prompts for Personal trainers, gyms, mindfulness, journaling, health writing & productivity",
    'career': "Resume, Job Search & Personal Brand Prompt Pack - 431 Prompts for Resumes, LinkedIn, cold email, interviews, salary negotiation & hiring",
    'video': "YouTube, TikTok & Reels Video Prompt Pack - 456 Prompts for Scripts, Shorts, hooks, thumbnails, voiceover & streaming",
    'realestate': "Real Estate & Interior Design AI Prompt Pack - 257 Prompts for Listing Photos, Virtual Staging, Home Decor, Architecture & Renovation",
    'etsy': "Etsy Seller & Print-on-Demand Prompt Pack \u2014 411 Prompts for Listings, POD & Handmade Shops",
}

PROTON = {
    'etsy': 'https://drive.proton.me/urls/3G5AQPNFR8#bmw3babeToZl',
    'realestate': 'https://drive.proton.me/urls/CG1PAFECDC#Hq33UOYQfI7r',
    'video': 'https://drive.proton.me/urls/JGBJZVNQN4#t1brRFLvEkrO',
    'career': 'https://drive.proton.me/urls/9EBPQ4883G#7nW3E7EOjEVS',
    'fitness': 'https://drive.proton.me/urls/CFXRHSJEP0#nxaWxHC7Bd7A',
    'fashion': 'https://drive.proton.me/urls/9787S0AXP4#uX71flg8brb7',
    'saas': 'https://drive.proton.me/urls/Z7N4WSQGEC#sQDPXwXCH5mK',
    'creative': 'https://drive.proton.me/urls/DKMT94JHF8#m4m4rTKhJMjH',
    'ecommerce': 'https://drive.proton.me/urls/Y8ZXBB0XPG#R9NIfR4mJLch',
    'food': 'https://drive.proton.me/urls/N53GXV6TJ4#DZSsPmkC1Iqh',
}

PRICE = 4.99


def html_to_text(h):
    h = re.sub(r'</(p|li|h1|h2|h3|h4|div|ul|ol|tr)>', '\n', h, flags=re.I)
    h = re.sub(r'<br\s*/?>', '\n', h, flags=re.I)
    h = re.sub(r'<li[^>]*>', '- ', h, flags=re.I)
    h = re.sub(r'<[^>]+>', '', h)
    lines = [re.sub(r'[ \t]+', ' ', s).strip() for s in html.unescape(h).split('\n')]
    out, prev = [], None
    for s in lines:
        if s == '' and prev == '':
            continue
        out.append(s)
        prev = s
    return '\n'.join(out).strip()


def parse_descriptions():
    src = open(LISTINGS, encoding='utf-8-sig').read()
    blocks = re.split(r'^## \d+\. ', src, flags=re.M)[1:]
    descs = {}
    for b in blocks:
        key = b.split()[0].strip().lower()
        m = re.search(r'\*\*Description \(HTML\):\*\*\s*```html\s*(.*?)\s*```', b, re.S)
        if m:
            descs[key] = html_to_text(m.group(1))
    return descs


def existing_names():
    st, page, _, _ = fetch('/dashboard/products', accept='text/html')
    if not isinstance(page, str):
        return set()
    out = set()
    starts = [m.start() for m in re.finditer(r'<div class="rounded-xl border', page)]
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(page)
        txt = re.sub(r'<[^>]+>', ' | ', page[s:e])
        txt = re.sub(r'(\s*\|\s*)+', ' | ', txt).strip(' |')
        m = re.match(r'(.*?)\s*\|\s*(?:\$|live|draft|paused)', txt)
        if m:
            out.add(html.unescape(m.group(1)).strip())
    return out


def main():
    descs = parse_descriptions()
    print('descriptions parsed:', sorted(descs))
    have = existing_names()
    print('existing on StableDeliver:', len(have))

    created, skipped, failed = [], [], []
    for key, title in LIVE.items():
        if title in have:
            skipped.append(key)
            continue
        body = {
            'name': title,
            'description': descs.get(key, ''),
            'price': '%.2f' % PRICE,
            'priceCurrency': 'USD',
            'asset': 'USDT',
            'chain': 'bsc',
            'deliveryType': 'link',
            'link': PROTON[key],
            'keys': '',
            'telegramGroup': '',
        }
        st, resp, _, _ = fetch('/api/dashboard/products', method='POST', data=body,
                               headers={'origin': 'https://stabledeliver.com',
                                        'referer': 'https://stabledeliver.com/dashboard/products'})
        if st in (200, 201):
            created.append([key, resp.get('id') if isinstance(resp, dict) else resp])
            have.add(title)
        else:
            failed.append([key, st, str(resp)[:250]])

    print('CREATED', len(created))
    for c in created:
        print('  +', c)
    print('SKIPPED (already live)', skipped)
    print('FAILED', failed)


if __name__ == '__main__':
    main()
