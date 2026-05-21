# Contract: Astro Content Collections

**Date**: 2026-05-12 | **Plan**: [../plan.md](../plan.md)

Tento dokument definuje **Zod schémy** pre Astro content collections. Slúži ako jediný zdroj pravdy o štruktúre obsahových súborov v `src/content/`. Decap CMS UI je generovaný **z týchto schém** (config.yml mapuje 1:1 na Zod fields).

Plné implementácie schém budú v `src/content/config.ts`. Tu len kontraktové detaily.

---

## Filesystem layout

```text
src/content/
├── config.ts                  # Zod schemas (autoritatívne)
│
├── pages/                     # Sekcie webu (per locale)
│   ├── sk/
│   │   ├── hero.md
│   │   ├── about.md
│   │   ├── for-partners.md
│   │   ├── for-municipalities.md
│   │   ├── for-investors.md
│   │   ├── for-media.md
│   │   ├── venue.md
│   │   ├── about-organizer.md
│   │   ├── investment-map.md
│   │   └── post-event.md
│   └── en/
│       └── ...
│
├── speakers/                  # 1 markdown / rečník (per locale)
│   ├── sk/
│   │   ├── janusz-michalek.md
│   │   ├── matus-vallo.md
│   │   └── ...
│   └── en/
│       └── ...
│
├── partners/                  # 1 yaml / partner
│   ├── partner-001-bigcorp.yaml
│   └── ...
│
├── partnership-tiers/         # 1 yaml / úroveň
│   ├── generalny.yaml
│   ├── hlavny.yaml
│   ├── partner-fora.yaml
│   ├── odborny-garant.yaml
│   └── medialny.yaml
│
├── program-blocks/            # 1 yaml / blok
│   ├── 01-keynote.yaml
│   ├── 02-panel-investments.yaml
│   ├── 03-workshop.yaml
│   └── ...
│
└── faq/                       # 1 markdown / FAQ položka (per locale)
    ├── sk/
    │   ├── 01-prečo-lifo.md
    │   ├── 02-ako-sa-prihlásiť.md
    │   └── ...
    └── en/
        └── ...
```

---

## Collection schemas (TypeScript / Zod)

### `pages`

```typescript
const pages = defineCollection({
  type: "content",  // markdown body je editovateľný v Decap UI
  schema: z.object({
    slug: z.string(),
    title: z.string().min(2).max(120),
    description: z.string().max(300).optional(),
    ctaLabel: z.string().max(50).optional(),
    ctaHref: z.string().optional(),
    locale: z.enum(["sk", "en"]),
    order: z.number().int().nonnegative().default(99),
    publishedAt: z.date().optional(),
  }),
});
```

**Markdown body** obsahuje samotný copy (paragraph, bullet lists, embedded images). Renderuje sa cez Astro `<Content />`.

### `speakers`

```typescript
const speakers = defineCollection({
  type: "content",
  schema: ({ image }) => z.object({
    name: z.string().min(2).max(100),
    role: z.string().min(2).max(150),
    organization: z.string().min(2).max(200),
    photo: image().refine(img => img.width >= 400, "Photo must be ≥ 400px wide"),
    socialLinks: z.object({
      linkedin: z.string().url().optional(),
      twitter: z.string().url().optional(),
      website: z.string().url().optional(),
    }).optional(),
    panelAssignment: z.string().optional(),  // FK to program-blocks slug
    order: z.number().int().nonnegative().default(99),
    status: z.enum(["confirmed", "pending"]).default("pending"),
    locale: z.enum(["sk", "en"]),
  }),
});
```

**Markdown body** = bio (max ~400 znakov, formatovaný).

### `partners`

```typescript
const partners = defineCollection({
  type: "data",
  schema: ({ image }) => z.object({
    name: z.string().min(2).max(100),
    tier: z.enum([
      "generalny",
      "hlavny",
      "partner-fora",
      "odborny-garant",
      "medialny",
      "it-partner",
    ]),
    logo: image(),
    websiteUrl: z.string().url(),
    descriptionShort: z.string().max(200).optional(),
    order: z.number().int().nonnegative().default(99),
    status: z.enum(["confirmed", "pending"]).default("pending"),
  }),
});
```

### `partnership-tiers`

```typescript
const partnershipTiers = defineCollection({
  type: "data",
  schema: z.object({
    slug: z.string(),
    name: z.string(),
    nameEn: z.string().optional(),
    shortDescription: z.string().max(300),
    shortDescriptionEn: z.string().max(300).optional(),
    benefits: z.array(z.string()),
    benefitsEn: z.array(z.string()).optional(),
    price: z.object({
      amountEur: z.number().int().positive().optional(),
      display: z.string().optional(),
    }),
    availableSlots: z.number().int().nonnegative().optional(),
    order: z.number().int().nonnegative(),
    isPublic: z.boolean().default(true),
  }),
});
```

