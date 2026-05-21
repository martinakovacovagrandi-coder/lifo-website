# Data Model: LIFO 2027 Conference Website

**Phase 1** | **Date**: 2026-05-12 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Princíp

LIFO web nemá vlastnú databázu v v1. Entity sú **distribuované** medzi:

1. **Astro content collections** (markdown / yaml v repo) — obsah ktorý sa zriedka mení a podlieha review (rečníci, partneri, FAQ, tarify, sekcie webu)
2. **Stripe** — všetko platobné (Customer, Product, Price, Promotion Code, Checkout Session, Invoice, Subscription ak vznikne)
3. **Brevo** — newsletter subscribers a transakčné maily
4. **Netlify Forms** — submissions formulárov (Inquiry)
5. **Vygenerované runtime** — Visitor, e-ticket QR token (in-memory, neukladáme)

## Mapovanie spec entít → storage

| Entity (zo spec.md)         | Storage                        | Editovateľnosť                              |
| --------------------------- | ------------------------------ | ------------------------------------------- |
| Visitor                     | Žiadne — anonymný session     | N/A                                          |
| Inquiry                     | Netlify Forms                 | Inbox UI v Netlify dashboarde                |
| Speaker                     | Astro collection `speakers/`  | Decap CMS `/admin/`                          |
| Program Block               | Astro collection `program-blocks/` | Decap CMS `/admin/`                     |
| Partner                     | Astro collection `partners/`  | Decap CMS `/admin/`                          |
| Partnership Tier            | Astro collection `partnership-tiers/` | Decap CMS `/admin/`                  |
| Page Content Block          | Astro collection `pages/{locale}/` | Decap CMS `/admin/` per-locale          |
| Newsletter Subscriber       | Brevo                          | Brevo UI                                     |
| Ticket Tier                 | Stripe Product + Price          | Stripe Dashboard                             |
| Pricing Phase               | Stripe Price (jeden Price = jedna fáza) | Stripe Dashboard                  |
| Promo Code                  | Stripe Promotion Code           | Stripe Dashboard                             |
| Order                       | Stripe Checkout Session        | Stripe Dashboard                             |
| Attendee                    | Stripe Checkout custom fields + Brevo contact | Stripe + Brevo            |
| Invoice                     | Stripe Invoice                  | Stripe Dashboard                             |

Toto rozdelenie minimalizuje **vlastnú DB infrastruktúru** v v1 a využíva osvedčené SaaS služby.

---

## Schemas — Astro content collections

Definované v `src/content/config.ts` cez Zod. Toto sú **autoritatívne schémy** pre obsah v repo.

### `speakers` collection

```typescript
import { defineCollection, z } from "astro:content";

const speakers = defineCollection({
  type: "content",
  schema: ({ image }) => z.object({
    name: z.string().min(2),
    role: z.string().min(2),
    organization: z.string().min(2),
    bio: z.string().max(400),  // SK and EN versions via i18n collection split
    photo: image().refine(img => img.width >= 400, "Photo must be ≥ 400px wide"),
    socialLinks: z.object({
      linkedin: z.string().url().optional(),
      twitter: z.string().url().optional(),
      website: z.string().url().optional(),
    }).optional(),
    panelAssignment: z.string().optional(),  // FK to program-block slug
    order: z.number().int().nonnegative().default(99),
    status: z.enum(["confirmed", "pending"]).default("pending"),
    locale: z.enum(["sk", "en"]).default("sk"),
  }),
});
```

**Pravidlá**:
- Iba `status: confirmed` rečníci sa zobrazia na webe (FR-007).
- `order` umožňuje manual reorder bez prejmenovávania súborov.
- `photo` má min. width požiadavku — chráni pred low-res fotkami.

### `program-blocks` collection

```typescript
const programBlocks = defineCollection({
  type: "data",
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    type: z.enum(["keynote", "panel", "workshop", "matchmaking", "break"]),
    startTime: z.string().regex(/^\d{2}:\d{2}$/),  // "09:30"
    endTime: z.string().regex(/^\d{2}:\d{2}$/),
    description: z.string().max(500),
    speakerIds: z.array(z.string()).default([]),  // FK to speakers
    order: z.number().int().nonnegative(),
  }),
});
```

### `partners` collection

