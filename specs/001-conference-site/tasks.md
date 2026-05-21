---
description: "Task list for LIFO 2027 Conference Website implementation"
---

# Tasks: LIFO 2027 Conference Website

**Input**: Design documents from [/specs/001-conference-site/](./)
**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)
**Tests**: Included (Vitest + Playwright + axe + Lighthouse CI per `plan.md` Testing section).
**Organization**: Tasks grouped by user story (US1, US2, US3, US2b, US4, US5) to enable independent implementation. US1 + US2 spolu tvoria MVP (oba P1).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Maps to user story in spec.md
- Tasks include exact file paths

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Establish empty but runnable Astro project with toolchain.

- [ ] T001 Initialize Astro 5 + TypeScript project at repo root via `npm create astro@latest -- --template minimal --typescript strict --skip-houston` (creates `astro.config.mjs`, `tsconfig.json`, `package.json`, `src/pages/index.astro`)
- [ ] T002 [P] Install runtime dependencies: `npm i @astrojs/netlify @astrojs/tailwind @astrojs/react react react-dom @types/react @types/react-dom stripe @stripe/stripe-js @react-pdf/renderer @getbrevo/brevo zod qrcode`
- [ ] T003 [P] Install dev dependencies: `npm i -D vitest @vitest/coverage-v8 @playwright/test @axe-core/playwright @lhci/cli prettier eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser`
- [ ] T004 [P] Configure Tailwind v4 in `tailwind.config.ts` with brand tokens (`src/styles/tokens.css` imported via `@theme` directive)
- [ ] T005 [P] Create `.prettierrc` and `.eslintrc.cjs` with project conventions (semi: true, single-quote, 100 char line limit)
- [ ] T006 [P] Create `.env.example` listing all required vars from `quickstart.md` (no real values)
- [ ] T007 [P] Create `.gitignore` for Astro / Node / IDE / Netlify (`node_modules/`, `dist/`, `.netlify/`, `.env`, `*.log`, `.vscode/`)
- [ ] T008 Create `netlify.toml` with build command `npm run build`, publish dir `dist`, and Edge Functions config (per `plan.md` Project Structure)
- [ ] T009 [P] Create project folder skeleton: `src/{components,layouts,lib,styles,pages/api,content}`, `tests/{unit,e2e}`, `public/{fonts,uploads,admin}` per `plan.md`
- [ ] T010 [P] Copy brand assets from `podklady/brand/04_web_assets/` → `public/` (favicon.ico, all icon variants, og-image, twitter-card, manifest)
- [ ] T011 [P] Copy LIFO logo SVG variants from `podklady/brand/01_master/` + `02_variants/` → `public/logos/` (5 SVG files)
- [ ] T012 [P] Download Inter font (woff2 latin + latin-ext subsets, weights 400/600/700) from rsms.me/inter/ → `public/fonts/`
- [ ] T013 Initialize git repo, commit initial scaffold to `main` branch (`git init && git add . && git commit -m "chore: initial Astro scaffold"`)
- [ ] T014 Create GitHub repository (private) and push initial commit (`gh repo create lifo-website --private --source=. --push`)
- [ ] T015 [P] Connect GitHub repo to Netlify (Settings → Build → Git provider) — auto-deploy from `main`, configure env vars placeholders

**Checkpoint**: Empty Astro project deploys to Netlify preview URL with green favicon. No content yet.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure — i18n, brand tokens, layouts, content schemas, Decap CMS, integrations. **No user story work can start until this completes.**

