# Implementation Plan: LIFO 2027 Conference Website

**Branch**: `001-conference-site` | **Date**: 2026-05-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from [spec.md](spec.md)

## Summary

LIFO 2027 web je mostly-statický, content-first marketing + paid ticketing site pre B2B konferenciu, ktorá kombinuje funkčnosť jednoduchej landing page (à la lidskykapital.cz) s plnohodnotným registračno-platobným tokom (Stripe Checkout, B2B fakturácia s DPH, gated tarify cez promo kódy). Stack je optimalizovaný pre **rýchle TTFB**, **mobile-first**, **viacjazyčnosť** (SK + EN pri launchi, roadmapa DE/PL/IT/ES), **editovateľný obsah** bez dev releasu a **vendor lock-in minimalizáciu**. Primárny prístup: **statický build + serverless endpointy** pre interaktívne časti (forms, Stripe webhook). Žiadny vlastný backend server, žiadna vlastná DB v v1 — orchestrácia cez Stripe + Brevo + Netlify Forms + Decap CMS.

## Technical Context

**Language/Version**:
- **TypeScript 5.5+** (typovaná bezpečnosť pre business logiku ticketingu)
- **Node.js 22 LTS** (build prostredie, serverless functions)

**Primary Dependencies**:
- **Astro 5+** — content-first framework, built-in i18n, MDX, image optimization, partial hydration (islands)
- **Tailwind CSS 4+** — utility-first styling s CSS variable-based brand tokens
- **Stripe SDK** (`@stripe/stripe-js` na klientovi, `stripe` na serveri) — Checkout + Webhook + Invoice
- **@react-pdf/renderer** alebo `pdfkit` — server-side generovanie e-ticket PDF
- **Decap CMS** — git-based content editing UI (markdown content collections)
- **Zod** — runtime validácia formulárov a Stripe webhook payloadov
- **Brevo (Sendinblue) SDK** — transakčné emaily + newsletter

**Storage**:
- **Žiadna vlastná DB** v v1 — obsah v markdown súboroch (Astro content collections), platby v Stripe, kontakty v Brevo, formulárové submissions v Netlify Forms inboxe + e-mail notifikácie
- **Postgres / Supabase** je voliteľný upgrade ak vznikne potreba (napr. dashboard pre matchmaking) — out of scope pre v1

**Testing**:
- **Vitest** — unit testy biz logiky (cenové výpočty, promo kód validácia, fakturačné polia)
- **Playwright** — E2E testy kritických tokov (kúpa lístka cez Stripe test mode, odoslanie formulára, prepnutie jazyka)
- **axe-core** — automatizovaný a11y audit
- **Lighthouse CI** — výkon, SEO, a11y skóre (fail < 95)

**Target Platform**:
- **Modern web browsers** (Chrome / Firefox / Safari / Edge — last 2 verzie); IE11 nie je podporovaný
- **Mobile-first** (320px+ šírka), responsive až po 4K
- **Edge runtime** pre serverless endpointy (Netlify Edge Functions alebo Deno-compatible)

**Project Type**:
- **Web application** (static-first + serverless endpoints) — *not* full SPA, *not* traditional server-rendered app

**Performance Goals**:
- **LCP < 2.0s** na 4G; **< 3.0s** na simulovanom 3G (SC-002)
- **TTI < 3.5s** na 4G
- **Lighthouse skóre ≥ 95** pre Performance, A11y, Best Practices, SEO
- **Bundle JS ≤ 50 KB** kritická cesta (gzipped)

**Constraints**:
- **WCAG 2.1 AA** (FR-021); kontrast min 4.5:1 pre body, 3:1 pre veľký text
- **GDPR compliance** — žiadne cookies bez consentu okrem nutných (Stripe session); prefer cookie-less analytics (Plausible)
- **Slovenské DPH** — fakturácia musí spĺňať § 74 zákona o DPH (IČO, DIČ, IČ DPH, dátum dodania, splatnosť, var. symbol)
- **6 jazykov v roadmape** — content model musí izolovať preklad od štruktúry

**Scale/Scope**:
- **Návštevnosť**: stovky až nízke tisíce unikátov mesačne v pre-event období (žiadny viral traffic)
- **Predaj**: ~200–300 vstupeniek pre prvý ročník; očakávaný peak v Early Bird kampani (T-60 dní pred eventom)
- **Obsah**: cca 20–30 markdown súborov (sekcie webu + rečníci + partneri + FAQ) × 2–6 jazykov
- **Build čas**: < 60s pre full rebuild (Astro je rýchly)

## Constitution Check

Constitution dokument v `.specify/memory/constitution.md` je v čase tohto plánu **prázdny template** (žiadne definované princípy). Constitution Check je **vacuously pass** — žiadne gates na vyhodnotenie. Ak v budúcnosti vznikne explicit constitution (cez `/speckit-constitution`), tento plán bude potrebovať re-check.

**Recommended self-imposed principles** (môžu sa neskôr formalizovať do constitution):
- **Statický-first**: každá stránka servuje predovšetkým statické HTML; JS je doplnok, nie predpoklad funkčnosti
- **Vendor lock-in minimalizovať**: každý 3rd-party (Stripe, Brevo, Netlify) má jasnú exit stratégiu (eject → vlastný backend)
- **Brand tokeny izolované**: žiadny hardcoded HEX kód v komponentoch, všetko cez CSS variables
- **Žiadne dáta v repo navyše**: žiadne secrety, žiadne .env v gite; používať Netlify env vars

## Project Structure

### Documentation (this feature)

