/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'newspaper-headline': ['Playfair Display', 'serif'],
        'newspaper-body': ['Crimson Text', 'serif'],
      },
      colors: {
        'newspaper': {
          'black': '#1a1a1a',
          'gray': '#4a4a4a',
          'light-gray': '#f5f5f5',
          'border': '#d1d1d1',
          'accent': '#8b0000',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-in': 'slideIn 0.8s ease-out',
      }
    },
  },
  plugins: [],
}
