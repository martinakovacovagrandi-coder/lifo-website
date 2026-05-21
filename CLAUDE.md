<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
[specs/001-conference-site/plan.md](specs/001-conference-site/plan.md)

Supporting documents:
- [specs/001-conference-site/spec.md](specs/001-conference-site/spec.md) — Feature specification
- [specs/001-conference-site/research.md](specs/001-conference-site/research.md) — Technical decisions + rationale
- [specs/001-conference-site/data-model.md](specs/001-conference-site/data-model.md) — Entities + storage mapping
- [specs/001-conference-site/contracts/](specs/001-conference-site/contracts/) — API + content-collection contracts
- [specs/001-conference-site/quickstart.md](specs/001-conference-site/quickstart.md) — Dev getting-started

**Stack summary**: Astro 5 + TypeScript + Tailwind 4 on Netlify; Stripe for ticketing/invoicing; Brevo for email (newsletter + transactional); Decap CMS for content editing; Plausible analytics; Vitest + Playwright for testing. Content lives in `src/content/` markdown collections; payments in Stripe; submissions in Netlify Forms. No custom backend/DB in v1.
<!-- SPECKIT END -->
