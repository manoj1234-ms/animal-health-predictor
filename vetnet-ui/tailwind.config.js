/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'vet-primary': '#0f172a',
        'vet-secondary': '#1e293b',
        'vet-accent': '#3b82f6',
        'vet-success': '#22c55e',
        'vet-warning': '#f59e0b',
        'vet-danger': '#ef4444',
      }
    },
  },
  plugins: [
    function ({ addUtilities }) {
      addUtilities({
        '.scrollbar-thin': {
          'scrollbar-width': 'thin',
          'scrollbar-color': '#334155 rgba(15, 23, 42, 0.2)',
        },
      })
    }
  ],
}
