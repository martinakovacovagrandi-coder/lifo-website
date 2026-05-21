# Specification Quality Checklist: LIFO 2027 Conference Website

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-05-12
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — implementation choices (Next.js / Astro / static HTML, CMS) sú deferované do `/speckit-plan`. Špec hovorí o platformových výsledkoch (CDN-fronted hosting), nie o konkrétnych frameworkoch.
- [x] Focused on user value and business needs — tri user stories priamo mapujú obchodné cieľovky (partner, samospráva, investor).
- [x] Written for non-technical stakeholders — zápis v slovenčine, business jazyk, technické termíny vysvetlené.
- [x] All mandatory sections completed — User Scenarios, Requirements, Success Criteria, Assumptions.

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — **0 markerov**. FR-028 (jazyky) vyriešená: SK + EN minimum + roadmapa DE/PL/IT/ES. FR-029 (acquisition model) vyriešená: paid model pre všetkých účastníkov, kurátorský acquisition mimo webu (mail + telefón), tarifa "Samospráva" gated cez promo kód (Option D — hybrid).
- [x] Requirements are testable and unambiguous — FR sú formulované ako MUST, každý overiteľný.
- [x] Success criteria are measurable — SC-001 až SC-010 obsahujú konkrétne metriky (čas, percentá, počty).
- [x] Success criteria are technology-agnostic — formulované cez user / business outcomes, nie cez konkrétne nástroje.
- [x] All acceptance scenarios are defined — každá user story má Given/When/Then.
- [x] Edge cases are identified — sekcia Edge Cases pokrýva pre-launch stav, slabé pripojenie, accessibility, sponzor odstúpi, zmena dátumu, anti-spam, post-event.
- [x] Scope is clearly bounded — Assumptions explicitne vylučujú live event features, online platby, plnohodnotnú CRM integráciu, viral traffic.
- [x] Dependencies and assumptions identified — Assumptions sekcia obsahuje 11 explicitných predpokladov.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria — pokrytie cez User Stories a Edge Cases.
- [x] User scenarios cover primary flows — 5 user stories pokrývajú primárne (P1) aj sekundárne (P2/P3) cieľovky.
- [x] Feature meets measurable outcomes defined in Success Criteria — SC-001 až SC-010 reflektujú business intent.
- [x] No implementation details leak into specification — kontrolované, jediná zmienka technologického charakteru (HTTPS, GA4 / Plausible v Assumptions) je v rámci povolených platformových štandardov.

## Notes

- Špec je **kompletne validovaná** (14/14 položiek pass). Pripravená na `/speckit-plan`.
- Otvorené **plán-level** otázky (nie spec-level, riešia sa v implementačnom pláne):
  - Výber konkrétnej platobnej brány (Stripe / GP webpay / TrustPay / Besteron) — kritériá: B2B fakturácia na SK, multi-currency pre zahraničné platby.
  - Výber CMS / obsahového modelu pre i18n (headless: Sanity / Contentful / Strapi / Decap, alebo statické markdown súbory s build-time generovaním).
  - Výber frameworku / hostingu (Astro + Netlify vs. Next.js + Vercel vs. iné).
  - Konkrétne názvy a ceny tarif (Samospráva / Investor / Business / VIP).
  - Konkrétny dátum cutoffu Early Bird a Regular fázy.
  - Refund / storno podmienky (text dokumentu).

## Validation iterations

1. **2026-05-12 (initial)**: 13/14 položiek prešlo. 2 markery zámerne ponechané pre obchodné rozhodnutia.
2. **2026-05-12 (po Q1)**: FR-028 vyriešená — SK + EN minimum, roadmapa DE/PL/IT/ES (FR-028a až FR-028e). Zostáva 1 marker (FR-029).
3. **2026-05-12 (po Q2 + paid model)**: FR-029 vyriešená — paid model pre všetkých, acquisition cez mail + telefón, web ako platobný kanál; tarifa "Samospráva" gated cez promo kód (Option D hybrid). Doplnené FR-030 až FR-041 (ticketing + pricing + faktúry + promo kódy). Pridaná sekcia Reference (lidskykapital.cz / retailindetail.cz). Doplnené entity Ticket Tier, Pricing Phase, Promo Code, Order, Attendee, Invoice. Doplnené SC-011 až SC-015 (konverzia, drop-off, čas nákupu, platobné incidenty, daňová zhoda faktúr). 14/14 položiek pass.
4. **2026-05-12 (LIFO-only scope, Project Nation deferred)**: Spec scope-uje **iba LIFO** — Project Nation prepojenie out of scope pri launchi (FR-003 prepísaná, FR-029b cleanup). Brand požiadavky odpojené od Project Nation brand briefu — FR-018/019/020 prepísané pre LIFO vlastný brand kit, s pracovnými default-mi a CSS token izoláciou. Vyradenie "Interlock" / "Pillar Pivot" / PN palety z požiadaviek (FR-020 explicitne). Aktualizovaná Reference sekcia, Assumptions (brand, plán rastu). 14/14 prešlo, ale **2 nové plán-level otázky** otvorené (Investment Map, LIFO brand kit) — viď Notes nižšie.