```typescript
const partners = defineCollection({
  type: "data",
  schema: ({ image }) => z.object({
    name: z.string(),
    tier: z.enum(["generalny", "hlavny", "partner-fora", "medialny", "odborny-garant"]),
    logo: image(),
    websiteUrl: z.string().url(),
    order: z.number().int().nonnegative().default(99),
    status: z.enum(["confirmed", "pending"]).default("pending"),
  }),
});
```

**Pravidlá**:
- Iba `status: confirmed` sa zobrazí.
- Tier je enumerated → konzistentné grouping na webe.

### `partnership-tiers` collection

```typescript
const partnershipTiers = defineCollection({
  type: "data",
  schema: z.object({
    slug: z.string(),                // "generalny", "hlavny", ...
    name: z.string(),                // "Generálny partner"
    shortDescription: z.string(),
    benefits: z.array(z.string()),   // bullet list
    price: z.object({
      amount: z.number().int().positive().optional(),  // €
      currency: z.string().default("EUR"),
      display: z.string().optional(),  // "20 000 €" alebo "Na vyžiadanie"
    }),
    availableSlots: z.number().int().nonnegative().optional(),
    order: z.number().int().nonnegative(),
    isPublic: z.boolean().default(true),  // false = "na vyžiadanie"
  }),
});
```

### `faq` collection

```typescript
const faq = defineCollection({
  type: "content",
  schema: z.object({
    question: z.string(),
    answer: z.string(),
    category: z.enum(["general", "registration", "venue", "program", "partnership"]),
    order: z.number().int().nonnegative(),
    locale: z.enum(["sk", "en"]),
  }),
});
```

### `pages` collection (sekcie webu — hero, about, atď.)

```typescript
const pages = defineCollection({
  type: "content",
  schema: z.object({
    slug: z.string(),               // "hero", "about", "for-partners", ...
    title: z.string(),
    description: z.string().optional(),
    ctaLabel: z.string().optional(),
    ctaHref: z.string().optional(),
    locale: z.enum(["sk", "en"]),
  }),
});
```

---

## Schemas — Stripe entities

Tieto entity žijú v Stripe Dashboarde. **Nedefinujeme ich v kóde** — kód iba s nimi komunikuje cez Stripe SDK.

### Stripe Product (zodpovedá Ticket Tier zo spec.md)

```yaml
# Vytvorené raz v Stripe Dashboarde (manuálne alebo cez setup script)
Products:
  - id: prod_samosprava
    name: "LIFO 2027 — Vstupenka pre samosprávy"
    description: "Pre primátorov, starostov a manažment priemyselných parkov"
    metadata:
      tier_slug: "samosprava"
      gated: "true"
      visible_public: "false"
  - id: prod_investor
    name: "LIFO 2027 — Vstupenka pre investorov / business"
    ...
    metadata:
      tier_slug: "investor"
      gated: "false"
      visible_public: "true"
  - id: prod_vip
    name: "LIFO 2027 — VIP vstupenka"
    ...
```

### Stripe Price (zodpovedá Pricing Phase zo spec.md)

Každá kombinácia tarifa × fáza = jedna Price v Stripe.

```yaml
Prices:
  - id: price_samosprava_earlybird
    product: prod_samosprava
    unit_amount: 19000  # cents = 190 €
    currency: eur
    active: true
    metadata:
      phase: "earlybird"
      phase_end: "2026-10-31T23:59:59Z"
  - id: price_samosprava_regular
    product: prod_samosprava
    unit_amount: 29000  # 290 €
    active: false  # aktivuje sa po skončení earlybird
    metadata:
      phase: "regular"
      phase_start: "2026-11-01T00:00:00Z"
  - id: price_investor_earlybird
    ...
```

**Príklad runtime resolution** (server-side):
1. Klient navštívi `/tickets/`.
2. Server fetchuje `Stripe.prices.list({ active: true })` → vráti len aktívne Prices.
3. Pre každý Product vyberie najlacnejšiu aktívnu Price (= aktuálna fáza).
4. Renderuje TierCard s touto cenou + countdown do `phase_end`.

Cron / scheduled function prepne `active: false → true` medzi fázami (alebo manuálne).

### Stripe Promotion Code (zodpovedá Promo Code zo spec.md)

