/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: { 
      backgroundImage: {
      'bg1': "url('/static/resources/bg.png')"  
    }},
  },
  plugins: [],
}

