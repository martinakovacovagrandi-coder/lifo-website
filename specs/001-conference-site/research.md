# Research: LIFO 2027 Conference Website

**Phase 0** | **Date**: 2026-05-12 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Účel

Tento dokument obsahuje **rozhodnutia** o technológii a **rationale** pre každú voľbu. Slúži ako referencia pre `/speckit-tasks` a budúcich vývojárov. Žiadne otvorené [NEEDS CLARIFICATION] markery — všetky technické nejasnosti sú rozriešené pred prechodom na Phase 1.

---

## 1. Framework / Static Site Generator

**Decision**: **Astro 5+**

**Rationale**:
- LIFO web je z 90 % statický obsah (marketing) + 10 % interaktivita (ticketing flow, forms, language switch). Astro je optimalizovaný presne na tento mix — defaultne statický HTML, JS sa hydratuje len pre tzv. "islands" (interaktívne komponenty).
- Built-in i18n routing v Astro 4+ (`astro.config.mjs` → `i18n: { locales: ['sk', 'en'], defaultLocale: 'sk' }`) — neobsahuje žiadny i18n boilerplate; podporuje hreflang automaticky.
- Content collections s Zod schemami → typovaná štruktúra obsahu (rečníci, partneri, FAQ) v markdown / MDX.
- Image optimization (`<Image>` komponent) — automatické responsive `<picture>`, lazy load, WebP/AVIF fallback.
- Framework-agnostic islands — pri ticketing UI môžeme použiť React (pre Stripe Elements). Pri jednoduchých interakciách stačí vanilla.
- Build je rýchly (10–30s pre projekt LIFO veľkosti).

**Alternatives considered**:
- **Next.js (App Router)**: Skvelé pre SPA / app-like, ale overkill pre content-first marketing site. Server Components + RSC = väčší JS bundle. SEO / static gen je slabší než Astro.
- **Eleventy (11ty)**: Najminimalistickejší, pure static. Ale chýba mu modernou DX (TypeScript native, content collections, image optimization out-of-box). Pre ticketing flow by sme potrebovali zlepiť rôzne knižnice.
- **SvelteKit**: Konkurent Astro, podobné výsledky. Ale eco-system pre Stripe / Decap / brand tooling je o niečo užšie. Preferuje React-y front-end pre Stripe Elements (oficiálne podporované).
- **Nuxt 3 (Vue)**: Podobné Next.js. Tím má pravdepodobne väčšiu React expozíciu.

---

## 2. Hosting + Build platforma

**Decision**: **Netlify**

**Rationale**:
- **Netlify Forms** — native handling formulárov bez vlastného backendu (FR-014, FR-015): submission → e-mail notifikácia organizátorom + uložené v Netlify inbox UI. Free tier 100 submissions/mesiac (dostatočné pre lead-gen objem; upgrade ak treba).
- **Netlify Edge Functions** alebo Functions (Lambda-on-Netlify) — pre Stripe Checkout / webhook endpointy.
- **Built-in CDN** s automatickým HTTPS, Brotli compression, image CDN.
- **Decap CMS** integrácia natívna (Decap pôvodne Netlify CMS).
- **Branch previews** — každý PR má auto-generated preview URL pre review.
- **GDPR-friendly**: dáta v Netlify EU regions; bez ďalšieho US data transfer.

**Alternatives considered**:
- **Vercel**: Skoro identický feature-set. Edge functions sú o niečo bohatšie. Ale Vercel Forms je za paywall-om (Vercel paid plán), Netlify Forms je free. Pre LIFO objem submissions Netlify šetrí náklady.
- **Cloudflare Pages**: Najlacnejší + najrýchlejší CDN. Ale form handling nemá native, treba Worker. Decap integrácia tiež manuálnejšia.
- **Vlastný server (DigitalOcean, Hetzner)**: Maximum kontroly, ale ops overhead je out of scope pre v1.

---

## 3. CMS / Editovanie obsahu

**Decision**: **Decap CMS** (drží markdown súbory v git repo)

