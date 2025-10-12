/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'blue': {
          400: '#60a5fa',
          600: '#2563eb',
        },
      },
    },
  },
  plugins: [],
}