- [ ] T016 Configure Astro i18n in `astro.config.mjs` with `locales: ['sk', 'en']`, `defaultLocale: 'sk'`, `routing: { prefixDefaultLocale: false }`
- [ ] T017 [P] Create `src/styles/tokens.css` with CSS custom properties for brand colors + fonts from [colors.md](../../podklady/brand/05_brand_guidelines/colors.md) and [typography.md](../../podklady/brand/05_brand_guidelines/typography.md)
- [ ] T018 [P] Create `src/styles/global.css` with Tailwind v4 imports + `@theme` block referencing tokens + base resets
- [ ] T019 [P] Create `src/styles/fonts.css` with `@font-face` declarations for self-hosted Inter (Bold + SemiBold + Regular)
- [ ] T020 Create `src/layouts/BaseLayout.astro` — html / head / meta / OG tags / hreflang / font preloads / Plausible script (only in prod) / lang attribute per locale
- [ ] T021 [P] Create `src/layouts/SectionLayout.astro` — wrapper for content pages (container, spacing, breadcrumbs)
- [ ] T022 Create `src/content/config.ts` defining Zod schemas for all collections per [contracts/content-collections.md](contracts/content-collections.md): `pages`, `speakers`, `partners`, `partnership-tiers`, `program-blocks`, `faq`
- [ ] T023 [P] Create seed content stubs in `src/content/pages/sk/` and `src/content/pages/en/` for: hero, about, for-partners, for-municipalities, for-investors, for-media, venue, about-organizer, post-event (markdown frontmatter only, placeholder body)
- [ ] T024 [P] Create `src/components/LanguageSwitcher.astro` — toggle between SK and EN with current-page-aware URL mapping
- [ ] T025 [P] Create `src/components/Header.astro` — logo + nav links + LanguageSwitcher + mobile menu
- [ ] T026 [P] Create `src/components/Footer.astro` — copyright, GDPR link, contact, organizer credit, social links
- [ ] T027 Create `src/lib/i18n.ts` — locale utils (URL routing, fallback chain, hreflang generation)
- [ ] T028 [P] Create `src/lib/stripe.ts` — Stripe client singleton with env var validation; helpers for product/price/promo lookups
- [ ] T029 [P] Create `src/lib/brevo.ts` — Brevo SDK client; helpers for `upsertContact`, `sendTransactionalEmail`
- [ ] T030 [P] Create `src/lib/env.ts` — Zod-validated env var schema, fails fast at startup if required keys missing
- [ ] T031 [P] Create `src/lib/errors.ts` — i18n-aware error code → message mapping for both locales
- [ ] T032 [P] Create `src/lib/anti-spam.ts` — honeypot validation + rate-limit (Netlify Blobs counter per IP)
- [ ] T033 [P] Create `public/admin/index.html` + `public/admin/config.yml` for Decap CMS UI per [contracts/content-collections.md](contracts/content-collections.md) Decap config section
- [ ] T034 Create `public/site.webmanifest` per [brand-guidelines.md](../../podklady/brand/05_brand_guidelines/brand-guidelines.md) §9 (name, short_name, icons, theme_color, background_color)
- [ ] T035 [P] Create `src/pages/404.astro` — branded not-found page (SK + EN via /en/404)
- [ ] T036 [P] Create `src/pages/500.astro` — branded error page
- [ ] T037 [P] Create `src/pages/privacy.astro` + `src/pages/en/privacy.astro` — GDPR Zásady ochrany OÚ (placeholder text, právny review pred go-live)
- [ ] T038 [P] Create `src/pages/terms.astro` + `src/pages/en/terms.astro` — VOP / Storno podmienky (placeholder, právny review pred go-live)
- [ ] T039 Configure Vitest in `vitest.config.ts` with TS path resolution + `tests/unit/` discovery
- [ ] T040 [P] Configure Playwright in `playwright.config.ts` with baseURL pointing to dev server, projects for chromium / firefox / webkit, axe integration
- [ ] T041 [P] Configure Lighthouse CI in `lighthouserc.cjs` — assertions for ≥95 on perf/a11y/best-practices/SEO
- [ ] T042 Add GitHub Actions workflow `.github/workflows/ci.yml` — runs lint + vitest + playwright + lighthouse on PR

**Checkpoint**: Foundation ready. Empty pages render with brand layout, both locales accessible at `/` and `/en/`. CMS UI loads at `/admin/`. No business logic yet.