**Rationale**:
- FR-027 vyžaduje editovateľnosť bez dev releasu. Decap rieši toto: organizátor (Martina, koordinátorka, marketing) sa prihlási do `/admin/`, edituje markdown v UI; uloženie = git commit + auto-deploy cez Netlify.
- **Žiadny vendor lock-in**: obsah je markdown v repo, nie v cudzej DB. Ak Decap zanikne, presunúť obsah znamená iba opustiť `/admin/` UI.
- **Free a self-hosted** (UI je JS bundle, žiadny SaaS poplatok).
- Integrácia s GitHub auth — vstavané OAuth.
- **Limity**: UI je menej polished než Sanity / Contentful; nie pre netechnické "obohatené blog" obsahy. Pre štruktúrovaný obsah (rečníci, partneri, ticket tarify) je úplne adekvátne.

**Alternatives considered**:
- **Sanity.io**: Najpolish-nutejší CMS s vlastným query language (GROQ). Free do 3 users, paid plán $99/mes pre väčší tím. Sanity Studio je výborné UI. Trade-off: obsah žije v Sanity cloud, nie v repo → vendor lock-in. Pre LIFO scope (malý tím, content tier nie extrémny) Decap stačí.
- **Contentful**: Enterprise headless CMS. Drahší (od $300/mes pre Pro). Overkill pre LIFO.
- **Strapi (self-hosted)**: Vlastný backend. Vyžaduje DB + hosting Strapi servera. Žiadny benefit oproti Decap pre tento scope.
- **Markdown only (no UI)**: Najjednoduchšie, ale organizátor by musel ovládať git / VS Code. Nedosažiteľné pre non-tech tím (FR-027 by zlyhal v praxi).

---

## 4. Payment / Ticketing

**Decision**: **Stripe Checkout + Stripe Customer Portal**

**Rationale**:
- **Native B2B support**: Stripe Tax + Stripe Invoicing podporuje slovenskú DPH, IČO/DIČ na invoice. Sequential invoice numbering. PDF invoice doručený auto cez e-mail.
- **3-D Secure / SCA** vstavané — žiadny custom flow.
- **Promo codes nativne**: Stripe podporuje "Promotion codes" so všetkými vlastnosťami z FR-041 (limit použití, expiry, viazanie na konkrétnu cenu / tarifu, % alebo fixná zľava).
- **Multi-currency**: EUR default, ale podpora pre USD / GBP ak vznikne (zahraniční sponzori).
- **Webhook**: jasné dokumentovanie event-ov (`checkout.session.completed`, `invoice.paid`, atď.) → reliable backend logic.
- **Slovakia podporovaný trh**, sadzby 1.4% + €0.25 pre EU karty (rozumné na B2B objem).
- **Test mode** — bezplatné testovanie celého flow s testovacími kartami pred go-live.

**Alternatives considered**:
- **Eventbrite / Ticketmaster pre B2B**: Hotové ticketing platformy. Trade-off: nemajú kontrolu nad gated tarifami (FR-041a — skrytá tarifa odomknutá kódom), branding je obmedzený, B2B fakturácia obmedzená. Eventbrite čerpá ~3.5% + €0.79 per ticket — drahšie. Stripe je lepší fit.
- **Smartbillet / Tixly / Inviton (lokálne SK ticketing)**: Lokálna SK fakturácia out of the box, ale integrácia s vlastným webom je obmedzená (väčšinou iframe widget); kontrola nad UX/branding limitovaná. Vhodnejšie pre kultúrne podujatia (kiná, divadlá).
- **PayPal**: B2B fakturácia obmedzená v SK; vyššie fees; horšia DX.
- **Lokálne karta brány (Trust Pay, Besteron, GP webpay)**: Native SK, ale slabšia DX a horšia integrácia s modernými frameworkmi. Stripe ich premieňa na čisté Stripe-call. Pre v1 nadbytočné.

---

## 5. Faktúry (slovenská DPH compliance)

**Decision**: **Stripe Invoicing** v v1, hook pre účtovný export

