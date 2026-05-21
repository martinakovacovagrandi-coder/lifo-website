# LIFO Brand Guidelines — Working Draft

> **Status**: Working draft / placeholder. Tieto assety boli vygenerované programaticky na základe referenčných obrázkov od grafika, aby sa odblokoval vývoj webu. **Pri dodaní finálneho brand kit-u od grafika sa všetky súbory v tomto priečinku swapnú 1:1 — implementácia webu izoluje brand tokeny do CSS variable, takže swap je bez zásahu do markupu.**

**Verzia**: 0.1 — 2026-05-12
**Konferencia**: LIFO 2027 — Local Innovation Forum, 11. 2. 2027, Hotel Clarion Bratislava

---

## 1. Logo — koncept

LIFO symbol je geometrický **interlock** z dvoch blok-L tvarov v diagonálnej kompozícii. Vyjadruje prepojenie (samosprávy ↔ kapitál) ako dva blokové elementy zapadajúce do seba s krokovým step-pattern v strede.

### Súbory loga

| Účel                                        | Súbor                                                        |
| ------------------------------------------- | ------------------------------------------------------------ |
| Master (gradient, primárne použitie)        | [01_master/lifo-logo.svg](../01_master/lifo-logo.svg)          |
| Mono čierna — pre svetlé pozadie            | [02_variants/lifo-logo-black.svg](../02_variants/lifo-logo-black.svg) |
| Mono biela — pre tmavé pozadie              | [02_variants/lifo-logo-white.svg](../02_variants/lifo-logo-white.svg) |
| Outline čierna — delikátny variant na svetlom | [02_variants/lifo-logo-outline-black.svg](../02_variants/lifo-logo-outline-black.svg) |
| Outline biela — delikátny variant na tmavom  | [02_variants/lifo-logo-outline-white.svg](../02_variants/lifo-logo-outline-white.svg) |
| Raster exporty (PNG / WebP, 256–2048 px)    | [03_raster/](../03_raster/)                                    |
| Web assety (favicon, iOS, Android, OG image) | [04_web_assets/](../04_web_assets/)                            |

---

## 2. Clear space

Okolo loga musí byť **prázdny priestor minimálne rovný šírke vertikálnej časti L-tvaru** (≈ 14 % z výšky loga).

```
   ┌────────────────────┐
   │  ▓                 │
   │  ▓▓▓▓▓             │
   │      ▓             │  ← clear space okolo dokola
   │      ▓▓▓▓▓         │
   │                    │
   └────────────────────┘
```

Žiadny iný prvok (text, ikona, foto, hrana grafiky) nesmie zasahovať do clear space zóny.

## 3. Minimum size

| Médium    | Minimálna výška loga | Poznámka                                  |
| --------- | -------------------- | ----------------------------------------- |
| Digitál   | **24 px**            | Pod touto veľkosťou používaj favicon       |
| Tlač      | **10 mm**            | Pod 10 mm sa stráca čitateľnosť hrán     |
| Favicon   | 16 / 32 / 48 px       | Pripravené raster súbory, neukladaj logo vektoroho |

## 4. Do's & Don'ts

### ✅ DO

- Používaj logo **bez modifikácie**: presné proporcie, presné farby, žiadne dopĺňajúce efekty
- **SVG** pre web a digitál (skálovateľné, ostré pri každej veľkosti)
- **PNG s priehľadným pozadím** tam kde SVG nie je možné
- Logo na **rovnomernom pozadí** alebo na fotografii s dostatočným kontrastom
- Pri fotopozadí použij mono variantu (čiernu / bielu) ak gradient stráca čitateľnosť

### ❌ DON'T

- ❌ Nedeformuj logo (žiadne stretching, skewing, rotácia)
- ❌ Nemeň farby gradientu (magenta a teal sú definované v `colors.md`)
- ❌ Nepridávaj tieň, glow, outline okolo loga (okrem dodaných outline variantov)
- ❌ Neumiestňuj logo na pozadie ktoré "kradne" gradient (napr. na fotku obloh, ružové stenu)
- ❌ Nezmenšuj pod minimum size
- ❌ Nepoužívaj rasterové verzie tam kde sa dá použiť SVG
- ❌ Nevkladaj text do clear space zóny okolo loga

