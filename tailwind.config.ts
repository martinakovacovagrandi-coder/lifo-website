import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        lifo: {
          magenta: "#D6307A",
          teal: "#36A2A8",
          ink: "#0A0A0A",
          paper: "#FFFFFF",
          navy: "#0C1223",
        },
      },
      fontFamily: {
        display: ["Inter", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
        body: ["Inter", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
      },
      backgroundImage: {
        "lifo-gradient": "linear-gradient(135deg, #D6307A 0%, #36A2A8 100%)",
      },
    },
  },
} satisfies Config;
