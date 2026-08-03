/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#708C69',
        primaryDark: '#5B7256',
        primaryLight: '#9BB39A',
        mint: '#E8EFE6',
        leaf: '#86A67E',
        moss: '#3F5A44',
      },
      fontFamily: {
        'lato': ['Lato', 'sans-serif'],
        'roboto': ['Roboto', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
