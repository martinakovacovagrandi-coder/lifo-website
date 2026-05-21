# Contract: Forms API endpoints

**Date**: 2026-05-12 | **Plan**: [../plan.md](../plan.md)

LIFO web vystavuje 3 endpointy pre formulárové submission-y. Všetky implementované ako **Astro endpoints** v `src/pages/api/`, deployované ako Netlify Functions.

---

## POST `/api/inquiry`

**Purpose**: Spracovať odoslanie kontaktného / dopytového formulára (FR-014, FR-015).

**Alternative**: Formulár môže ísť priamo cez Netlify Forms (HTML attribute `data-netlify="true"`) bez vlastného endpointu. V tom prípade `/api/inquiry` slúži ako **JS-enhanced fallback** s lepšou UX (klientská validácia, lepšie chybové hlásenia).

### Request

**Headers**:
- `Content-Type: application/json`

**Body** (Zod-validated):
```typescript
{
  segment: "partner" | "samosprava" | "investor" | "media" | "other",
  name: string (min 2, max 100),
  email: string (RFC 5322),
  phone?: string (max 30),
  organization: string (min 2, max 200),
  message: string (min 10, max 2000),

  // Segment-špecifické (voliteľné, validované podľa segment-u)
  municipality?: string,           // pre samosprava
  population?: number (positive),  // pre samosprava
  challenge?: string (max 1000),   // pre samosprava
  investmentFocus?: string,        // pre investor

  // GDPR
  gdpr: true,  // explicit consent
  locale: "sk" | "en",

  // Anti-spam
  honeypot: string (must be empty),
  recaptchaToken?: string,  // ak je captcha aktivovaná
}
```

### Response

**Success (200)**:
```json
{
  "ok": true,
  "message": "Ďakujeme, ozveme sa do 5 pracovných dní."
}
```

**Validation error (400)**:
```json
{
  "ok": false,
  "errors": {
    "email": "Neplatný e-mail.",
    "gdpr": "Súhlas je povinný."
  }
}
```

**Spam blocked (400)**:
```json
{ "ok": false, "error": "Blocked." }
```

**Server error (500)**:
```json
{ "ok": false, "error": "Internal error. Skús to neskôr." }
```

### Side effects

1. **Netlify Forms** zápis (alternatíve route — submit formulára s `name="inquiry"` cez Astro proxy).
2. **Brevo transactional email** — notifikácia organizačnému tímu (`tim@lifo.urbanlama.eu`) s plnými detailmi submission-u + identifikovaným segmentom.
3. **Brevo transactional email** — potvrdenie odosielateľovi s textom "Ďakujeme, ozveme sa do X pracovných dní."
4. **Brevo contact** vytvorenie / update s tagom `inquiry-{segment}` (ak gdpr consent zahŕňa newsletter).

### Anti-spam

- Honeypot field `bot-field` (skryté CSS) — non-empty value = block.
- Optional reCAPTCHA v3 token validácia (server-side).
- Rate limit per IP: max 5 submission/hod (Netlify Edge middleware).

---

## POST `/api/newsletter`

**Purpose**: Pridať e-mail do Brevo newsletter zoznamu s double opt-in (FR-016).

### Request

```typescript
{
  email: string (RFC 5322),
  segments?: ("partner" | "samosprava" | "investor" | "media")[],
  gdpr: true,
  locale: "sk" | "en",
  honeypot: string (must be empty),
}
```

### Response

**Success (200)**:
```json
{
  "ok": true,
  "message": "Skontroluj e-mail — poslali sme ti potvrdzovací odkaz."
}
```

**Already subscribed (200)**:
```json
{
  "ok": true,
  "message": "Tento e-mail je už prihlásený."
}
```

**Validation / spam (400)**:
```json
{ "ok": false, "errors": { ... } }
```

### Side effects

1. **Brevo API call** — `POST /contacts` s double opt-in flag. Brevo pošle confirmation e-mail s linkom.
2. Po potvrdení používateľom Brevo nastaví `attribute: gdpr_confirmed = <timestamp>`.
3. Kontakt pridaný do list-ov podľa `segments[]`.

---

## POST `/api/promo-validate`

**Purpose**: Validovať promo kód pri vstupe do ticketing flow (FR-041a).

**Volá sa** z klientského UI keď používateľ klikne "Použiť kód" v ticket pickeri.

### Request

```typescript
{
  code: string (max 32, case-insensitive),
  locale: "sk" | "en",
}
```

### Response

**Valid (200)**:
```json
{
  "ok": true,
  "code": "LIFO27-SAMOSPRAVA",
  "applies_to": {
    "tier_slug": "samosprava",
    "display_name": "Vstupenka pre samosprávy"
  },
  "discount": {
    "type": "unlock" | "percent" | "amount",
    "value": 0 | 10 | 50  // pre percent: %; pre amount: cents
  },
  "expires_at": "2027-01-15T23:59:59Z"
}
```

