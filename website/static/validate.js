function showErrors(form, errors) {
  let box = form.querySelector(".js-errors");
  if (!box) {
    box = document.createElement("div");
    box.className = "js-errors w-100";
    form.prepend(box);
  }
  box.innerHTML = "";
  errors.forEach(function (msg) {
    const p = document.createElement("div");
    p.className = "alert alert-danger py-2 mb-2";
    p.textContent = msg;
    box.appendChild(p);
  });
}

function val(form, name) {
  return form.querySelector('[name="' + name + '"]').value;
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    const errors = [];
    const password = val(registerForm, "password");
    const confirm = val(registerForm, "confirm_password");
    if (!val(registerForm, "name").trim()) errors.push("Name is required");
    if (!val(registerForm, "email").trim()) errors.push("Email is required");
    if (Array.from(val(registerForm, "name").trim()).length > 100) errors.push("Name is too long (100 characters at most)");
    if (Array.from(val(registerForm, "email").trim()).length > 255) errors.push("Email is too long (255 characters at most)");
    if (new TextEncoder().encode(password).length > 72) errors.push("Password is too long (72 UTF-8 bytes at most)");
    if (!password) errors.push("Password is required");
    if (!confirm) errors.push("Confirm password is required");
    if (password && confirm && password !== confirm) errors.push("Passwords do not match");
    if (errors.length) {
      e.preventDefault();
      showErrors(registerForm, errors);
    }
  });
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    const errors = [];
    if (!val(loginForm, "email").trim()) errors.push("Email is required");
    if (!val(loginForm, "password")) errors.push("Password is required");
    if (errors.length) {
      e.preventDefault();
      showErrors(loginForm, errors);
    }
  });
}

document.querySelectorAll(".title-form").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    const title = val(form, "title").trim();
    const errors = [];
    if (!title) errors.push("Title is required");
    else if (Array.from(title).length > 200) errors.push("Title is too long (200 characters at most)");
    if (errors.length) {
      e.preventDefault();
      showErrors(form, errors);
    }
  });
});