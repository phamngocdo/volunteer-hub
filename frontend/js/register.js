function initRegisterPage() {
  const form = document.querySelector(".login-form");

  if (form) {
    console.log("Register form found. Initializing...");
    initEmailRegister(form);
  } else {
    console.warn("Register form (.login-form) not found on this page.");
  }
}

function initEmailRegister(form) {
  const firstNameInput = form.querySelector("#first_name");
  const lastNameInput = form.querySelector("#last_name");
  const phoneInput = form.querySelector("#phone");
  const emailInput = form.querySelector("#email");
  const passwordInput = form.querySelector("#password");
  const confirmPasswordInput = form.querySelector("#confirm_password");
  const roleSelect = form.querySelector("#role");
  const registerButton = form.querySelector(".btn-login");

  // Tạo message box chung
  const messageBox = document.createElement("div");
  messageBox.className = "message-box";
  Object.assign(messageBox.style, {
    fontSize: "14px",
    marginTop: "10px",
    display: "none",
  });
  form.insertBefore(messageBox, registerButton);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Lấy giá trị input
    const first_name = firstNameInput.value.trim();
    const last_name = lastNameInput.value.trim();
    const phone_number = phoneInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirm_password = confirmPasswordInput.value;
    const role = roleSelect.value;

    // Validate cơ bản
    if (!first_name || !last_name || !phone_number || !email || !password || !confirm_password || !role) {
      showMessage(messageBox, "Vui lòng nhập đầy đủ thông tin.", "red");
      return;
    }

    // Validate số điện thoại
    if (!/^0\d{9}$/.test(phone_number)) {
      showMessage(messageBox, "Số điện thoại không hợp lệ. Ví dụ: 0123456789", "red");
      return;
    }

    // Validate email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showMessage(messageBox, "Email không hợp lệ.", "red");
      return;
    }

    // Kiểm tra password
    if (password !== confirm_password) {
      showMessage(messageBox, "Mật khẩu và xác nhận mật khẩu không khớp.", "red");
      return;
    }

    // Disable button
    registerButton.disabled = true;
    registerButton.innerText = "Đang đăng ký...";

    try {
      const res = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ first_name, last_name, phone_number, email, password, role }),
      });

      const data = await res.json();

      if (res.ok) {
        showMessage(messageBox, data.message || "Đăng ký thành công!", "green");
        // Delay 1.5s trước khi redirect
        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);
      } else {
        showMessage(messageBox, data.detail || "Có lỗi xảy ra. Vui lòng thử lại.", "red");
      }
    } catch (err) {
      console.error(err);
      showMessage(messageBox, "Không thể kết nối đến máy chủ.", "red");
    } finally {
      registerButton.disabled = false;
      registerButton.innerText = "Đăng ký";
    }
  });
}

function showMessage(element, message, color) {
  element.innerText = message;
  element.style.color = color;
  element.style.display = "block";
}

initRegisterPage();
