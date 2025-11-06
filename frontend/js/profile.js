const form = document.getElementById("profileForm");
const formError = document.getElementById("form-error");
const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type");

document.querySelectorAll(".toggle-password").forEach(icon => {
  icon.addEventListener("click", () => {
    const input = icon.previousElementSibling;
    if (input.type === "password") {
      input.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
    } else {
      input.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
    }
  });
});

async function loadUser() {
  try {
    const res = await fetch("http://localhost:8000/api/users/me", {
      headers: { Authorization: `${token_type} ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch user data");
    const data = await res.json();
    document.getElementById("first_name").value = data.first_name || "";
    document.getElementById("last_name").value = data.last_name || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("phone_number").value = data.phone_number || "";
  } catch (err) {
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Không thể tải thông tin người dùng.";
    console.error(err);
  }
}

function validateForm() {
  formError.style.display = "none";
  const firstName = form.first_name.value.trim();
  const lastName = form.last_name.value.trim();
  const email = form.email.value.trim();
  const phone = form.phone_number.value.trim();
  const oldPassword = form.old_password.value.trim();
  const newPassword = form.new_password.value.trim();
  const confirmPassword = form.confirm_password.value.trim();

  if (!firstName || !lastName || !email || !phone) {
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Họ, Tên, Email, Số điện thoại không được để trống.";
    return false;
  }

  if (!/^0\d{9}$/.test(phone)) {
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Số điện thoại không hợp lệ.";
    return false;
  }


  const anyPasswordFilled = oldPassword || newPassword || confirmPassword;
  if (anyPasswordFilled) {
    if (!oldPassword || !newPassword || !confirmPassword) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Khi thay đổi mật khẩu, tất cả các trường mật khẩu phải được điền.";
      return false;
    }

    if (newPassword.length < 6) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Mật khẩu mới phải có ít nhất 6 ký tự";
      return false;
    }

    if (newPassword !== confirmPassword) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Mật khẩu mới và xác nhận mật khẩu mới không khớp.";
      return false;
    }
  }

  return true;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!validateForm()) return;

  form.classList.add("animate-form");
  setTimeout(() => form.classList.remove("animate-form"), 300);

  const payload = {
    first_name: form.first_name.value.trim(),
    last_name: form.last_name.value.trim(),
    email: form.email.value.trim(),
    phone_number: form.phone_number.value.trim(),
    old_password: form.old_password.value.trim(),
    new_password: form.new_password.value.trim(),
    confirm_password: form.confirm_password.value.trim(),
  };

  try {
    const res = await fetch("http://localhost:8000/api/users/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${token_type} ${token}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = data.detail || "Cập nhật thất bại.";
      return;
    }

    formError.style.display = "block";
    formError.style.color = "green";
    formError.textContent = "Cập nhật thành công!";
    form.old_password.value = "";
    form.new_password.value = "";
    form.confirm_password.value = "";
  } catch (err) {
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Có lỗi xảy ra, vui lòng thử lại.";
    console.error(err);
  }
});

loadUser();