**Rationale**:
- Stripe Invoicing podporuje § 74 zákona o DPH (povinné náležitosti: identifikácia dodávateľa/odberateľa, IČO, DIČ, IČ DPH, dátum dodania, dátum splatnosti, sadzba DPH, suma).
- Sequential numbering nativne (`INV-{YYYY}-{NNNN}`).
- PDF doručený automaticky e-mailom kupujúcemu.
- Žiadne ďalšie účtovné systémy v v1.

**Pre SK účtovníctvo (mimo Stripe)**:
- Mesačný export Stripe invoices (CSV / API) → import do **SuperFaktura** / **iDoklad** / **Fakturoid** / účtovníckeho SW
- Voliteľný direct integration ak vznikne objem, ktorý opodstatňuje (out of scope v1)

**Alternatives considered**:
- **SuperFaktura priama integrácia**: SuperFaktura má REST API. Trade-off: nezvláda payment flow, len fakturovanie. Treba párovať Stripe payment s SuperFaktura invoice → komplexita. Stripe vlastné invoice je dostatočné, manuálny mesačný transfer do účtovníctva je v1-ready.
- **Vlastný PDF generator + custom invoice numbering**: Override Stripe nemá zmysel. Stripe rieši compliance.

---

## 6. Forms (kontaktný, aplikačný, newsletter signup)

**Decision**: **Netlify Forms** + **Brevo (newsletter)**

**Rationale**:
- **Netlify Forms**: zero-setup. Astro form `<form name="inquiry" netlify>` → Netlify zachytí submission, e-mail notif + UI inbox. Vstavané spam filtering (honeypot, akismet).
- **Brevo**: pre newsletter signup, double opt-in, GDPR template, transakčné emaily (e-ticket delivery, formulárové notifikácie).

**Alternatives considered**:
- **Formspree**: Podobné Netlify Forms, ale extra vendor + free tier nižší.
- **Vlastný API endpoint + DB**: Zbytočná komplexita pre v1. Netlify Forms eliminuje potrebu vlastnej DB pre lead capture.
- **Mailchimp**: US-based, GDPR má, ale Brevo (EU-based) je čistejší.

---

## 7. Newsletter + transakčné emaily

**Decision**: **Brevo (formerly Sendinblue)**

**Rationale**:
- **EU-based** (Paríž) → GDPR čistejšie, menej DPA dokumentov.
- Free tier 300 emails/deň → adekvátne pre lead-gen objem.
- API pre transakčné emaily (e-ticket, invoice link, inquiry notifikácie organizátorom).
- Newsletter zoznamy s tagovaním podľa segmentov (Partner / Samospráva / Investor) → cielená komunikácia.
- Double opt-in nativne.

**Alternatives considered**:
- **Mailchimp**: US-based, vyžaduje SCC pre EU export.
- **Postmark**: Skvelé pre transakčné, ale draho a chýba marketing UI.
- **Resend**: Nový hráč, dev-friendly, ale chýba marketing automation.

---

## 8. i18n stratégia

**Decision**: **Astro built-in i18n** + **markdown content collections per locale**

**Rationale**:
- Astro routing `/sk/program/`, `/en/program/` cez `i18n` config.
- Content collections per-locale: `src/content/pages/sk/`, `src/content/pages/en/`.
- Fallback: ak EN preklad chýba, zobrazí SK s vizuálnym indikátorom "Translation pending" (FR-028e).
- `<link rel="alternate" hreflang="...">` generované automaticky.
- Pre roadmapu DE/PL/IT/ES — pridanie ďalšieho jazyka je: 1 row v `astro.config.mjs` + nový priečinok v `src/content/pages/{xx}/`. Žiadny refaktor.

**Alternatives considered**:
- **astro-i18next**: bohatšie API (interpolácia, pluralizácia), ale ťažšie pre markdown-only obsah. Pre FAQ / hero text Astro built-in stačí.
- **Vlastný i18n hook**: zbytočný overhead.

---

## 9. Analytics

**Decision**: **Plausible Analytics** (cloud-hosted EU)

**Rationale**:
- **Cookie-less** — žiadny cookie banner kvôli analytike (GDPR-friendly out of box).
- EU-hosted (Estónsko / Nemecko, podľa plánu).
- Lightweight JS (< 1 KB).
- $9/mes pre 10k pageviews — primerané.
- Custom events pre conversion tracking (Stripe Checkout success, Newsletter signup).