```yaml
PromotionCodes:
  - code: "LIFO27-SAMOSPRAVA"
    coupon_id: coupon_samosprava_unlock
    metadata:
      tier_slug: "samosprava"
    expires_at: 2027-01-15T23:59:59Z
    max_redemptions: 200
    restrictions:
      first_time_transaction: false
      minimum_amount: null
      currency_options:
        eur: {}

  - code: "LIFO27-IND-{random}"   # Individual one-time codes
    max_redemptions: 1
    expires_at: <7 days from issuance>
```

Coupon `coupon_samosprava_unlock` má `percent_off: 0` (nezľava) ale priradený k `applies_to.products: [prod_samosprava]` — tj. iba "odomyká" inak skrytú tarifu. Pre skutočnú zľavu vytvoriť coupon s `percent_off` alebo `amount_off`.

### Stripe Checkout Session (zodpovedá Order zo spec.md)

```yaml
CheckoutSession:
  mode: payment
  payment_method_types: [card]
  line_items:
    - price: price_samosprava_earlybird
      quantity: 1
  customer_email: <buyer email>
  metadata:
    organization: <IČO + name>
    locale: <sk|en>
    referral: <UTM / from invite link>
  invoice_creation:
    enabled: true
    invoice_data:
      custom_fields:
        - name: "IČO"
          value: <buyer IČO>
        - name: "DIČ"
          value: <buyer DIČ>
        - name: "IČ DPH"
          value: <buyer IČ DPH or "—">
      description: "Vstupenka na LIFO 2027 — Local Innovation Forum, 11. 2. 2027, Hotel Clarion Bratislava"
      footer: "Splatné na účet uvedený na faktúre."
  ui_mode: hosted
  success_url: "https://lifo.urbanlama.eu/tickets/confirmation?session_id={CHECKOUT_SESSION_ID}"
  cancel_url: "https://lifo.urbanlama.eu/tickets/"
```

### Stripe Invoice (zodpovedá Invoice zo spec.md)

Generovaný automaticky Stripe pri `invoice_creation.enabled: true`. Pole `custom_fields` umožňuje pridať IČO / DIČ / IČ DPH (povinné pre SK B2B fakturáciu).

---

## Schemas — Brevo entities

### Contact (zodpovedá Attendee + Newsletter Subscriber zo spec.md)

```yaml
Contact:
  email: <email>
  attributes:
    FIRSTNAME: <meno>
    LASTNAME: <priezvisko>
    ORGANIZATION: <názov organizácie>
    SEGMENT: "partner" | "samosprava" | "investor" | "media"
    LANGUAGE: "sk" | "en"
    SOURCE: "newsletter" | "ticket-purchase" | "inquiry-form"
    TICKET_TIER: "samosprava" | "investor" | "vip" | null
    GDPR_CONSENT: <ISO timestamp>
  lists:
    - 1  # All subscribers
    - <segment-specific list id>
```

Brevo lists umožňujú segmentovanú komunikáciu (napr. iba samosprávam pošleme upozornenie o blízkom workshope).

---

## Schemas — Netlify Forms

Forms sú definované **v HTML-i** (Astro `<form>` element s `name` a `data-netlify="true"`). Polia sa automaticky parsujú a uložia.

### `inquiry` form

```html
<form name="inquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="inquiry" />
  <p class="hidden"><label>Don't fill this: <input name="bot-field" /></label></p>

  <fieldset>
    <legend>Segment</legend>
    <label><input type="radio" name="segment" value="partner" required /> Partner / Sponzor</label>
    <label><input type="radio" name="segment" value="samosprava" /> Samospráva</label>
    <label><input type="radio" name="segment" value="investor" /> Investor / Business</label>
    <label><input type="radio" name="segment" value="media" /> Médiá</label>
    <label><input type="radio" name="segment" value="other" /> Iné</label>
  </fieldset>

  <label>Meno*: <input name="name" type="text" required minlength="2" /></label>
  <label>E-mail*: <input name="email" type="email" required /></label>
  <label>Telefón: <input name="phone" type="tel" /></label>
  <label>Organizácia*: <input name="organization" type="text" required /></label>
  <label>Správa*: <textarea name="message" required minlength="10" maxlength="2000"></textarea></label>

  <!-- Segment-špecifické polia (zobrazia sa JS-om podľa zvoleného segmentu) -->
  <label data-segment="samosprava">Názov obce: <input name="municipality" /></label>
  <label data-segment="samosprava">Počet obyvateľov: <input name="population" type="number" /></label>
  <label data-segment="samosprava">Hlavná výzva: <textarea name="challenge"></textarea></label>

  <label>
    <input type="checkbox" name="gdpr" required />
    Súhlasím so spracovaním osobných údajov podľa <a href="/privacy">Zásad ochrany OÚ</a>.
  </label>

  <button type="submit">Odoslať dopyt</button>
</form>
```

