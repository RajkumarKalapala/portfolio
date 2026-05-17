/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Syne'", "sans-serif"],
        body: ["'Outfit'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        bg: {
          primary: "#080c14",
          secondary: "#0d1424",
          card: "#0f1829",
          elevated: "#141e33",
        },
        accent: {
          cyan: "#00d4ff",
          teal: "#00b4cc",
          amber: "#f59e0b",
          muted: "#1a3a5c",
        },
        text: {
          primary: "#e8f0fe",
          secondary: "#8fa8c8",
          muted: "#4a6080",
        },
      },
    },
  },
  plugins: [],
};