**Alternatives considered**:
- **GA4**: Free, ale GDPR komplikácie (Google Consent Mode, US data transfer SCC). Ťažký script (~ 50 KB). Príliš veľký overhead pre marketing site.
- **Umami (self-hosted)**: Open-source ekvivalent Plausible. Treba si hostovať. Pre v1 cloud-hosted Plausible je rýchlejší rollout.
- **Vercel Analytics / Netlify Analytics**: Drahšie a obmedzenejšie.

---

## 10. PDF e-ticket generation

**Decision**: **@react-pdf/renderer** v Astro endpoint (server-side)

**Rationale**:
- Po Stripe Checkout success → webhook → vygeneruje PDF e-ticket → pošle cez Brevo transakčný email.
- @react-pdf/renderer je deklaratívne (React komponenty pre PDF), ovládať style cez CSS-in-JS.
- QR kód na e-tickete cez `qrcode` npm package → unikátny check-in token.
- Vygenerovaný PDF nahrať do Stripe Customer Portal alebo Brevo email attachment.

**Alternatives considered**:
- **pdfkit**: nižšieúrovňový API, viac práce.
- **Puppeteer/Playwright HTML → PDF**: heavy (Chromium download), pomalé na serverless.
- **Stripe receipt only**: nemá branding ani QR kód. Pre check-in v deň eventu potrebujeme vlastný e-ticket.

---

## 11. Doména a hosting setup

**Decision**: **Doména: `lifo.urbanlama.eu`** (subdoména existujúcej domény `urbanlama.eu` registrovanej u zadávateľky)

