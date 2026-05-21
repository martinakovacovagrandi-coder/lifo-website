# LIFO — Color System

> **Status**: Working draft. Hodnoty odhadnuté z referenčných obrázkov od grafika. Pri dodaní finálneho brand kit-u sa hodnoty swapnú.

## Brand colors

### Primary — Magenta

| Format        | Value                            |
| ------------- | -------------------------------- |
| HEX           | `#D6307A`                        |
| RGB           | `214, 48, 122`                   |
| HSL           | `333°, 64%, 51%`                 |
| CMYK *(approx)* | `0, 78, 43, 16`                |
| Pantone *(approx)* | `2039 C` (over ku grafikovi pre presné Pantone) |

**Použitie**: Akcenty, CTA tlačidlá, gradient start point, hyperlinky pri hover, dôležité dátumy.

### Primary — Teal

| Format        | Value                            |
| ------------- | -------------------------------- |
| HEX           | `#36A2A8`                        |
| RGB           | `54, 162, 168`                   |
| HSL           | `183°, 51%, 44%`                 |
| CMYK *(approx)* | `68, 4, 19, 34`                |
| Pantone *(approx)* | `7711 C` (over ku grafikovi)  |

**Použitie**: Sekundárne akcenty, gradient end point, success states, decorative elements.

### Neutral — Ink (čierna)

| Format | Value          |
| ------ | -------------- |
| HEX    | `#0A0A0A`      |
| RGB    | `10, 10, 10`   |

**Použitie**: Primárny text na svetlom pozadí, mono čierny logo variant.

### Neutral — Paper (biela)

| Format | Value                |
| ------ | -------------------- |
| HEX    | `#FFFFFF`            |
| RGB    | `255, 255, 255`      |

**Použitie**: Pozadie webu (svetlý režim), text na tmavom pozadí, mono biely logo variant.

### Neutral — Navy (tmavé pozadie)

| Format | Value             |
| ------ | ----------------- |
| HEX    | `#0C1223`         |
| RGB    | `12, 18, 35`      |

**Použitie**: OG image pozadie, dark mode sekcie, hero overlay na fotografiách.

## Gradient

Brand gradient prebieha od **Magenta** (top-left) po **Teal** (bottom-right), uhol 135°.

CSS:
```css
background: linear-gradient(135deg, #D6307A 0%, #36A2A8 100%);
```

SVG:
```xml
<linearGradient id="lifoGrad" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#D6307A"/>
  <stop offset="1" stop-color="#36A2A8"/>
</linearGradient>
```

## Použitie pomeru farieb

Pre celkový vizuálny dojem dodržiavaj rough pomer:

- **60 %** — Neutral (Paper / Ink / Navy podľa light/dark mode)
- **30 %** — Sekundárne neutrály (sivé tóny, foto, biele plochy)
- **10 %** — Brand akcenty (Magenta + Teal + gradient) — pre CTA, ikonografiu, kľúčové dátumy

Brand farby nemajú "premaľovať" stránku — sú to akcenty na neutrálnom inštitucionálnom plátne.

## Accessibility — kontrast

Tieto kombinácie sú **WCAG 2.1 AA compliant** pre normálny text (kontrast min 4.5:1):

| Foreground   | Background   | Kontrast     | Status   |
| ------------ | ------------ | ------------ | -------- |
| Ink #0A0A0A  | Paper #FFFFFF | 19.7:1      | ✓ AAA   |
| Paper #FFFFFF | Navy #0C1223  | 16.8:1      | ✓ AAA   |
| Paper #FFFFFF | Magenta #D6307A | 4.9:1     | ✓ AA    |
| Ink #0A0A0A  | Magenta #D6307A | 4.0:1     | ✗ pod AA — nepoužívaj na text |
| Paper #FFFFFF | Teal #36A2A8 | 3.0:1       | ✗ pod AA — nepoužívaj na text |
| Ink #0A0A0A  | Teal #36A2A8 | 6.5:1       | ✓ AA    |

**Záver pre text**:
- Body text **vždy** Ink alebo Paper na neutrálnom pozadí
- Pre **veľký text** (≥ 24px regular alebo ≥ 18px bold) je WCAG AA 3:1 → Magenta/Teal pozadie s bielym/čiernym textom OK
- Pre **akcenty bez textu** (ikony, separátory) — žiadne kontrastné požiadavky
