/**
 * @file: profile.js
 * @description: Quản lý trang thông tin cá nhân, cập nhật profile và đổi mật khẩu.
 */

import { initHeader, getTokenPayload } from "/js/main.js";

const form = document.getElementById("profileForm");
const formError = document.getElementById("form-error");
const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type");

const avatarInput = document.getElementById("avatarInput");
const avatarImage = document.getElementById("avatarImage");
const removeAvatarBtn = document.getElementById("removeAvatar");

const DEFAULT_AVATAR = "assets/default-avatar.png";
let selectedAvatarFilename = null;

if (!getTokenPayload()) {
  window.location.href = "/";
} else {
  loadUser();
}


/**
 * Tải thông tin người dùng từ API và điền vào form
 */
async function loadUser() {
  document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", () => {
      const input = icon.previousElementSibling;
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
      } else {
        input.type = "password";
        icon.classList.replace("fa-eye-slash", "fa-eye");
      }
    });
  });

  try {
    const res = await fetch("http://localhost:8000/api/users/me", {
      headers: { Authorization: `${token_type} ${token}` },
    });

    if (!res.ok) throw new Error("Failed to load user");

    const data = await res.json();

    document.getElementById("first_name").value = data.first_name || "";
    document.getElementById("last_name").value = data.last_name || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("phone_number").value = data.phone_number || "";

    avatarImage.src = data.avatar_url || DEFAULT_AVATAR;

  } catch (err) {
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Không thể tải thông tin người dùng.";
    console.error(err);
  }
}

avatarInput.addEventListener("change", () => {
  const file = avatarInput.files[0];
  if (!file) return;

  selectedAvatarFilename = file;

  const reader = new FileReader();
  reader.onload = e => {
    avatarImage.src = e.target.result;
  };
  reader.readAsDataURL(file);
});

removeAvatarBtn.addEventListener("click", () => {
  avatarImage.src = DEFAULT_AVATAR;
  selectedAvatarFilename = "DELETE_ACTION";
  avatarInput.value = "";
});


/**
 * Validate dữ liệu form trước khi submit
 * @returns {boolean} - True nếu hợp lệ, False nếu có lỗi
 */
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

  const hasPassword = oldPassword || newPassword || confirmPassword;
  if (hasPassword) {
    if (!oldPassword || !newPassword || !confirmPassword) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Khi đổi mật khẩu, phải nhập tất cả các trường.";
      return false;
    }
    if (newPassword.length < 6) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Mật khẩu mới phải có ít nhất 6 ký tự.";
      return false;
    }
    if (newPassword !== confirmPassword) {
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = "Mật khẩu xác nhận không khớp.";
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
    if (selectedAvatarFilename instanceof File) {
      const formData = new FormData();
      formData.append("file", selectedAvatarFilename);
      const avatarRes = await fetch("http://localhost:8000/api/users/avatar", {
        method: "POST",
        headers: {
          Authorization: `${token_type} ${token}`,
        },
        body: formData,
      });

      if (!avatarRes.ok) throw new Error("Failed to upload avatar");

      const avatarData = await avatarRes.json();
      payload.avatar_url = avatarData;
    } else if (selectedAvatarFilename === "DELETE_ACTION") {
      payload.avatar_url = DEFAULT_AVATAR;
    } else {
      delete payload.avatar_url;
    }

    const res = await fetch("http://localhost:8000/api/users/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${token_type} ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      const data = await res.json();
      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("token_type", data.token_type);
      }
      formError.style.display = "block";
      formError.style.color = "green";
      formError.textContent = "Cập nhật thành công!";

      form.old_password.value = "";
      form.new_password.value = "";
      form.confirm_password.value = "";
      selectedAvatarFilename = null;
    } else {
      const errorData = await res.json();
      formError.style.display = "block";
      formError.style.color = "var(--error)";
      formError.textContent = errorData.detail || "Cập nhật thất bại.";
    }

  } catch (err) {
    console.error(err);
    formError.style.display = "block";
    formError.style.color = "var(--error)";
    formError.textContent = "Có lỗi xảy ra, vui lòng thử lại.";
  }
});