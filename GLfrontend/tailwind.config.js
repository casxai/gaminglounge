/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [
    require('flowbite/plugin')
  ],
  content: [
    "./index.html",
    "./src/**/*.{html,vue,js,ts,jsx,tsx}", // joey added html
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'hero-pattern': "url('/src/assets/img/bg/hero.svg')",
        'header-texture': "url('/src/assets/img/navbar/header.png')",
      },
      colors: {
        'purple1': '#A35DD2', // for border
        'violet1': '#8150CA',  // for border
        'purple_main2': '#4B2E75', // main color of the website
        'purple_main': '#0A001266',
        'blue_link': '#8AC6FD', // color for link
        'dark_purple': '#020816', // color ng background
        'white': '#f9f9f9'
      },
      borderRadius: {
        'none': '0',
        'sm': '0.125rem',
        DEFAULT: '0.25rem',
        DEFAULT: '4px',
        'md': '0.375rem',
        'lg': '0.5rem',
        'full': '20px',
        'img':'9999px',
        'large': '100px',
      },
      fontSize: {
        sm: '0.8rem',
        base: '1rem',
        xl: '1.25rem',
        '2xl': '1.563rem',
        '3xl': '1.953rem',
        '4xl': '2.441rem',
        '5xl': '3.052rem',
      },
      borderColor:{
        'border2': '#4B2E75',
        'border3': '#8150CA', 
      },



      // backgroundImage: {
      //   'hero-pattern': "url('/assets/img/bg/bg-1.svg')",
      //   'footer-texture': "url('/img/footer-texture.png')",
      // }
    },
  },
  plugins: [],
}

