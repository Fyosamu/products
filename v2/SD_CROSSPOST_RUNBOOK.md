# StableDeliver cross-post — batch v2 (10 products) · runbook ✅ COMPLETE (28 Sep 2026)

StableDeliver = **0% fee, 10 free orders/month**, payout USDT **BEP-20** →
`0xE1E3e1c2978c74f43Bb095023135C3278303aF34`. Nothing here costs money.

## Result
- **28 products live on StableDeliver = full parity with Getly** (8 original + 10 batch-v2
  + 10 niche packs). Every one verified: `GET /c/<uuid>` → 200 and the right price renders.
- **11 duplicates deactivated** (`PATCH … {"active":false}`): `09621caf-…` (Client Invoice kit)
  plus 10 pack copies this session created because `_sd_create_packs.py` compared titles on
  `-` while the canonical set (already documented in credentials §3) uses `—`.
  **Lesson: normalise dashes/whitespace/HTML entities before deduping.**
- All 28 delivery links = Proton Drive public share links (all returned 200 on 28 Sep 2026).

| Product | Price | StableDeliver checkout |
|---|---:|---|
| Client Invoice and Quote Kit 2026 | $12.00 | https://stabledeliver.com/c/fe0c5806-a5de-4ee3-ac6f-665a106ef38c |
| Content Calendar and Social Media Planner 2026 | $12.00 | https://stabledeliver.com/c/52943d1f-a9ba-461f-87b2-c74f4073251f |
| Personal Budget and Savings Tracker 2026 | $12.00 | https://stabledeliver.com/c/ab281b01-09b7-4dd9-b84c-2fd2ae0e8746 |
| Client CRM and Project Tracker | $14.00 | https://stabledeliver.com/c/95bdcd53-f710-47b5-8a2f-8e2286a460a1 |
| 150 AI Video, Reels & YouTube Script Prompts | $7.99 | https://stabledeliver.com/c/9c7b642f-4fcb-4e26-83eb-2ed22b112b83 |
| 120 Cold Outreach & Sales Prompts | $7.99 | https://stabledeliver.com/c/e90f24cd-1a02-4d68-9703-3644619e5c08 |
| 120 Job Search Prompts | $7.99 | https://stabledeliver.com/c/c71b7e61-205c-40d7-9082-0cb172abbf2a |
| 390 AI Prompt Mega Pack | $14.99 | https://stabledeliver.com/c/32de4574-1424-447a-bde2-818569df39ab |
| The Ultimate Printable Planner 2026 | $9.00 | https://stabledeliver.com/c/db06404c-daaf-4246-95c3-62ede5796272 |
| Resume and Cover Letter Kit 2026 | $9.00 | https://stabledeliver.com/c/9cc99bac-6e4b-4ad2-979a-458edc181d67 |

## How it was done (reusable)

### Step 1 — StableDeliver login (headless, no browser) ✅
- `products/v2/_sd_login.py`: `POST /api/auth/request-link` → read the magic link from
  **mail.tm** → `GET /auth/verify?t=` → `POST /api/auth/consume`
  (`application/x-www-form-urlencoded`, `t=<token>`) → 302 to `/dashboard`.
- Cookie `__Host-sd_session` saved to `products/v2/_sd_cookies.json`.
- Links are **one-time, 15 min**. `GET /api/auth/session` is *not* a route (404) — test auth
  with `GET /dashboard/products` instead.
- Reusable helper: `products/v2/_sd_session.py` → `fetch(path, accept, method, data, headers)`.

### Step 2 — Proton Drive upload ✅ 10/10
- Account `dreamerpromptlab@proton.me`, root folder (`drive.proton.me/u/1/…/folder/…`).
- Method: `browser.snapshot({tabID, depth:20})` → ref of `[main]` →
  `browser.files.drop({tabID, ref, paths})` (max 8 paths, ≤5 MiB each).
  `UnknownVizError` → just retry. Close the transfers panel first
  (`button: Close transfers`, clicked via `browser.evaluate`).
- The file list is **virtualized** — rows outside the viewport do not exist in the DOM.
  Scroll `.flex-1.overflow-auto` (set `scrollTop`) until the target row appears.
- Storage after all 10: ~6.3 MB / 5 GB.

### Step 3 — public share links ✅ 10/10 → `products/v2/_sd_proton_links.json`
Per file: click the row activator (`[data-item-activator]`) → toolbar
`[data-testid=toolbar-share-link]` → in the panel click the **label**
(`label[data-testid=toggle-switch]` inside `[data-testid=share-modal-shareWithAnyoneSection]`,
*not* the hidden checkbox input — `input.click()` does nothing) → wait ~6 s for
`Public link / Active` → read the `https://drive.proton.me/urls/XXX#KEY` input value →
`[data-testid=modal:close]`.

### Step 4 — create the products (headless) ✅
- `POST /api/dashboard/products`, `content-type: application/json`
  **+ `origin` and `referer: https://stabledeliver.com`** — without those headers the API
  answers **`403 forbidden`**.
- Body: `{name, description, price:"12.00", priceCurrency:"USD", asset:"USDT",
  chain:"bsc", deliveryType:"link", link:<Proton url>, keys:"", telegramGroup:""}`
  → `{"ok":true,"id":"<uuid>"}`.
  (`chain` ids: `tron|polygon|bsc|arbitrum|ethereum|bitcoin|solana`; `bsc` = BNB Smart Chain.)
- Scripts: `_sd_payload.json` (titles/prices/descriptions), `_sd_proton_links.json`,
  `_sd_create.py` (idempotent, skips names already on the account),
  `_sd_verify.py` (re-lists every product with price/status/checkout URL).

## Housekeeping done
- `prompt-shop/credentials.md` §3 (28 checkout links + API recipe + deactivated-ID list),
  §3b (batch-v2 link table), §5 (StableDeliver 28, Getly 28) — mirrored to
  `C:\Users\USER\Documents\_prompt-shop_backup\`.
- **Getly re-checked 28 Sep 2026:** `GET /api/stores/dreamer-prompt-lab-muifdken` →
  **28 products, all `active`** (4 extra $4.99 packs — SaaS / Fiction / Ecommerce / Food —
  added by a parallel session). Telegram mirror auto-syncs hourly.

## Watch-outs
- StableDeliver free tier = **10 orders/month**; 28 products are live, so the cap is orders,
  not listings.
- If a delivery link is ever changed: `PATCH /api/dashboard/products/<id> {"link":"<url>"}`.
- Existing orders keep their original terms — editing never touches past sales.