---

## Phase 3: User Story 1 — Partner Inquiry Flow (Priority: P1) 🎯 MVP

**Goal**: Sponsor / partner can land on homepage, navigate to "Pre partnerov", read positioning + tiers + Martina's track record, submit inquiry form. Inquiry arrives in Netlify Forms inbox + e-mail notification to organizers.

**Independent Test**: Open homepage cold → within 30s identify LIFO date/venue/CTA → click "Pre partnerov" → see partnership tiers → submit inquiry form → receive confirmation + organizers receive notification with segment=partner.

### Tests for US1

- [ ] T043 [P] [US1] E2E test in `tests/e2e/partner-inquiry.spec.ts` — full happy path from homepage → partnership page → submit form → confirmation
- [ ] T044 [P] [US1] Unit test in `tests/unit/inquiry-validation.test.ts` — Zod schema for partner inquiry validates required fields + GDPR consent

### Content for US1

- [ ] T045 [P] [US1] Write SK content for `src/content/pages/sk/hero.md` (name + date + venue + positioning + 3 CTAs)
- [ ] T046 [P] [US1] Write EN content for `src/content/pages/en/hero.md`
- [ ] T047 [P] [US1] Write SK content for `src/content/pages/sk/for-partners.md` (value prop, ROI, benefits, CTA)
- [ ] T048 [P] [US1] Write EN content for `src/content/pages/en/for-partners.md`
- [ ] T049 [P] [US1] Write SK content for `src/content/pages/sk/about-organizer.md` (Martina Grandi track record: JLR Nitra, Volvo Valaliky, 30+ samospráv)
- [ ] T050 [P] [US1] Write EN content for `src/content/pages/en/about-organizer.md`
- [ ] T051 [P] [US1] Create 4 partnership tier yaml files in `src/content/partnership-tiers/` (generalny, hlavny, partner-fora, medialny) with placeholder ceny + benefits (právny review pred go-live)

### Implementation for US1

- [ ] T052 [US1] Implement `src/components/Hero.astro` — full-width hero with logo + dátum 11.2.2027 + Hotel Clarion Bratislava + 3 segmented CTA tlačidlá
- [ ] T053 [P] [US1] Implement `src/components/PartnershipTierCard.astro` — card with tier name, benefits list, price/CTA per [data-model.md](data-model.md) `partnership-tiers` schema
- [ ] T054 [P] [US1] Implement `src/components/TrackRecordSection.astro` — Martina's case studies (JLR 450ha, Volvo 380ha, 30+ samospráv) with subtle metrics
- [ ] T055 [P] [US1] Implement `src/components/InquiryForm.tsx` — React island with segment selector, Zod validation, segment-conditional fields, honeypot, locale-aware errors per [contracts/forms-api.md](contracts/forms-api.md)
- [ ] T056 [US1] Implement `src/pages/api/inquiry.ts` — POST handler with Zod validation, anti-spam, Brevo email send to organizers + confirmation to submitter, Brevo contact upsert with tag
- [ ] T057 [US1] Wire homepage `src/pages/index.astro` + `src/pages/en/index.astro` with Hero + 3 segment cards + Footer
- [ ] T058 [US1] Wire `src/pages/pre-partnerov.astro` + `src/pages/en/for-partners.astro` with PartnershipTierCard grid + TrackRecordSection + InquiryForm
- [ ] T059 [US1] Add SEO meta tags (Open Graph image, hreflang, canonical) via BaseLayout for US1 pages

**Checkpoint**: Partner can complete inquiry flow end-to-end. E2E test passes. Foundation US1 = MVP demo-ready.

---

## Phase 4: User Story 2 — Paid Ticket Purchase (Priority: P1) 🎯 MVP

**Goal**: Pozvaný starosta dostane mail s promo kódom → otvorí web → vyberie tarifu "Samospráva" → aplikuje kód → vyplní fakturačné údaje obce → zaplatí kartou (alebo zvolí prevod) → dostane e-ticket s QR kódom + faktúru s povinnými náležitosťami.

