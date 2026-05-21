# LIFO — Typography

> **Status**: Working draft. Finálny výber písma confirmuje grafik; tokeny sú izolované v CSS, takže swap je 1-line zmena.

## Pracovný font: Inter

**Inter** (Rasmus Andersson, OFL licensed — free for any use) je moderný neutrálny grotesk s vynikajúcou čitateľnosťou na obrazovkách aj v tlači.

- Free na web aj print (SIL Open Font License)
- Variabilné weights (100–900)
- Široká podpora znakov (latinka, cyrilika, diakritika SK/CZ/PL/DE)
- Dostupné cez Google Fonts: https://fonts.google.com/specimen/Inter

## Hierarchia

| Úroveň              | Font          | Size                                | Weight       | Použitie                                |
| ------------------- | ------------- | ----------------------------------- | ------------ | --------------------------------------- |
| Display (hero)      | Inter         | `clamp(2.5rem, 6vw, 5rem)`          | **Bold 700** | LIFO wordmark, hero headline            |
| H1                  | Inter         | `clamp(2rem, 4vw, 3rem)`            | **Bold 700** | Hlavné sekcie ("Pre partnerov", atď.) |
| H2                  | Inter         | `clamp(1.5rem, 3vw, 2.25rem)`       | **SemiBold 600** | Podsekcie                            |
| H3                  | Inter         | `1.25rem`                           | **SemiBold 600** | Karty, listy                         |
| Body                | Inter         | `1rem (16px)`                       | Regular 400  | Hlavný text                             |
| Small / Meta        | Inter         | `0.875rem (14px)`                   | Regular 400  | Captions, dátumy, footnotes             |
| Caps                | Inter         | `0.75rem (12px)`, `letter-spacing: 0.08em` | **Bold 700** | Eyebrow labels, tags                    |

## Line-height

| Veľkosť     | Line-height |
| ----------- | ----------- |
| Display / H1 | `1.05`     |
| H2 / H3     | `1.2`        |
| Body        | `1.55`       |
| Small       | `1.4`        |

## Letter-spacing

| Použitie       | Hodnota             |
| -------------- | ------------------- |
| Display / H1   | `-0.02em` (tighter) |
| H2 / H3        | `-0.01em`           |
| Body           | `0` (default)       |
| Caps / Eyebrow | `0.08em` (looser)   |

## Použitie LIFO wordmark-u

Wordmark "LIFO" má vždy:
- **Bold 700** weight
- **UPPERCASE** capitalizácia
- **Tight letter-spacing** (-0.02em na display veľkosti)

Príklad:
```html
<h1 class="lifo-wordmark">LIFO</h1>
```

```css
.lifo-wordmark {
  font-family: var(--lifo-font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  font-size: clamp(3rem, 8vw, 6rem);
  line-height: 1;
}
```

## CSS tokens

```css
:root {
  --lifo-font-display: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --lifo-font-body: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --lifo-font-mono: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
}
```

## Load (Google Fonts)

V `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

Alternatívne **self-hosted** (lepšie pre výkon + GDPR):
1. Stiahnuť Inter z https://rsms.me/inter/
2. Umiestniť `.woff2` súbory do `public/fonts/`
3. `@font-face` deklarácie v CSS

## Alternatívy ak grafik chce premium font

Konzistentné s "premium grotesk" rodinou (FR-019 v specu):

| Font              | Licencia                | Cena (orientačne) |
| ----------------- | ----------------------- | ----------------- |
| **Inter**         | OFL (free)              | $0                |
| IBM Plex Sans     | OFL (free)              | $0                |
| **Neue Haas Grotesk** | Komerčný (Linotype) | ~ €350 pre web   |
| **Suisse Int'l**  | Komerčný (Swiss Typefaces) | ~ €390 pre web |
| **Graphik**       | Komerčný (Commercial Type) | ~ $400 pre web |
| **GT America**    | Komerčný (Grilli Type)  | ~ €270 pre web    |

**Odporúčanie**: Začať s Inter (free, dobré pre launch). Ak grafik trvá na premium fonte (napr. Neue Haas Grotesk), kúpiť pri schválení brand kit-u a swapnúť cez CSS token bez zásahu do markupu.

## Don'ts

- ❌ **Žiadne dekoratívne / zaoblené fonty** (Comic Sans, Pacifico, atď.)
- ❌ **Montserrat** — vyhradené (per pôvodný PN brand brief)
- ❌ **Mix-ovanie viacerých rodín** v rámci jednej stránky (drž sa Inter + jednej monospace pre code)
- ❌ **Italic v nadpisoch** (Inter italic je OK pre body emfázu, ale nie pre H1/H2)
- ❌ **Justify alignment** pre body text (vytvára nerovnomerné medzery)
