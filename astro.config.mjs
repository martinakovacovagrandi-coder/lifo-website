// @ts-check
import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://lifo.urbanlama.eu",
  trailingSlash: "ignore",
  i18n: {
    locales: ["sk", "en"],
    defaultLocale: "sk",
    routing: {
      prefixDefaultLocale: false,
    },
  },
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap({
      i18n: {
        defaultLocale: "sk",
        locales: {
          sk: "sk-SK",
          en: "en-US",
        },
      },
    }),
  ],
});
