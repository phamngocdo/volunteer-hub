/**
 * @file: admin.js
 * @description: Các tiện ích dùng chung cho trang Admin (Fetch có auth, Modal, Download file).
 */

const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type") || "Bearer";


/**
 * Hàm fetch có tự động gắn header Authorization
 * @param {string} url - API URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>}
 */
export async function authedFetch(url, options = {}) {
  const headers = {
    ...options.headers,
    "Authorization": `${token_type} ${token}`,
  };
  if (options.body) {
    headers["Content-Type"] = "application/json";
  }

  try {
    const res = await fetch(url, { ...options, headers });
    if (res.status === 401 || res.status === 403) {
      localStorage.clear();
      window.location.href = "/login";
    }
    return res;
  } catch (err) {
    console.error("Fetch error:", err);
    alert("Không thể kết nối đến máy chủ.");
    throw err;
  }
}

let currentModalCallback = null;
let modal, modalTitle, modalMessage, modalConfirmBtn, modalCancelBtn, modalCloseBtn;


/**
 * Khởi tạo và quản lý Modal Admin
 * @returns {Object} - { openModal, closeModal }
 */
export function initAdminModal() {
  modal = document.getElementById("adminModal");
  modalTitle = document.getElementById("modalTitle");
  modalMessage = document.getElementById("modalMessage");
  modalConfirmBtn = document.getElementById("modalConfirmBtn");
  modalCancelBtn = document.getElementById("modalCancelBtn");
  modalCloseBtn = document.querySelector(".modal-close");

  const closeModal = () => {
    modal.classList.add("hidden");
    currentModalCallback = null;
  };

  modalConfirmBtn.addEventListener("click", () => {
    if (currentModalCallback) {
      currentModalCallback();
    }
  });
  modalCancelBtn.addEventListener("click", closeModal);
  modalCloseBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  const openModal = (title, message, onConfirmCallback, type = "normal") => {
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    currentModalCallback = onConfirmCallback;

    modalConfirmBtn.className = "modal-btn confirm";
    if (type === "delete") {
      modalConfirmBtn.classList.add("danger");
    }

    modal.classList.remove("hidden");
  };

  return { openModal, closeModal };
}


/**
 * Tải xuống file từ URL (Blob)
 * @param {string} url - URL file cần tải
 * @param {string} filename - Tên file lưu về
 */
export async function downloadFile(url, filename) {
  try {
    const res = await authedFetch(url);
    if (!res.ok) throw new Error("Xuất file thất bại");

    const blob = await res.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}