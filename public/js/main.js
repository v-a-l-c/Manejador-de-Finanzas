function submitEmail() {
  const emailInput = document.getElementById("emailInput").value;
  if (emailInput) {
      window.location.href = `signup.html?email=${encodeURIComponent(emailInput)}`;
  } else {
      alert("Por favor, ingresa un correo electrónico válido.");
  }
}

function submitLogin() {
  const usernameInput = document.getElementById("usernameInput").value;
  const passwordInput = document.getElementById("passwordInput").value;
  if (usernameInput && passwordInput) {
      alert(`¡Bienvenido, ${usernameInput}!`);
  } else {
      alert("Por favor, ingresa un nombre de usuario y contraseña.");
  }
}

function submitSignup() {
  const usernameInput = document.getElementById("usernameInput").value;
  const passwordInput = document.getElementById("passwordInput").value;
  const mailInput = document.getElementById("mailInput").value;
  if (usernameInput && passwordInput && mailInput) {
      alert(`¡Gracias por registrarte, ${usernameInput}!`);
  } else {
      alert("Por favor, ingresa un nombre de usuario, contraseña y correo electrónico.");
  }
}

document.getElementById("emailForm").addEventListener("submit", (event) => {
  event.preventDefault();  // Evita el envío normal del formulario
  submitEmail();
});

document.getElementById("loginForm").addEventListener("submit", (event) => {
  event.preventDefault();  // Evita el envío normal del formulario
  submitLogin();
});

document.getElementById("signupForm").addEventListener("submit", (event) => {
  event.preventDefault();  // Evita el envío normal del formulario
  submitSignup();
});
