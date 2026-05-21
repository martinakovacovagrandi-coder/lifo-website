# Contract: Stripe Webhook handler

**Date**: 2026-05-12 | **Plan**: [../plan.md](../plan.md)

## POST `/api/webhook-stripe`

**Purpose**: Spracovať Stripe webhook udalosti (`checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, atď.) — generovať e-ticket, posielať e-maily, sledovať stav objednávky.

## Bezpečnosť

- Vlastné Astro endpoint volané **iba Stripe-om** (z konkrétnych IP rozsahov).
- **Signature verification** povinné — overiť `Stripe-Signature` header proti `STRIPE_WEBHOOK_SECRET`. Neoverené requesty → 400.
- Endpoint je **idempotent** — Stripe môže poslať ten istý event viackrát, retry safe.

## Request format

**Headers**:
- `Stripe-Signature: t=<timestamp>,v1=<signature>`
- `Content-Type: application/json`

**Body**: Stripe event objekt (rôzne `type`).

## Spracovávané eventy

### `checkout.session.completed`

Najdôležitejší event — kupujúci dokončil platbu kartou.

**Akcie**:
1. Načítať full Checkout Session detaily (line items, customer, invoice_id).
2. Vygenerovať **e-ticket PDF** s QR kódom (unikátny token, hash zo session.id + secret).
3. Odoslať cez Brevo:
   - **Kupujúcemu**: ďakovný e-mail s e-ticketom + invoice link.
   - **Organizátorom** (`tim@lifo.urbanlama.eu`): notif "Nová objednávka: tarifa X, kupujúci Y".
4. Vytvoriť / update **Brevo Contact** s atribútmi (segment podľa tarify, locale).
5. (Ak je v scope) prirátať redeemed count k internému tracking-u promo kódu.

**Response**: `200 OK` s `{ received: true }`.

### `invoice.paid`

Pre bank transfer flow — kupujúci zaplatil prevodom.

**Akcie**:
- Rovnaké ako `checkout.session.completed` (Stripe samé vie kedy invoice prešla z `open` na `paid`).
- Ak používateľ ešte nedostal e-ticket (čakanie na payment), TERAZ pošli.

### `invoice.payment_failed`

Karta zamietnutá alebo prevod zlyhal.

**Akcie**:
1. Notif kupujúcemu cez Brevo: "Platba zlyhala — skús znova alebo nás kontaktuj."
2. Notif organizátorom (severity: warn).
3. Po 3 retry uvoľniť rezervovanú kapacitu vstupenky.

### `customer.subscription.*` (FUTURE)

Pre v1 mimo scope — LIFO 2027 je one-shot platba, nie subscription. Endpoint **logne event a ignoruje** (nevyhodí chybu, aby Stripe nemal failed deliveries).

### `charge.refunded`

Manual refund z Stripe dashboardu po žiadosti o storno (FR-039).

**Akcie**:
1. Notif kupujúcemu: "Refund spracovaný, X €."
2. Notif organizátorom.
3. **Invalidovať e-ticket QR token** (admin operácia — pozri sekciu nižšie).
4. Vrátiť uvoľnenú vstupenku do kapacity.

## Idempotency

Stripe môže poslať rovnaký event viackrát (network retry). Endpoint musí byť **idempotent**:

1. Pre každý event Stripe poskytne `event.id` (unique).
2. Pred spracovaním skontrolovať `KV.get(event.id)` — ak existuje, vrátiť `{ received: true, duplicate: true }` bez vykonania akcií.
3. Po úspešnom spracovaní `KV.set(event.id, true, ttl: 7 days)`.

**Storage**: Netlify Blobs alebo external KV (Upstash / Cloudflare KV). Pre v1 jednoduchá in-memory cache v Function _NESTAČÍ_ (funkcie sú stateless). Použiť Netlify Blobs.

## Side effects pipeline

```text
checkout.session.completed
   ↓
[1] Signature verify ───[fail]──> 400 + log
   ↓ pass
[2] Idempotency check ──[dup]──> 200 { duplicate: true }
   ↓ new
[3] Load session details (Stripe API)
   ↓
[4] Generate e-ticket PDF
   │
   ├─► [5a] Brevo: send email to buyer (with PDF attachment)
   ├─► [5b] Brevo: notify organizers
   └─► [5c] Brevo: upsert contact (with tags)
   ↓
[6] Mark event processed (KV)
   ↓
[7] Return 200 { received: true }
```

Ak ktorýkoľvek z `[5a-c]` zlyhá → log + retry-able (Brevo SDK má built-in retry).

Ak `[4]` zlyhá → kritická chyba, alert organizátorom, return 500 (Stripe retryne).

## E-ticket QR token

QR kód na e-tickete obsahuje URL:
```
https://lifo.urbanlama.eu/check-in?t=<token>
```

`<token>` je signed JWT (HS256, secret = env var):
```json
{
  "sub": "<order_id>",
  "tier": "samosprava",
  "att": "<attendee_email>",
  "evt": "lifo-2027",
  "iss": "lifo.urbanlama.eu",
  "exp": 1771113600   // event end + 1 deň
}
```

**Validačná logika** na check-in stránke (v deň eventu):
1. Decode JWT, verify signature, check `exp`.
2. Look up `order_id` v Stripe — verify `status: paid`, žiadny refund.
3. Mark attendee `checked_in: true` (Brevo contact attribute).
4. Display "Vitajte, [meno]" na obrazovke iPadu / scanner-u.

**Out of scope v1**: Plnohodnotná check-in aplikácia. Tento endpoint slúži ako placeholder; pred eventom môžeme rozšíriť alebo použiť dedicated tool (Eventbrite Organizer / Boomset / vlastný React app).

## Logging

- **Production**: každý webhook event log-uje do Netlify Function logs s context (event.id, type, processing_time_ms).
- **Severity**:
  - `info` — successful processing.
  - `warn` — payment failed, retry-able errors.
  - `error` — signature mismatch, idempotency KV failures, Brevo API down.
- **Alerts** (out of scope v1, but plan for): warn / error → Slack webhook do organizátorského kanála.

## Test mode workflow

Pred go-live všetky webhooks testovať s Stripe test mode:

1. `stripe listen --forward-to localhost:4321/api/webhook-stripe` (lokálny dev).
2. `stripe trigger checkout.session.completed` → end-to-end test.
3. Skontrolovať že e-ticket PDF prišiel + má správny QR.
4. Skontrolovať že Brevo notif prišiel organizátorom.
5. Skontrolovať že kontakt sa vytvoril v Brevo s správnym tag-om.

## Failure modes

| Failure                              | Symptom                                    | Mitigation                                                   |
| ------------------------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| Webhook secret rotation              | Stripe vraj signature mismatch             | Update `STRIPE_WEBHOOK_SECRET` v Netlify env, redeploy       |
| Brevo API down                       | E-ticket sa nepošle                        | Stripe retryne event do 72h; ak pretrváva, manuálne resend |
| PDF generation OOM                   | Function timeout                           | Resize Function memory (Netlify allows up to 3 GB)            |
| KV unavailability                    | Idempotency check fails → duplicate sends | Tolerable na krátky čas (Stripe-am je vedomé)                |
