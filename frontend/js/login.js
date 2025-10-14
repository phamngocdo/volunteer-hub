import { initHeader } from "./main.js";
function initLoginPage() {
  const form = document.querySelector(".login-form");

  if (form) {
    console.log("Login form found. Initializing...");
    initEmailLogin(form);
  } else {
    console.warn("Login form (.login-form) not found on this page.");
  }

}


function initEmailLogin(form) {
  const emailInput = form.querySelector("#email");
  const passwordInput = form.querySelector("#password");
  const loginButton = form.querySelector(".btn-login");

  const errorBox = document.createElement("div");
  errorBox.className = "error-message";
  Object.assign(errorBox.style, {
    color: "#ff4d4d",
    fontSize: "14px",
    marginTop: "10px",
    display: "none",
  });
  form.insertBefore(errorBox, loginButton);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      showError(errorBox, "Vui lòng nhập đầy đủ thông tin.");
      return;
    }

    loginButton.disabled = true;
    loginButton.innerText = "Đang đăng nhập...";

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("token_type", data.token_type);
        initHeader();
        window.location.href = "/";
      } else if (res.status === 401) {
        const data = await res.json();
        showError(errorBox, data.detail || "Email hoặc mật khẩu sai.");
      } else {
        showError(errorBox, "Có lỗi xảy ra. Vui lòng thử lại.");
      }
    } catch (err) {
      console.error(err);
      showError(errorBox, "Không thể kết nối đến máy chủ.");
    } finally {
      loginButton.disabled = false;
      loginButton.innerText = "Đăng nhập";
    }
  });
}

function showError(element, message) {
  element.innerText = message;
  element.style.display = "block";
}

initLoginPage();