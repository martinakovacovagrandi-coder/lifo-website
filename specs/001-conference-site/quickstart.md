# Quickstart: LIFO 2027 Web

**Date**: 2026-05-12 | **Plan**: [plan.md](plan.md)

Sprievodca pre vývojára / koordinátora ako rozbehnúť, editovať a deploynúť LIFO web.

---

## Prerequisites

| Tool       | Version           | Why                                  |
| ---------- | ----------------- | ------------------------------------ |
| Node.js    | 22 LTS            | Astro build, dev server               |
| npm / pnpm | latest            | Package manager                       |
| Git        | 2.30+             | Version control, Netlify deploy      |
| VS Code    | optional          | Recommended editor                    |
| Stripe CLI | latest            | Webhook testing                       |

**Účty** (potrebné keys / config):
- **Netlify** — hosting + Forms + Functions
- **Stripe** — payments (test mode pre dev)
- **Brevo** — newsletter + transakčné maily
- **Plausible** — analytics (cloud-hosted)
- **GitHub** — repo + Decap auth

---

## First-time setup (dev)

```bash
# 1. Clone repo
git clone <repo-url>
cd lifo-website

# 2. Install dependencies
npm install

# 3. Copy env vars sample → .env (local)
cp .env.example .env
# Vyplniť STRIPE_SECRET_KEY (test mode), BREVO_API_KEY, atď.

# 4. Run dev server
npm run dev
# → http://localhost:4321

# 5. (Optional) Run Stripe webhook listener
stripe listen --forward-to localhost:4321/api/webhook-stripe
# Skopíruj signing secret do .env: STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Available scripts

```bash
npm run dev          # Astro dev server (HMR)
npm run build        # Production build → dist/
npm run preview      # Preview production build lokálne
npm run check        # Astro check (Zod schema validation, TypeScript)
npm run lint         # ESLint
npm run format       # Prettier
npm run test         # Vitest unit tests
npm run test:e2e     # Playwright E2E tests (Stripe test mode)
npm run a11y         # axe-core a11y audit
npm run lighthouse   # Lighthouse CI
```

---

## Pridanie nového rečníka

**Cesta 1 — Decap CMS UI** (pre koordinátora / netechnického používateľa):

1. Otvor `https://lifo.urbanlama.eu/admin/`.
2. Prihláste sa cez GitHub (account musí byť pridaný ako collaborator v repo).
3. Klik **Rečníci** → **Nový**.
4. Vyplň polia (meno, pozícia, organizácia, foto, bio).
5. Vyber programový blok (panel/keynote).
6. **Status: confirmed** (až keď je rečník skutočne potvrdený).
7. Klik **Publish** → automatický git commit → Netlify rebuild → live do 2 minút.

**Cesta 2 — Markdown ručne** (pre vývojára):

1. Vytvor `src/content/speakers/sk/janusz-michalek.md`:
   ```markdown
   ---
   name: "Janusz Michałek"
   role: "CEO"
   organization: "Katowicka Specjalna Strefa Ekonomiczna"
   photo: "./images/janusz-michalek.jpg"
   panelAssignment: "panel-investments"
   order: 1
   status: confirmed
   locale: sk
   ---

   Janusz vedie 30 rokov najúspešnejšiu SEZ v strednej Európe.
   Ako lákať investorov do regiónu — case studies z poľského Górnego Śląska.
   ```
2. Vytvor zodpovedajúci EN variant v `src/content/speakers/en/janusz-michalek.md`.
3. Commit + push → Netlify rebuild.

---

## Pridanie nového partnera

Rovnaký pattern ako rečník, ale do `src/content/partners/`. Formát yaml, nie markdown (nemá bio):

```yaml
# src/content/partners/example-corp.yaml
name: "Example Corp"
tier: "hlavny"
logo: "./logos/example-corp.svg"
websiteUrl: "https://example.com"
order: 2
status: confirmed
```

Logo nahrať do `src/content/partners/logos/` (Decap UI alebo manuálne). **Preferuj SVG**; ak raster, min 240×80 px.

---

## Pridanie / úprava cien tarif (Stripe)

LIFO tarify NIE SÚ v markdowne — sú v Stripe (single source of truth).

**Pridanie novej fázy ceny**:

1. Stripe Dashboard → Products → vyber tarifu (napr. "LIFO 2027 — Samospráva").
2. Pridaj novú Price (alebo deaktivuj starú a vytvor novú):
   - Amount: napr. 29000 (cents = 290 €)
   - Currency: EUR
   - Metadata: `phase=regular`, `phase_start=2026-11-01T00:00:00Z`
3. **Active: false** zatiaľ (aktivovať keď skončí Early Bird).
4. V čase prepnutia (manuálne alebo cron):
   - Deaktivovať `phase=earlybird` Price.
   - Aktivovať `phase=regular` Price.

Stránka automaticky načíta aktívnu Price pri každom build / SSR call.

**Pridanie nového promo kódu**:

1. Stripe Dashboard → Products → Promotion codes → Create.
2. Code: napr. `LIFO27-VIP-INVITE`.
3. Restrictions: `Applies to: [LIFO 2027 — VIP]`.
4. Max redemptions: 50.
5. Expires: 2027-01-15.

---

## Deploy workflow

```text
local dev ─┐
           │
           ▼
       git push origin feature-branch
           │
           ├─► Netlify auto-builds → preview URL pre review
           │
       Open PR
           │
       (Review)
           │
       Merge to main
           │
           ▼
       Netlify auto-builds → produkcia
       https://lifo.urbanlama.eu
```

