document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".login-form");
  const firstNameInput = document.querySelector("#first_name");
  const lastNameInput = document.querySelector("#last_name");
  const emailInput = document.querySelector("#email");
  const phoneInput = document.querySelector("#phone");
  const passwordInput = document.querySelector("#password");
  const confirmPasswordInput = document.querySelector("#confirm_password");
  const roleSelect = document.querySelector("#role");
  const registerButton = form.querySelector(".btn-login");

  const messageBox = document.createElement("div");
  messageBox.className = "message-box";
  messageBox.style.fontSize = "14px";
  messageBox.style.marginTop = "10px";
  messageBox.style.display = "none";
  form.insertBefore(messageBox, registerButton);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const first_name = firstNameInput.value.trim();
    const last_name = lastNameInput.value.trim();
    const email = emailInput.value.trim();
    const phone_number = phoneInput.value.trim();
    const password = passwordInput.value.trim();
    const confirm_password = confirmPasswordInput.value.trim();
    const role = roleSelect.value;

    if (!first_name || !last_name || !email || !phone_number || !password || !confirm_password)
      return showMessage("Vui lòng nhập đầy đủ thông tin.", false);
    if (password.length < 6)
      return showMessage("Mật khẩu phải có ít nhất 6 ký tự.", false);
    if (password !== confirm_password)
      return showMessage("Mật khẩu xác nhận không khớp.", false);
    if (!role)
      return showMessage("Vui lòng chọn vai trò.", false);

    registerButton.disabled = true;
    registerButton.innerText = "Đang đăng ký...";

    try {
      const response = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ first_name, last_name, email, phone_number, password, role }),
      });

      if (response.ok) {
        showMessage("Đăng ký thành công! Đang chuyển hướng...", true);
        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);
      } else {
        const data = await response.json().catch(() => ({}));
        showMessage(data.detail || "Đăng ký thất bại. Vui lòng thử lại.", false);
      }
    } catch (err) {
      showMessage("Không thể kết nối đến máy chủ.", false);
    } finally {
      registerButton.disabled = false;
      registerButton.innerText = "Đăng ký";
    }
  });

  function showMessage(message, success) {
    messageBox.innerText = message;
    messageBox.style.display = "block";
    messageBox.style.color = success ? "#2ecc71" : "#ff4d4d";
  }
});