```text
specs/001-conference-site/
├── spec.md              # Feature specification (DONE)
├── plan.md              # This file (DONE — /speckit-plan)
├── research.md          # Phase 0 output (DONE — /speckit-plan)
├── data-model.md        # Phase 1 output (DONE — /speckit-plan)
├── quickstart.md        # Phase 1 output (DONE — /speckit-plan)
├── contracts/           # Phase 1 output
│   ├── forms-api.md             # Form submission endpoint contracts
│   ├── stripe-webhook.md        # Stripe webhook events handling
│   └── content-collections.md   # Astro content collection schemas
├── checklists/
│   └── requirements.md  # Validation checklist (DONE — /speckit-specify)
└── tasks.md             # Phase 2 output (TODO — /speckit-tasks)
```

### Source Code (repository root)

Štruktúra optimalizovaná pre **Astro web aplikáciu s i18n + content collections + serverless API endpoints**:

```text
.
├── astro.config.mjs           # Astro config (i18n, integrations, build options)
├── tailwind.config.ts         # Tailwind v4 config (brand tokens)
├── tsconfig.json
├── package.json
├── netlify.toml               # Netlify build + redirects + Edge Functions config
├── .env.example               # Sample env vars (no secrets)
│
├── public/                    # Statické assety servované cez CDN
│   ├── favicon.ico
│   ├── favicon-32.png
│   ├── apple-touch-icon-180.png
│   ├── android-chrome-{192,512}.png
│   ├── og-image-1200x630.png
│   ├── og-image-1200x630-en.png
│   ├── twitter-card-1200x600.png
│   ├── fonts/                 # Self-hosted Inter (woff2)
│   └── site.webmanifest
│
├── src/
│   ├── content/               # Astro content collections (markdown / MDX)
│   │   ├── config.ts          # Zod schemas pre collections
│   │   ├── pages/             # Top-level sekcie (hero, about, faq, ...)
│   │   │   ├── sk/
│   │   │   └── en/
│   │   ├── speakers/          # Rečníci (1 markdown / rečník)
│   │   ├── partners/          # Partneri (1 markdown / partner)
│   │   ├── program-blocks/    # Programové bloky
│   │   ├── faq/               # FAQ položky
│   │   └── ticket-tiers/      # Cenové tarify (yaml)
│   │
│   ├── pages/                 # Astro routes (file-based routing)
│   │   ├── index.astro        # SK homepage (default locale)
│   │   ├── [...slug].astro    # Catch-all pre stránky
│   │   ├── en/
│   │   │   └── index.astro    # EN homepage
│   │   ├── api/               # Astro endpoints (serverless)
│   │   │   ├── inquiry.ts     # Inquiry form handler
│   │   │   ├── newsletter.ts  # Newsletter signup handler
│   │   │   ├── checkout.ts    # Vytvorenie Stripe Checkout session
│   │   │   ├── webhook-stripe.ts  # Stripe webhook handler
│   │   │   └── promo-validate.ts  # Promo kód validácia
│   │   └── tickets/
│   │       └── confirmation.astro # Po-platobná potvrdzovacia stránka
│   │
│   ├── components/            # Astro / React (selective islands) komponenty
│   │   ├── Hero.astro
│   │   ├── LanguageSwitcher.astro
│   │   ├── TicketTierCard.astro
│   │   ├── CountdownEarlyBird.astro    # React island (live countdown)
│   │   ├── CheckoutFlow.tsx            # React island (Stripe Elements)
│   │   ├── ContactForm.tsx             # React island (form s Zod)
│   │   ├── NewsletterForm.tsx
│   │   ├── FAQ.astro
│   │   ├── SpeakerCard.astro
│   │   └── PartnerLogo.astro
│   │
│   ├── layouts/
│   │   ├── BaseLayout.astro            # html, head, meta, OG, brand fonts
│   │   └── SectionLayout.astro
│   │
│   ├── lib/                   # Server-side business logic
│   │   ├── stripe.ts                   # Stripe client + helpers
│   │   ├── brevo.ts                    # Brevo API client (newsletter + transactional)
│   │   ├── invoice.ts                  # SK VAT invoice generation
│   │   ├── ticket-pdf.tsx              # E-ticket PDF (react-pdf)
│   │   ├── promo-codes.ts              # Promo kód validačná logika
│   │   ├── pricing.ts                  # Pricing phase resolution (Early Bird vs Regular)
│   │   └── i18n.ts                     # Locale utils (URL routing, fallback)
│   │
│   ├── styles/
│   │   ├── tokens.css                  # Brand CSS variables (single source of truth)
│   │   └── global.css                  # Reset, base styles
│   │
│   └── env.d.ts               # Astro env typings
│
├── tests/
│   ├── unit/                  # Vitest
│   │   ├── pricing.test.ts
│   │   ├── promo-codes.test.ts
│   │   └── invoice.test.ts
│   └── e2e/                   # Playwright
│       ├── ticket-purchase.spec.ts
│       ├── inquiry-form.spec.ts
│       ├── language-switch.spec.ts
│       └── accessibility.spec.ts
│
├── public/admin/              # Decap CMS UI
│   ├── index.html
│   └── config.yml             # Decap config (collections, fields)
│
├── podklady/brand/            # Brand assety (existujú — vygenerované)
│   └── ...                    # (kopírujú sa do public/ pri builde)
│
└── specs/001-conference-site/ # Spec dokumenty (tento priečinok)
    └── ...
```

**Structure Decision**: Astro je content-first framework s vlastným routing-om a content collections — projekt nemá oddelený "frontend" vs "backend"; namiesto toho má **routes** (file-based v `src/pages/`) a **API endpoints** (`src/pages/api/`) ktoré sa kompilujú na serverless functions na Netlify. Toto je explicitne "**single project, web application**" — žiadne mono-repo / multi-app komplikovanie pre v1.

## Complexity Tracking

Žiadne constitution violations. Tabuľka prázdna.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| —         | —          | —                                    |
