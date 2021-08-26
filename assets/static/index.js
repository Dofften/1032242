window.addEventListener("load", function () {
    const loader = document.querySelector(".loader");
    loader.className += " hidden"; // class "loader hidden"
});

const emailRegEx = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const email = document.getElementById('email')
const password = document.getElementById('password')
const form = document.getElementById('form')
const errorElement = document.getElementById('error')



password.setAttribute('type','password')

form.addEventListener('submit', (e) =>{
  let messages = []
  if (email.value === '' || email.value == null) {
    errorElement.style.display = 'block'
    messages.push("Email is required")
  }
  else if (emailRegEx.test(email.value) == false) {
    errorElement.style.display = 'block'
    messages.push("Please enter a valid email address")
  }
  if (password.value === '' || password.value == null) {
    errorElement.style.display = 'block'
    messages.push("Password is required")
  }

  if (messages.length > 0) {
    e.preventDefault()
    errorElement.innerText = messages.join(', ')
  }
})