**Pozn.**: Pre partnership tiers nepouživame per-locale rozdelenie (sú to malé objekty s len pár stringami). Inline EN polia ako `nameEn`, `benefitsEn`.

### `program-blocks`

```typescript
const programBlocks = defineCollection({
  type: "data",
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    titleEn: z.string().optional(),
    type: z.enum(["keynote", "panel", "workshop", "matchmaking", "break", "networking"]),
    startTime: z.string().regex(/^\d{2}:\d{2}$/),
    endTime: z.string().regex(/^\d{2}:\d{2}$/),
    description: z.string().max(500),
    descriptionEn: z.string().max(500).optional(),
    speakerSlugs: z.array(z.string()).default([]),
    moderatorSlug: z.string().optional(),
    order: z.number().int().nonnegative(),
  }),
});
```

### `faq`

```typescript
const faq = defineCollection({
  type: "content",
  schema: z.object({
    question: z.string().min(5).max(300),
    answer: z.string().min(5).max(2000),  // duplikované v markdown body
    category: z.enum([
      "general",
      "registration",
      "pricing",
      "venue",
      "program",
      "partnership",
      "samosprava",
    ]),
    order: z.number().int().nonnegative(),
    locale: z.enum(["sk", "en"]),
  }),
});
```

**Markdown body** = answer s formátovaním (linky, zvýraznenie).

---

## Cross-collection references (FK pattern)

Astro content collections nemajú native FK enforcement. Validáciu robíme **runtime v build kroku** alebo manuálne v komponentoch.

```typescript
// pages/program.astro
const programBlocks = await getCollection("program-blocks");
for (const block of programBlocks) {
  for (const slug of block.data.speakerSlugs) {
    const speaker = await getEntry("speakers", `${block.data.locale}/${slug}`);
    if (!speaker) {
      throw new Error(`Speaker "${slug}" referenced in program block "${block.id}" not found.`);
    }
  }
}
```

Pri zlyhaní build crashne — zaručuje že nemôžeme deploynúť stránku s broken FK.

---

## Decap CMS config (auto-generated z Zod schém)

`public/admin/config.yml`:

```yaml
backend:
  name: git-gateway
  branch: main

media_folder: public/uploads
public_folder: /uploads

i18n:
  structure: multiple_folders
  locales: [sk, en]
  default_locale: sk

collections:
  - name: speakers
    label: Rečníci
    folder: src/content/speakers
    create: true
    slug: "{{name | slugify}}"
    i18n: true
    fields:
      - { name: name, label: Meno, widget: string, i18n: duplicate }
      - { name: role, label: Pozícia, widget: string, i18n: translate }
      - { name: organization, label: Organizácia, widget: string, i18n: translate }
      - { name: photo, label: Foto, widget: image, i18n: duplicate }
      - { name: panelAssignment, label: Programový blok, widget: relation,
          collection: program-blocks, value_field: slug, display_fields: [title],
          search_fields: [title], required: false, i18n: duplicate }
      - { name: order, label: Poradie, widget: number, default: 99, i18n: duplicate }
      - { name: status, label: Stav, widget: select, options: [confirmed, pending],
          default: pending, i18n: duplicate }
      - { name: body, label: Bio, widget: markdown, i18n: translate }

  - name: partners
    label: Partneri
    folder: src/content/partners
    format: yml
    extension: yaml
    create: true
    slug: "{{name | slugify}}"
    fields:
      - { name: name, label: Názov, widget: string }
      - { name: tier, label: Úroveň, widget: select,
          options: [generalny, hlavny, partner-fora, odborny-garant, medialny, it-partner] }
      - { name: logo, label: Logo, widget: image }
      - { name: websiteUrl, label: Web, widget: string }
      - { name: order, label: Poradie, widget: number, default: 99 }
      - { name: status, label: Stav, widget: select, options: [confirmed, pending],
          default: pending }

  # ... ďalšie collections
```

---

## Validation & deployment

1. **Pre-commit hook** (lokálne dev) — `astro check` overí všetky collection content súbory voči Zod schemam. Build fails on schema violation.
2. **CI pipeline** (Netlify build) — to isté `astro check` ako gate.
3. **Decap CMS** — UI validuje typy v reálnom čase pred submitom (číslo musí byť číslo, string nesmie byť prázdny ak required).

---

## Migrácia / evolúcia

Pri zmene schémy:

1. **Backward-compatible (pridanie optional poľa)** — žiadna migrácia, existujúce súbory ostávajú validné.
2. **Breaking change (nový required field, premenovanie)** — písať migration script v `src/content/_migrations/` ktorý:
   - Načíta všetky súbory v collection
   - Pridá / premenuje pole
   - Commit batchom

Príklad pre pridanie `nameEn` na partners (ak by sa neskôr rozhodlo držať EN preklad inline):
```bash
node scripts/migrate-add-name-en.mjs
```