**Invalid (404)**:
```json
{ "ok": false, "error": "code-not-found" }
```

**Exhausted (410)**:
```json
{ "ok": false, "error": "code-exhausted", "message": "Kód už dosiahol maximálny počet použití." }
```

**Expired (410)**:
```json
{ "ok": false, "error": "code-expired" }
```

### Implementation

Server-side:
1. `stripe.promotionCodes.list({ code, active: true })` — case-insensitive search.
2. Ak nájdený, vráti meta-data o akciovom kóde.
3. **Žiadne** redemption tu sa nevykonáva — len validácia. Skutočná redemption sa robí v Stripe Checkout (kód sa pripojí k Checkout Session).

---

## POST `/api/checkout`

**Purpose**: Vytvoriť Stripe Checkout Session a vrátiť redirect URL (FR-030, FR-037).

### Request

```typescript
{
  tier_slug: string,       // "samosprava" | "investor" | "vip"
  quantity: number (1-50),
  promo_code?: string,
  buyer: {
    email: string,
    organization: string,
    ico?: string,          // SK IČO, povinné pre B2B
    dic?: string,          // DIČ, povinné pre B2B
    ic_dph?: string,       // IČ DPH (DPH platiteľ)
    address: {
      street: string,
      city: string,
      postal_code: string,
      country: string (ISO 3166-1 alpha-2),
    },
  },
  attendees?: Array<{
    name: string,
    email: string,
  }>,
  locale: "sk" | "en",
  metadata?: Record<string, string>,  // UTM, referral
}
```

### Response

**Success (200)**:
```json
{
  "ok": true,
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_..."
}
```

**Tier gated, no code (400)**:
```json
{
  "ok": false,
  "error": "tier-requires-promo-code",
  "message": "Pre vstupenku 'Samospráva' potrebuješ promo kód z pozvánky. Nemáš? Napíš nám cez formulár."
}
```

**Tier sold out (410)**:
```json
{ "ok": false, "error": "tier-sold-out" }
```

**Validation errors (400)**:
```json
{ "ok": false, "errors": { "buyer.ico": "Neplatný formát IČO (musí mať 8 číslic)." } }
```

### Implementation

1. Načítať aktívnu `Price` pre tarifu (Stripe Product → Price kde `active: true`).
2. Ak je tarifa gated (`metadata.gated === "true"`), promo kód je povinný.
3. Ak je promo kód poskytnutý → validovať cez Stripe Promotion Codes API.
4. Validovať `buyer` polia (IČO regex, povinnosť B2B polí).
5. `stripe.checkout.sessions.create({...})` — vytvoriť Checkout Session s `invoice_creation.enabled: true`, line items, customer fields.
6. Vrátiť `session.url`.

---

## Validation rules

| Field             | Rule                                                           |
| ----------------- | -------------------------------------------------------------- |
| `email`           | RFC 5322; max 254 znakov                                        |
| `name` (osoba)    | min 2, max 100 znakov                                          |
| `organization`    | min 2, max 200 znakov                                          |
| `ico` (SK)        | regex `^\d{8}$` (8 číslic); povinné pre B2B                    |
| `dic` (SK)        | regex `^\d{10}$` (10 číslic)                                  |
| `ic_dph` (SK)     | regex `^SK\d{10}$`; voliteľné (len pre DPH platiteľov)        |
| `postal_code` (SK) | regex `^\d{3} ?\d{2}$`                                        |
| `phone`           | E.164 alebo lokálny formát; max 30 znakov                      |
| `message`         | min 10, max 2000 znakov                                        |
| `gdpr`            | musí byť `true`                                                |
| `honeypot`        | musí byť `""` (prázdne); inak block                            |

## Error i18n

Všetky chybové hlásenia sú vrátené **v locale ktorý posiela request** (`locale` field v body). Mapovanie `error code → message` v `src/lib/errors.ts`:

```typescript
const errorMessages = {
  sk: {
    "code-not-found": "Tento kód neexistuje.",
    "code-exhausted": "Kód už dosiahol maximálny počet použití.",
    "code-expired": "Platnosť kódu uplynula.",
    "tier-requires-promo-code": "Pre túto vstupenku potrebuješ kód z pozvánky.",
    "tier-sold-out": "Vstupenky tejto kategórie sú vypredané.",
    "invalid-ico": "Neplatný formát IČO.",
    ...
  },
  en: {
    "code-not-found": "This code does not exist.",
    ...
  },
};
```

## Security

- **Žiadne CORS** — endpoints servujú len pre `lifo.urbanlama.eu` origin (Netlify env config).
- **Rate limiting** — Netlify Edge middleware: 30 req/min/IP pre `/api/*`.
- **Stripe Secret Key** — len v server env vars (`STRIPE_SECRET_KEY`), nikdy nie v klientskom JS.
- **CSP header** — `default-src 'self'; script-src 'self' js.stripe.com plausible.io; frame-src js.stripe.com hooks.stripe.com`.
