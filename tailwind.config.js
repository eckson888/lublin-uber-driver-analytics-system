/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: { 
      backgroundImage: 
      {
      'bg1': "url('/static/resources/bg_blur.png')"  
      },
      boxShadow:
      {
      'shad_big' : '0px 0px 60px 30px rgba(0, 0, 0, 0.95)',
      'shad_button' : '0px 0px 49px -14px rgba(110, 0, 253, 1)'
      }
      },
  },
  plugins: [],
}