Build trvá ~ 60s. Rollback: `git revert <commit>` → push → nový build → starý content živý.

---

## Environment variables (Netlify env)

| Variable                          | Where                | Required          |
| --------------------------------- | -------------------- | ----------------- |
| `STRIPE_SECRET_KEY`               | Stripe dashboard      | Production: live  |
| `STRIPE_PUBLISHABLE_KEY`          | Stripe dashboard      | Public (in HTML)  |
| `STRIPE_WEBHOOK_SECRET`           | Stripe → Webhooks    | Production        |
| `BREVO_API_KEY`                   | Brevo account        | Always            |
| `BREVO_NEWSLETTER_LIST_ID`        | Brevo lists          | Always            |
| `BREVO_NOTIFICATION_EMAIL`        | env                  | Always            |
| `PLAUSIBLE_DOMAIN`                | env                  | Always            |
| `ETICKET_JWT_SECRET`              | generated, env       | Always            |
| `NETLIFY_BLOBS_TOKEN`             | Netlify (auto)        | Idempotency cache |
| `SITE_BASE_URL`                   | env                  | Always            |

**Nikdy** nekommitnúť `.env` súbor — len `.env.example` so sample (prázdnymi) hodnotami.

---

## Testing

### Unit tests

```bash
npm run test
# Run specific:
npm run test -- pricing
```

Pokrytie:
- `src/lib/pricing.ts` — Early Bird vs Regular vs Last-minute resolution
- `src/lib/promo-codes.ts` — validation, redemption tracking
- `src/lib/invoice.ts` — SK VAT compliance (povinné polia)
- `src/lib/i18n.ts` — URL routing, fallback chain

### E2E tests

```bash
npm run test:e2e
```

Pokrytie:
- **`ticket-purchase.spec.ts`** — happy path: pick tier → checkout → Stripe test card → confirmation → e-ticket email
- **`promo-code.spec.ts`** — gated tier flow: bez kódu nie je viditeľná → s kódom viditeľná → kúpa OK
- **`inquiry-form.spec.ts`** — kontaktný formulár (každý segment), validation errors
- **`language-switch.spec.ts`** — prepnúť SK → EN → zachovať kontext stránky
- **`accessibility.spec.ts`** — axe-core sweep na všetkých pages, fail na critical violations

### Lighthouse CI

```bash
npm run lighthouse
```

Spustí Lighthouse na `http://localhost:4321` + produkciu, generuje report. Fail na score < 95.

---

## Common tasks

### Aktualizovať dátum konferencie

`src/content/pages/sk/hero.md` a `en/hero.md`:
```yaml
---
title: "LIFO 2027"
description: "11. 2. 2027 · Hotel Clarion Bratislava"
---
```

Pri zmene dátumu globálne: skontrolovať aj `astro.config.mjs` (site title / meta), OG image (regenerate cez `podklady/brand/_tooling/build.py`).

### Aktualizovať logo / brand kit

Súbory v `podklady/brand/` sa pri build-e kopírujú do `public/`. Workflow:

1. Pri dodaní finálneho brand kit-u od grafika nahrať súbory do `podklady/brand/01_master/`, `02_variants/`, `04_web_assets/` (override).
2. Aktualizovať `tokens.css` s presnými HEX kódmi (ak sa zmenili).
3. Spustiť `podklady/brand/_tooling/build.py` pre regeneráciu raster exportov (alebo nahrať aj raster ručne ak grafik dodá kompletnú sadu).
4. Commit + push → auto-deploy.

### Aktualizovať FAQ

Decap CMS UI → FAQ → Edit. Alebo ručne v `src/content/faq/sk/{nazov}.md`.

### Otestovať Stripe webhook lokálne

```bash
# Terminal 1
npm run dev

# Terminal 2
stripe listen --forward-to localhost:4321/api/webhook-stripe
# → poznač whsec_xxx do .env

# Terminal 3 — trigger
stripe trigger checkout.session.completed
```

Skontroluj logy v Terminal 1 — webhook bol prijatý, e-ticket vygenerovaný (skontroluj Mailtrap inbox alebo Brevo logs).

---

## Tro fixujte

| Problem                                                      | Riešenie                                                                         |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| `npm install` zlyhá na Windows kvôli `sharp`                | Aktualizuj Node na 22 LTS; ak pretrváva, `npm install --include=optional sharp` |
| Decap CMS UI nesa otvorí                                     | Skontroluj GitHub OAuth callback URL v Netlify settings                          |
| Stripe webhook signature mismatch                            | Skontroluj `STRIPE_WEBHOOK_SECRET` v Netlify env vars                            |
| Lighthouse skóre < 95                                        | Skontroluj nepotrebné JS bundles cez `npm run build && open dist/stats.html`     |
| Build padá na "FK violation in program block"                | Skontroluj že všetky `speakerSlugs` v program-blocks existujú v `speakers/`     |
| E-ticket nepríjde po test purchase                           | Skontroluj Brevo logs + idempotency KV; manuálne resend cez Stripe dashboard    |

---

## Ďalšie kroky

Tento quickstart pokrýva **v1 ošetrenie**. Pre rozšírenia (live event app, check-in scanner, dashboard pre matchmaking) doplniť do `/speckit-specify` ako nový spec.