## 5. Farby

Plné HEX / RGB / CMYK kódy v [colors.md](colors.md).

| Token        | HEX        | Použitie                                  |
| ------------ | ---------- | ----------------------------------------- |
| Magenta      | `#D6307A`  | Primárny akcent, gradient start            |
| Teal         | `#36A2A8`  | Sekundárny akcent, gradient end           |
| Ink          | `#0A0A0A`  | Primárny text, mono čierny logo variant   |
| Paper        | `#FFFFFF`  | Pozadie, text na tmavom, mono biely logo |
| Navy (tmavé pozadie) | `#0C1223` | OG image, dark mode hero sekcie         |

## 6. Typografia

Pracovný výber: **Inter Bold** pre nadpisy / wordmark, **Inter Regular** pre body text.

Detaily v [typography.md](typography.md).

## 7. Wordmark "LIFO"

Logo často sprevádza wordmark "LIFO" alebo "LIFO 2027" alebo plné "Local Innovation Forum".

**Použitia**:
- "**LIFO**" — primárny wordmark v hlavičke webu, hero, materiáloch
- "**LIFO 2027**" — pre tento ročník (časové ukotvenie v komunikácii)
- "**LIFO — Local Innovation Forum**" — pre prvé použitie v dokumente / kde treba kontext

## 8. Open Graph image (sociálne zdieľanie)

Pripravené v [04_web_assets/](../04_web_assets/):
- `og-image-1200x630.png` — SK verzia (LinkedIn / Facebook / WhatsApp / Slack)
- `og-image-1200x630-en.png` — EN verzia
- `twitter-card-1200x600.png` — X / Twitter

V `<head>` webu:
```html
<meta property="og:image" content="https://[domena]/og-image-1200x630.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://[domena]/twitter-card-1200x600.png" />
```

## 9. Favicon

Pripravené v [04_web_assets/](../04_web_assets/):

V `<head>` webu:
```html
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180.png" />
<link rel="manifest" href="/site.webmanifest" />
```

`site.webmanifest` (Android / PWA):
```json
{
  "name": "LIFO 2027",
  "short_name": "LIFO",
  "icons": [
    { "src": "/android-chrome-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0C1223",
  "background_color": "#0C1223",
  "display": "standalone"
}
```

## 10. Implementačný hint pre vývoj

Brand tokeny majú byť izolované v jednom CSS súbore (napr. `src/styles/tokens.css`), aby swap na finálne hodnoty od grafika bol triviálny:

```css
:root {
  --lifo-magenta: #D6307A;
  --lifo-teal: #36A2A8;
  --lifo-ink: #0A0A0A;
  --lifo-paper: #FFFFFF;
  --lifo-navy: #0C1223;
  --lifo-gradient: linear-gradient(135deg, var(--lifo-magenta) 0%, var(--lifo-teal) 100%);

  --lifo-font-display: 'Inter', system-ui, -apple-system, sans-serif;
  --lifo-font-body: 'Inter', system-ui, -apple-system, sans-serif;
}
```

Pri dodaní finálneho brand kit-u od grafika prepíš HEX hodnoty + font názvy v tomto súbore. Žiadne ďalšie zmeny v markupu nie sú potrebné.

---

## Limity tohto draftu

Toto sú **programmatic placeholder** assety. Limity:

1. **3D rendered variant** (na mramore) nie je obsiahnutý — vyžaduje samostatný 3D rendering tool a poskytne ho grafik.
2. **Adobe Illustrator `.ai` master** chýba — SVG je funkčný ekvivalent pre 95 % use cases, grafik dodá `.ai` keď bude treba editovať v Illustratore.
3. **Presné farby** sú odhadnuté z referenčných obrázkov — môžu sa mierne líšiť od grafikových definícií. Pri swap-e za finálne hodnoty stačí prepísať HEX v CSS tokenoch.
4. **Typografia** je default (Inter — free, OFL) — grafik môže doporučiť licencovaný premium font (Neue Haas Grotesk, Suisse Int'l, Graphik) ktorý sa swapne cez `--lifo-font-display` token.
