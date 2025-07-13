/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'walmart-blue': '#004c91',
        'walmart-gold': '#ffc220',
      },
    },
  },
  plugins: [],
};