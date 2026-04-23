/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'joj-blue': '#0057B7',
        'joj-yellow': '#FFDD00',
        'military-green': '#4B5320',
        'military-khaki': '#C3B091',
      },
    },
  },
  plugins: [],
};
