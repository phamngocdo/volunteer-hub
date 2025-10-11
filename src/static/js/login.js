document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".login-form");
  const emailInput = document.querySelector("#email");
  const passwordInput = document.querySelector("#password");
  const loginButton = form.querySelector(".btn-login");

  const errorBox = document.createElement("div");
  errorBox.className = "error-message";
  errorBox.style.color = "#ff4d4d";
  errorBox.style.fontSize = "14px";
  errorBox.style.marginTop = "10px";
  errorBox.style.display = "none";
  form.insertBefore(errorBox, loginButton);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      errorBox.innerText = "⚠️ Vui lòng nhập đầy đủ thông tin.";
      errorBox.style.display = "block";
      return;
    }

    loginButton.disabled = true;
    loginButton.innerText = "Đang đăng nhập...";

    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        window.location.href = "/";
      } else if (response.status === 401) {
        const data = await response.json();
        errorBox.innerText = (data.detail || "Email hoặc mật khẩu sai.");
        errorBox.style.display = "block";
      } else {
        errorBox.innerText = "Có lỗi xảy ra. Vui lòng thử lại.";
        errorBox.style.display = "block";
      }
    } catch (err) {
      errorBox.innerText = "Không thể kết nối đến máy chủ.";
      errorBox.style.display = "block";
    } finally {
      loginButton.disabled = false;
      loginButton.innerText = "Đăng nhập";
    }
  });
});
