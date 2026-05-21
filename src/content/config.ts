import { defineCollection, z } from "astro:content";

const pages = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string().min(2),
    subtitle: z.string().optional(),
    tagline: z.string().optional(),
    description: z.string().optional(),
    date: z.string().optional(),
    venue: z.string().optional(),
    ctaPrimary: z
      .object({ label: z.string(), href: z.string() })
      .optional(),
    ctaSecondary: z
      .object({ label: z.string(), href: z.string() })
      .optional(),
    ctaTertiary: z
      .object({ label: z.string(), href: z.string() })
      .optional(),
    locale: z.enum(["sk", "en"]),
    order: z.number().int().nonnegative().default(99),
  }),
});

export const collections = { pages };