**App hosting**: Netlify (per #2)

**DNS**: **Webglobe panel** (kde `urbanlama.eu` je hostovaná). Webglobe je primárne PHP/MySQL shared hosting → nepodporuje Node.js serverless funkcie potrebné pre Stripe webhook + Astro API endpointy. Preto **aplikácia žije na Netlify**, Webglobe slúži len ako **DNS broker** pre subdoménu.

**Action plan pre go-live (DNS + HTTPS)**:

1. **V Netlify projekte** pridať custom domain `lifo.urbanlama.eu`:
   - Settings → Domain management → Add custom domain → zadať `lifo.urbanlama.eu`
   - Netlify vygeneruje cieľovú hodnotu pre CNAME (typicky `<site-name>.netlify.app` alebo `apex-loadbalancer.netlify.com`)

2. **V Webglobe DNS paneli** (zóna pre `urbanlama.eu`) pridať:
   ```
   Type:  CNAME
   Name:  lifo
   Value: <vygenerovaná hodnota z Netlify>
   TTL:   3600 (1 hod) alebo default
   ```
   Pri prvom verifikačnom kroku môže Netlify vyžadovať aj `TXT` záznam pre vlastníctvo — tiež pridať podľa pokynov.

3. **Počkať na DNS propagation** (5 min – 24 h; typicky pod 30 min). Test:
   ```bash
   nslookup lifo.urbanlama.eu
   # alebo
   dig lifo.urbanlama.eu
   ```

4. **Let's Encrypt cert** sa vystaví automaticky cez Netlify v priebehu pár minút po úspešnej DNS verifikácii. **Žiadna manuálna SSL inštalácia na Webglobe** sa nevyžaduje.

5. **HSTS** zapnúť v Netlify (Settings → Domain → HTTPS → Force HTTPS).

**E-maily** (info@, kontakt@):
- Pravdepodobne už existujú na `urbanlama.eu` cez Webglobe mail.
- Pre LIFO odporúčam **použiť existujúce schránky** (napr. `lifo@urbanlama.eu` ako alias) — netreba nový tenant.
- **Transakčné maily** (e-ticket, faktúra) **idú cez Brevo** z `noreply@urbanlama.eu` alebo `tickets@urbanlama.eu` — Brevo bude potrebovať SPF + DKIM záznamy v Webglobe DNS pre legitímne doručovanie. Pridanie SPF/DKIM je 2 TXT záznamy v paneli.

**Budúci ročník**: ak sa LIFO rozbehne a vznikne potreba samostatnej domény (`lifoforum.sk` alebo `localinnovationforum.sk`), migrácia je nekomplikovaná — Astro nemá hard-coded URL, base URL je env premenná; v Netlify pridáme novú custom domain + 301 redirect z `lifo.urbanlama.eu`.

---

## 12. Brand tokens implementation

**Decision**: **CSS Custom Properties (variables) + Tailwind v4** s `@theme` direktívou

**Rationale**:
- Tailwind 4 podporuje `@theme` blok ktorý mapuje CSS variables na utility classes.
- Brand tokeny v jednom súbore (`src/styles/tokens.css`) — single source of truth (FR-019).
- Pri swap-e na finálny brand kit od grafika: zmena HEX hodnôt v tokens.css = celá stránka prefarbená bez zásahu do komponentov.

**Príklad**:
```css
/* tokens.css */
@import "tailwindcss";

@theme {
  --color-lifo-magenta: #D6307A;
  --color-lifo-teal: #36A2A8;
  --color-lifo-ink: #0A0A0A;
  --color-lifo-paper: #FFFFFF;
  --color-lifo-navy: #0C1223;

  --font-display: "Inter", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
}
```

Použitie v komponentoch: `class="bg-lifo-navy text-lifo-paper"`.

---

## 13. Testing stratégia

**Decision**:
- **Vitest** pre unit testy biz logiky (pricing.ts, promo-codes.ts, invoice.ts)
- **Playwright** pre E2E (kúpa lístka v Stripe test mode, formulárové submissions, language switch)
- **axe-core / @axe-core/playwright** pre automated a11y
- **Lighthouse CI** v build pipeline — fail < 95 score

**Rationale**:
- Biz logika ticketingu (Early Bird vs Regular cena podľa dátumu, promo kód limit počítanie) má pure-function shape — perfektné pre unit testy.
- E2E pokrýva kritické user flows. Stripe má test mode + Playwright má dobré recording/debugging.
- A11y bez auditácie sa zhoršuje rapídne — automated check chytí 80 % regresií.

**Alternatives considered**:
- **Jest**: Nahradený Vitest-om v Vite-based eco-systéme (Astro = Vite).
- **Cypress**: Playwright má lepšiu DX a multi-browser support out of box.

---

## 14. Deployment workflow

**Decision**: **Git-based deploy s Netlify** + branch previews

**Workflow**:
- `main` → produkcia (automatický deploy)
- `develop` → staging URL (review)
- Feature branches → individuálne preview URLs (review s klientom)

**Build**:
- Netlify: `npm run build` → `dist/` → serve.
- Build env vars: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `BREVO_API_KEY` — nikdy nie v gite, len v Netlify env settings.

---

## 15. Pre-flight checklist pred `/speckit-tasks`

- [x] Framework (Astro)
- [x] Hosting (Netlify)
- [x] CMS (Decap)
- [x] Payments (Stripe)
- [x] Invoicing (Stripe Invoicing)
- [x] Forms (Netlify Forms + Brevo)
- [x] Newsletter (Brevo)
- [x] i18n (Astro built-in)
- [x] Analytics (Plausible)
- [x] E-ticket PDF (@react-pdf/renderer)
- [x] Brand tokens (Tailwind v4 + CSS vars)
- [x] Testing (Vitest + Playwright + axe + Lighthouse CI)
- [x] **Doména** — `lifo.urbanlama.eu` (subdoména existujúcej `urbanlama.eu` na Webglobe DNS, smerujúca cez CNAME na Netlify)
- [ ] **Konkrétne ceny tarif** — TBD, zadávateľka rozhodne pred go-live ticketingu
- [ ] **Refund / storno podmienky text** — TBD, právny review pred go-live
- [ ] **Finálne LIFO brand kit od grafika** — paralelný proces; pracovné placeholders v `podklady/brand/` umožnia rozbeh

**Žiadne zostávajúce NEEDS CLARIFICATION blokujúce `/speckit-tasks`**. TBD položky sú obchodno-právne, nie technicko-architektonické.
