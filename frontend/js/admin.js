// --- 1. Cấu hình và Xác thực ---
const API_BASE_URL = "http://localhost:8000/api/admin";
const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type") || "Bearer";

/**
 * Kiểm tra xem người dùng đã đăng nhập chưa.
 * Nếu chưa, chuyển hướng về trang login.
 */
export function checkAuth() {
  if (!token) {
    window.location.href = "/login";
    return false;
  }
  return true;
}

/**
 * Hàm fetch đã được thêm header xác thực.
 * Tự động xử lý lỗi 401/403.
 * @param {string} url - URL để fetch
 * @param {object} options - Tùy chọn của hàm fetch (method, body,...)
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
    throw err; // Ném lỗi ra để hàm gọi có thể xử lý
  }
}

// --- 2. Logic Modal (Cửa sổ xác nhận) ---
let currentModalCallback = null;
let modal, modalTitle, modalMessage, modalConfirmBtn, modalCancelBtn, modalCloseBtn;

/**
 * Khởi tạo và gắn listener cho modal.
 * Trả về các hàm để điều khiển modal.
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

// --- 3. Logic Export (Tiện ích tải file) ---
/**
 * Tải file từ API về máy người dùng.
 * @param {string} url - URL của API export
 * @param {string} filename - Tên file mong muốn (e.g., "users.csv")
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

// Hàm này sẽ được gọi bên trong các tệp JS cụ thể
// export { API_BASE_URL, checkAuth, authedFetch, initAdminModal, downloadFile };