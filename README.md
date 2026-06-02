# LIFO 2027 — Local Innovation Forum

Web pre konferenciu LIFO 2027 (Local Innovation Forum), ktorá sa koná **11. februára 2027 v Bratislave**.

🌐 **Live**: https://lifo.urbanlama.eu

## Tech stack

- **Astro 5** + TypeScript + Tailwind 4
- **Netlify** (hosting + Forms + auto-deploy)
- **GitHub** (verzia + collaborácia)

## Editácia obsahu

Texty sú v markdown súboroch:

- **`src/content/pages/sk/`** — slovenské texty
- **`src/content/pages/en/`** — anglické texty

Edituj priamo cez GitHub web editor (klikni súbor → ceruzka → Commit). Netlify nasadí novú verziu do 60-90 sekúnd.

## Lokálny vývoj

```bash
npm install
npm run dev     # http://localhost:4321
npm run build   # produkčný build do dist/
```

## Projekty

Web je súčasť portfólia [Excelerate](https://excelerate.sk) — okrem LIFO 2027 zahŕňa aj projekt Urban Láma.
