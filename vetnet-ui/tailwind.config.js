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
  plugins: [],
}