**Independent Test**: Get test promo code `LIFO27-SAMOSPRAVA` → unlock hidden tier → checkout via Stripe test card `4242 4242 4242 4242` → confirmation page → e-ticket PDF arrives in inbox with QR code + invoice PDF.

### Tests for US2

- [ ] T060 [P] [US2] Unit test in `tests/unit/pricing.test.ts` — Early Bird vs Regular phase resolution by date
- [ ] T061 [P] [US2] Unit test in `tests/unit/promo-codes.test.ts` — code validation, max_redemptions, expiry handling
- [ ] T062 [P] [US2] Unit test in `tests/unit/invoice.test.ts` — SK VAT fields validation (IČO regex, DIČ regex, povinné polia)
- [ ] T063 [P] [US2] E2E test in `tests/e2e/ticket-purchase.spec.ts` — promo code → checkout → Stripe test card → confirmation
- [ ] T064 [P] [US2] E2E test in `tests/e2e/bank-transfer.spec.ts` — promo code → checkout → choose bank transfer → proforma invoice received

### Stripe setup (one-time)

- [ ] T065 [US2] Create Stripe Products in dashboard (or via setup script `scripts/stripe-setup.ts`): `prod_samosprava` (gated), `prod_investor` (public), `prod_vip` (public) with metadata per [data-model.md](data-model.md)
- [ ] T066 [US2] Create Stripe Prices for each product × Early Bird / Regular phase (active Early Bird, inactive Regular initially)
- [ ] T067 [US2] Create Stripe Promotion Code `LIFO27-SAMOSPRAVA` with `applies_to: prod_samosprava`, `max_redemptions: 200`, expires 2027-01-15
- [ ] T068 [US2] Configure Stripe webhook endpoint `https://lifo.urbanlama.eu/api/webhook-stripe` listening for `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `charge.refunded`

### Implementation for US2

- [ ] T069 [P] [US2] Implement `src/lib/pricing.ts` — `getActivePrice(tier)`, `getNextPhaseStart(price)`, `isPhaseActive(price, now)` pure functions
- [ ] T070 [P] [US2] Implement `src/lib/promo-codes.ts` — `validatePromoCode(code)`, `formatPromoErrorI18n(error, locale)`
- [ ] T071 [P] [US2] Implement `src/lib/invoice.ts` — buyer info validation (IČO, DIČ, IČ DPH regex per [contracts/forms-api.md](contracts/forms-api.md))
- [ ] T072 [P] [US2] Implement `src/lib/ticket-pdf.tsx` — React PDF document with logo, attendee name, tier, date, venue, QR code (token from JWT)
- [ ] T073 [P] [US2] Implement `src/lib/jwt-eticket.ts` — sign/verify HS256 e-ticket tokens with `ETICKET_JWT_SECRET`
- [ ] T074 [P] [US2] Implement `src/components/TicketTierCard.tsx` — React island with tier name, current price + countdown to phase end, "Zaregistrovať" CTA; respects gated visibility flag
- [ ] T075 [P] [US2] Implement `src/components/CountdownEarlyBird.tsx` — live countdown ticker until phase_end
- [ ] T076 [P] [US2] Implement `src/components/PromoCodeInput.tsx` — input + apply button calling `/api/promo-validate`; on success unlocks gated tier in UI
- [ ] T077 [P] [US2] Implement `src/components/CheckoutFlow.tsx` — multi-step form: tier select → quantity → buyer info (B2B/B2C toggle) → review → redirect to Stripe Checkout
- [ ] T078 [US2] Implement `src/pages/api/promo-validate.ts` — POST handler per [contracts/forms-api.md](contracts/forms-api.md) §POST /api/promo-validate
- [ ] T079 [US2] Implement `src/pages/api/checkout.ts` — POST handler creating Stripe Checkout Session with `invoice_creation.enabled: true`, custom_fields for IČO/DIČ, per [contracts/forms-api.md](contracts/forms-api.md) §POST /api/checkout
- [ ] T080 [US2] Implement `src/pages/api/webhook-stripe.ts` — signature verify, idempotency check via Netlify Blobs, event router per [contracts/stripe-webhook.md](contracts/stripe-webhook.md)
- [ ] T081 [US2] Implement webhook handler for `checkout.session.completed` — generate PDF, send via Brevo to buyer + notif to organizers, upsert Brevo contact
- [ ] T082 [US2] Implement webhook handler for `invoice.paid` (bank transfer path) — same as above
- [ ] T083 [US2] Implement webhook handler for `invoice.payment_failed` — Brevo notif to buyer "Retry alebo prevod"
- [ ] T084 [US2] Implement webhook handler for `charge.refunded` — invalidate JWT token, Brevo notif
- [ ] T085 [P] [US2] Wire `src/pages/tickets.astro` + `src/pages/en/tickets.astro` with TicketTierCard grid + PromoCodeInput + CheckoutFlow
- [ ] T086 [P] [US2] Wire `src/pages/tickets/confirmation.astro` — fetches Stripe session by `session_id` query param, displays success + ticket summary

**Checkpoint**: Test purchase end-to-end succeeds. E-ticket PDF doručený, invoice doručená. Stripe webhook idempotent (replay-safe). MVP = US1 + US2 ready.

---

## Phase 5: User Story 3 — Investor / Business Inquiry & Purchase (Priority: P2)

**Goal**: Investor / developer / banka pozrie "Pre investorov", vidí line-up speakerov + matchmaking formát → buď submituje inquiry (high-touch sales lead) ALEBO kúpi VIP / Investor tarifu priamo.

**Independent Test**: Land on "Pre investorov" → see investor value prop + program teaser → either submit inquiry form OR proceed to ticket purchase with Investor / VIP tier (no promo code needed).

### Tests for US3

- [ ] T087 [P] [US3] E2E test in `tests/e2e/investor-purchase.spec.ts` — buy Investor tier without promo code (public visibility)

### Content for US3

- [ ] T088 [P] [US3] Write SK content for `src/content/pages/sk/for-investors.md`
- [ ] T089 [P] [US3] Write EN content for `src/content/pages/en/for-investors.md`

### Implementation for US3

- [ ] T090 [US3] Wire `src/pages/pre-investorov.astro` + `src/pages/en/for-investors.astro` — Hero variant + Matchmaking formát section + speakers teaser + InquiryForm (segment=investor) + link to /tickets

**Checkpoint**: Investor flow works. Reuses US1 (inquiry form) and US2 (ticket purchase) komponenty.

---

## Phase 6: User Story 4 — Press / Media Kit (Priority: P3)

**Goal**: Novinár / médiá navštívia "Pre médiá" sekciu, stiahnu press kit (logo + fakty + biography Martiny + fotografie), kontaktujú PR osobu.

**Independent Test**: Open `/pre-media` → click "Stiahnuť press kit" → ZIP / PDF download succeeds with all branded assets.

### Tests for US4

- [ ] T091 [P] [US4] E2E test in `tests/e2e/press-kit.spec.ts` — navigate to media page → trigger download → verify file received

### Content for US4

- [ ] T092 [P] [US4] Write SK content for `src/content/pages/sk/for-media.md`
- [ ] T093 [P] [US4] Write EN content for `src/content/pages/en/for-media.md`
- [ ] T094 [P] [US4] Assemble `public/press-kit/lifo-2027-press-kit.zip` containing: logo variants from `podklady/brand/`, Martina biography PDF (text TBD), key facts PDF, 3 hero photos (TBD)

### Implementation for US4

- [ ] T095 [US4] Wire `src/pages/pre-media.astro` + `src/pages/en/for-media.astro` with download button + PR contact (e-mail link)

---

## Phase 7: User Story 2b — Out-of-list Záujemca (Priority: P3)

**Goal**: Záujemca mimo target listu (neoslovený mailom) vyplní "Mám záujem o pozvánku" formulár → manuálny review tímom → individuálny one-time promo kód odoslaný mailom.

**Independent Test**: Open "Pre samosprávy" → click "Nedostal som pozvánku" → submit form s názvom obce + motiváciou → confirmation message "Posúdime do 5 dní".

### Tests for US2b

- [ ] T096 [P] [US2b] E2E test in `tests/e2e/out-of-list-inquiry.spec.ts` — submit out-of-list interest → confirmation + organizers receive tagged notification

### Implementation for US2b

- [ ] T097 [P] [US2b] Write SK content for `src/content/pages/sk/for-municipalities.md` (samospráva value prop + invite-driven model + out-of-list path)
- [ ] T098 [P] [US2b] Write EN content for `src/content/pages/en/for-municipalities.md`
- [ ] T099 [US2b] Wire `src/pages/pre-samospravy.astro` + `src/pages/en/for-municipalities.astro` — value prop + workshop preview + InquiryForm (segment=samosprava-out-of-list)
- [ ] T100 [US2b] Update `/api/inquiry` handler to tag samospráva-out-of-list submissions with explicit `inquiry.subSegment` for organizer triage

---

## Phase 8: User Story 5 — Praktické Info (Priority: P3)

**Goal**: Potvrdený účastník 1-2 dni pred eventom kontroluje adresu hotela, MHD, parkovanie, aktuálny program, kontakty.

**Independent Test**: Open `/miesto-konania` → see adresa + Google Maps embed + MHD spojenie + parkovanie. Open `/program` → see updated agenda with timestamps + speakers.

### Tests for US5

- [ ] T101 [P] [US5] E2E test in `tests/e2e/practical-info.spec.ts` — navigate to venue, program, FAQ; verify content loads and mapa embed works

### Content for US5

- [ ] T102 [P] [US5] Write SK content for `src/content/pages/sk/venue.md` — Hotel Clarion Bratislava, adresa, MHD, parkovanie, bezbariérovosť
- [ ] T103 [P] [US5] Write EN content for `src/content/pages/en/venue.md`
- [ ] T104 [P] [US5] Create initial FAQ items in `src/content/faq/sk/` (6 položiek pokrývajúcich Objection Handler kategorie: čas, hodnota, "ďalšia konferencia?", veľkosť obce, peniaze, politická neutralita) + EN translations
- [ ] T105 [P] [US5] Create initial program blocks in `src/content/program-blocks/` (placeholder agenda — keynote, panel investments, workshop, matchmaking, networking)

### Implementation for US5

- [ ] T106 [P] [US5] Implement `src/components/Venue.astro` — adresa + Google Maps iframe + MHD + parkovanie info
- [ ] T107 [P] [US5] Implement `src/components/ProgramTimeline.astro` — chronological agenda renderer reading from program-blocks collection + speaker FK resolution
- [ ] T108 [P] [US5] Implement `src/components/FAQ.astro` — accordion (native `<details>` element) reading from faq collection grouped by category
- [ ] T109 [P] [US5] Implement `src/components/SpeakerCard.astro` — photo + name + role + organization + bio + social links (only status=confirmed)
- [ ] T110 [US5] Wire `src/pages/miesto-konania.astro` + `src/pages/en/venue.astro` with Venue + practical info
- [ ] T111 [US5] Wire `src/pages/program.astro` + `src/pages/en/program.astro` with ProgramTimeline + SpeakerCard grid
- [ ] T112 [US5] Wire `src/pages/faq.astro` + `src/pages/en/faq.astro` with FAQ component
- [ ] T113 [US5] Add "Posledná aktualizácia: DATE" badge na Program a Venue pages (auto-generated z git commit date alebo content frontmatter `lastUpdated`)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Production-readiness, performance, accessibility, SEO, deployment.

### Newsletter (cross-cutting)

- [ ] T114 [P] Implement `src/components/NewsletterForm.tsx` — email + segment checkboxes + GDPR consent
- [ ] T115 [P] Implement `src/pages/api/newsletter.ts` — POST handler with Brevo double opt-in per [contracts/forms-api.md](contracts/forms-api.md) §POST /api/newsletter
- [ ] T116 [P] Embed NewsletterForm in Footer across all pages

### Analytics + GDPR

- [ ] T117 [P] Integrate Plausible tracking in BaseLayout (script tag, only in production env)
- [ ] T118 [P] Add custom event tracking: ticket purchase initiated, ticket purchased, inquiry submitted, newsletter subscribed
- [ ] T119 [P] Verify NO third-party cookies set (cookie-less Plausible eliminates need for cookie banner); document in privacy.astro

### SEO

- [ ] T120 [P] Generate `public/sitemap.xml` (Astro integration `@astrojs/sitemap`) with hreflang annotations
- [ ] T121 [P] Generate `public/robots.txt` allowing all + sitemap link
- [ ] T122 [P] Verify OG image / Twitter card meta tags resolve correctly via OpenGraph.xyz validator

### Accessibility

- [ ] T123 [P] Run axe audit on all pages: `npm run a11y` — fix all critical / serious violations
- [ ] T124 [P] Keyboard navigation manual test: tab order, focus visible, skip-to-content link
- [ ] T125 [P] Screen reader test (NVDA Windows / VoiceOver Mac) — landmarks, ARIA labels, form errors announced

### Performance

- [ ] T126 [P] Run Lighthouse CI on staging — fail < 95 on perf / a11y / SEO / best-practices
- [ ] T127 [P] Verify LCP < 2s on 4G, < 3s on simulated 3G (Chrome DevTools throttling)
- [ ] T128 [P] Tree-shake unused dependencies, analyze bundle via `npm run build && open dist/_astro/`

### Deployment + DNS

- [ ] T129 In Netlify Settings → Domain management → Add custom domain `lifo.urbanlama.eu`
- [ ] T130 Add CNAME record `lifo` → `<netlify-target>.netlify.app` in Webglobe DNS panel (zone `urbanlama.eu`)
- [ ] T131 Add TXT verification record (Netlify provides exact value) in Webglobe DNS
- [ ] T132 Add SPF + DKIM TXT records for Brevo sender domain in Webglobe DNS
- [ ] T133 Verify HTTPS active (Let's Encrypt cert issued by Netlify within ~ 5 min after DNS propagation)
- [ ] T134 Set production env vars in Netlify dashboard (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, BREVO_API_KEY, ETICKET_JWT_SECRET, PLAUSIBLE_DOMAIN, SITE_BASE_URL)
- [ ] T135 Switch Stripe to **live mode** (Products + Prices + Promo Codes re-created in live mode; webhook re-pointed to live URL)
- [ ] T136 Test live transaction with real card (1 € test product, then refund) — verify full flow works in prod

### Documentation

- [ ] T137 [P] Update root `README.md` with project overview, links to spec/plan/tasks, quickstart link
- [ ] T138 [P] Document operator runbook in `docs/operator-runbook.md`: how to add speaker, partner, ticket tier, promo code; rollback strategy; incident response

### Pre-launch smoke test

- [ ] T139 Manual smoke test checklist execution: SK home → EN home → all segment pages → ticket purchase test (test mode) → inquiry submit → newsletter signup → press kit download → mobile responsive → all from cold cache
- [ ] T140 Sign-off review with stakeholder (Martina) → go/no-go for public launch

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: no dependencies, starts immediately. Many tasks parallelize after T001.
- **Foundational (Phase 2)**: depends on Phase 1 complete. **Blocks all user story work.**
- **User Story phases (3–8)**: depend on Phase 2 complete. Stories can be developed in parallel (different files); content writing is mostly parallel.
- **Polish (Phase 9)**: starts when at least US1 + US2 (MVP) are functional; deployment tasks (T129–T136) run sequentially at the end.

### User story dependencies

- **US1** (Partner inquiry): no deps on other stories. Independently testable.
- **US2** (Paid ticket): no deps on US1 logic but shares Header / Footer / Layout from Foundational.
- **US3** (Investor): reuses US1 InquiryForm + US2 ticket flow → can start after both reach 80% (or run parallel as long as components stabilize).
- **US2b** (Out-of-list): depends on US1 InquiryForm component + US2 understanding of promo code workflow. Light task.
- **US4** (Media): independent; only needs Header/Footer.
- **US5** (Practical info): independent; only needs Header/Footer + content collections.

### MVP definition

- **MVP = Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) + portion of Phase 9 (deployment + smoke test)**.
- US3, US2b, US4, US5 môžu pribudnúť v ďalších iteráciách (T+N týždňov).
- Brand kit final swap (od grafika): paralelný — kedykoľvek pred go-live, edits len v `src/styles/tokens.css` + assety v `public/`.

### Parallel opportunities

- **Phase 1**: T002–T012 môžu bežať paralelne (15 + parallel tasks)
- **Phase 2**: T017–T042 mostly parallel (foundational components + libs)
- **Within US1**: content writing (T045–T051) and component development (T053–T055) plne paralelné
- **Within US2**: lib tasks (T069–T073) paralelné, komponenty (T074–T077) paralelné, content (T088–T089) paralelné
- **Across stories**: After Phase 2 complete, multiple developers môžu paralelne na US1 / US2 / US3-5

---

## Parallel example: foundational phase

```bash
# After T016 (i18n config) commits, launch in parallel:
T017: tokens.css       # styling/
T018: global.css        # styling/
T019: fonts.css         # styling/
T020: BaseLayout.astro  # layouts/
T021: SectionLayout.astro
T022: content config.ts
T028: stripe.ts         # lib/
T029: brevo.ts          # lib/
T030: env.ts            # lib/
T031: errors.ts         # lib/
T032: anti-spam.ts      # lib/
T033: Decap config      # public/admin/
```

---

## Implementation strategy

### MVP first (Phase 1 → 2 → 3 → 4 → partial 9)

1. Phase 1 setup (cca 1–2 dni)
2. Phase 2 foundational (cca 3–5 dní)
3. Phase 3 US1 partner inquiry (cca 2–3 dni)
4. Phase 4 US2 paid ticketing (cca 5–7 dní — najkomplikovanejšia)
5. Phase 9 deployment + smoke test (cca 1–2 dni)
6. **STOP. Demo MVP zadávateľke.**

**MVP timeline odhad**: ~12–19 dní development pre 1 senior full-stack vývojára.

### Incremental delivery (rozšírenia po MVP)

7. Phase 5 US3 investor (cca 1 deň)
8. Phase 7 US2b out-of-list (cca 0.5 dňa)
9. Phase 8 US5 praktické info + program + FAQ (cca 2–3 dni)
10. Phase 6 US4 média kit (cca 0.5 dňa)
11. Phase 9 polish iterations (continuously)

### Parallel team strategy (ak je tím viacero vývojárov)

S 2 vývojármi po MVP:
- Dev A: Phase 5 (US3) + Phase 6 (US4)
- Dev B: Phase 7 (US2b) + Phase 8 (US5)
- Obidvaja: Phase 9 polish

---

## Notes

- [P] tasks = different files, no blocking dependencies — bezpečne paralelné
- [Story] label umožňuje filtrovať tasks per user story v Linear / Jira / GitHub Projects
- Každá user story je independently testable → MVP demo môže prebehnúť po Phase 3 + 4
- Brand kit final od grafika = swap CSS variables; **nezadrží** žiadnu inú task
- TBD obchodno-právne (ceny, refund policy, doménové texty) = obsahové edits, nie code changes — riešia sa paralelne s development-om
- Commit per task alebo logical group → granular history
- Pre každý task dôsledne dodržiavať file paths z [plan.md](plan.md) Project Structure
