module.exports = {
  content: [
    "./templates/main/*.html",
    "./templates/includes/*.html",
    "./templates/errors/*.html",
    "./templates/auth/*.html",
    "./templates/dashboard/shared/*.html",
    "./templates/dashboard/partials/*.html"

  ],

  plugins: [
    require('@tailwindcss/forms'),
    require("flowbite/plugin")
  ],
}