Submission → Netlify zachytí → e-mail notif organizátorom + uloží v Netlify inbox + (optional) Zapier / Make webhook → Brevo contact import.

### `newsletter` form

```html
<form name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="newsletter" />
  <p class="hidden"><label>Don't fill this: <input name="bot-field" /></label></p>

  <label>E-mail*: <input name="email" type="email" required /></label>
  <fieldset>
    <legend>Som...</legend>
    <label><input type="checkbox" name="segments[]" value="partner" /> Partner / Sponzor</label>
    <label><input type="checkbox" name="segments[]" value="samosprava" /> Samospráva</label>
    <label><input type="checkbox" name="segments[]" value="investor" /> Investor</label>
    <label><input type="checkbox" name="segments[]" value="media" /> Médiá</label>
  </fieldset>
  <label>
    <input type="checkbox" name="gdpr" required />
    Súhlasím s odberom noviniek o LIFO.
  </label>
  <button type="submit">Prihlásiť sa</button>
</form>
```

Po submit Astro endpoint pošle do Brevo API (double opt-in).

---

## Vzťahy (data relationships)

```text
Speaker ────< panelAssignment >──── ProgramBlock
Partner ────< tier >──── PartnershipTier (enum-like)

Ticket Tier (Stripe Product) ────< has many >──── Pricing Phase (Stripe Price)
Promotion Code ────< applies_to >──── Ticket Tier (Stripe Product)

Order (Stripe Checkout Session) ────< contains >──── Pricing Phase (line items)
Order ────< generates >──── Invoice (Stripe Invoice)
Order ────< creates / updates >──── Attendee (Stripe customer fields + Brevo contact)

Inquiry (Netlify Form submission) ────< maybe creates >──── Newsletter Subscriber (manual / Zapier)
```

## State transitions

### Order lifecycle (Stripe)

```text
Created (Checkout Session)
   ↓
 pending payment ──[ user pays card ]──> paid ──> e-ticket generated → Brevo email → DONE
   │
   ├─[ user closes / abandons ]──> expired (30 min default)
   │
   └─[ bank transfer chosen ]──> pending (awaiting manual reconciliation)
                                   ↓
                                 paid (after manual mark) → e-ticket sent
                                   ↓
                                 unpaid > 14 days → cancelled + slot released
```

### Promo Code lifecycle

```text
created (active) ──> redeemed N times
   │
   ├─[ max_redemptions reached ]──> exhausted
   ├─[ expires_at passed ]──> expired
   └─[ manually deactivated by admin ]──> archived
```

### Speaker / Partner lifecycle (content collections)

```text
draft (status: pending) ──[ confirmation received from speaker/partner ]──> confirmed
                                                                              ↓
                                                                            visible on website
   │
   └─[ withdrew ]──> archived (file moved to /archive/, not deleted)
```

## Validačné pravidlá

| Entity                | Validation                                                                  |
| --------------------- | --------------------------------------------------------------------------- |
| Speaker.bio           | max 60 slov / ≤ 400 znakov                                                  |
| Speaker.photo         | min šírka 400 px, max veľkosť 1 MB, formáty JPG / PNG / WebP               |
| Speaker.status        | iba `confirmed` sa renderuje na webe                                       |
| Partner.logo          | SVG preferred (vektor); min šírka 240 px ak raster                          |
| PartnershipTier.price | `amount` int €; ak `null`, zobrazí sa `display` string ("Na vyžiadanie")  |
| Inquiry.email         | validná RFC 5322                                                            |
| Inquiry.gdpr          | povinný consent checkbox                                                    |
| Newsletter.email      | double opt-in cez Brevo (potvrdzovací e-mail s linkom)                     |
| Order.organization    | povinné pre B2B nákup; IČO validný formát (8 číslic), DIČ validný (10)    |
| PromoCode             | case-insensitive porovnanie, max 32 znakov                                  |
