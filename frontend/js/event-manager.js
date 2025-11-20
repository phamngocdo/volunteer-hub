import { navigateTo } from "./main.js";

// Lấy token và token_type từ localStorage một lần
const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type") || "Bearer";
console.log("🕵️‍♂️ DEBUG: Token đã được tải.");

// === DOM Elements Chung ===
let mainContainer;
let deleteModal;
let closeDeleteBtn;
let cancelDeleteBtn;
let confirmDeleteBtn;
let eventIdToDelete = null;

// Modal Tạo/Sửa
let createModal;
let createForm;
let closeCreateBtn;
let cancelCreateBtn;
let formError;
let formTitle;
let saveEventBtn;
let eventIdToEdit = null;

// DOM Elements MỚI cho Upload
let imageFileInput;
let filePickerBtn;
let imagePreview;
let uploadStatus;
let hiddenImageUrlInput;

// ===========================================
// VIEW 1: DANH SÁCH SỰ KIỆN (Event List View)
// ===========================================

/**
 * Render HTML cho view danh sách sự kiện
 */
function renderEventListView() {
  console.log("Đang render: View Danh sách sự kiện");
  mainContainer.innerHTML = `
    <div class="page-header">
      <h1>Sự kiện của tôi</h1>
      <button id="openCreateEventBtn" class="btn btn-primary">
        <i class="fa-solid fa-plus"></i> Tạo sự kiện mới
      </button>
    </div>
    <div id="my-events-list">
      <p>Đang tải sự kiện của bạn...</p>
    </div>
  `;

  document
    .getElementById("openCreateEventBtn")
    .addEventListener("click", openCreateModal);
  fetchMyEvents();
}

/**
 * Tải và hiển thị danh sách sự kiện
 */
async function fetchMyEvents() {
  const container = document.getElementById("my-events-list");
  if (!container) return;

  container.innerHTML = "<p>Đang tải sự kiện của bạn...</p>";

  try {
    const res = await fetch(
      "http://localhost:8000/api/events/manager/my-events",
      {
        headers: { Authorization: `${token_type} ${token}` },
      }
    );
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Không thể tải sự kiện của bạn");
    }
    const myEvents = await res.json();
    renderEvents(myEvents);
  } catch (err) {
    container.innerHTML = `<p class="error">Lỗi: ${err.message}</p>`;
  }
}

/**
 * Render từng event item
 */
function renderEvents(events) {
  const container = document.getElementById("my-events-list");
  if (!container) return;

  container.innerHTML = "";
  if (events.length === 0) {
    container.innerHTML = "<p>Bạn chưa tạo sự kiện nào.</p>";
    return;
  }

  events.forEach((ev) => {
    const eventElement = document.createElement("div");
    eventElement.className = "manager-event-item";
    eventElement.innerHTML = `
      <div class="event-info">
        <h4>${ev.title}</h4>
        <p><i class="fa-solid fa-calendar-days"></i> ${formatDate(ev.start_date)}</p>
        <p><i class="fa-solid fa-users"></i> ${ev.volunteer_number} người đăng ký</p>
        <p><span class="status status-${ev.status}">${ev.status}</span></p>
      </div>
      <div class="event-actions">
        <a href="/event-user/${ev.event_id}" class="btn btn-secondary btn-admin-link">
          <i class="fa-solid fa-users"></i> Quản lý đơn
        </a>
        <button class="btn btn-secondary btn-edit" data-id="${ev.event_id}">
          <i class="fa-solid fa-pen"></i> Sửa
        </button>
        <button class="btn btn-danger btn-delete" data-id="${ev.event_id}" data-title="${ev.title}">
          <i class="fa-solid fa-trash"></i> Xóa
        </button>
      </div>
    `;

    // Gán listener cho các nút vừa tạo
    eventElement
      .querySelector(".btn-edit")
      .addEventListener("click", (e) =>
        openEditModal(e.currentTarget.dataset.id)
      );
    eventElement
      .querySelector(".btn-delete")
      .addEventListener("click", (e) =>
        openDeleteModal(
          e.currentTarget.dataset.id,
          e.currentTarget.dataset.title
        )
      );

    container.appendChild(eventElement);
  });
}

// ===========================================
// LOGIC MODAL (Chung)
// ===========================================

// --- Logic Modal Xóa ---
function openDeleteModal(id, title) {
  eventIdToDelete = id;
  document.getElementById("deleteConfirmMessage").textContent =
    `Bạn có chắc muốn xóa sự kiện "${title}"? Hành động này không thể hoàn tác.`;
  deleteModal.style.display = "";
  deleteModal.classList.remove("hidden");
}

function closeDeleteModal() {
  deleteModal.style.display = "none";
  deleteModal.classList.add("hidden");
  eventIdToDelete = null;
}

async function confirmDelete() {
  if (!eventIdToDelete) return;
  try {
    const res = await fetch(
      `http://localhost:8000/api/events/${eventIdToDelete}`,
      {
        method: "DELETE",
        headers: { Authorization: `${token_type} ${token}` },
      }
    );
    if (!res.ok && res.status !== 204) {
      const err = await res.json();
      throw new Error(err.detail || "Xóa thất bại");
    }
    closeDeleteModal();

    // Nếu đang ở trang quản lý đơn thì chuyển về event-manager
    if (window.location.pathname.startsWith("/event-user")) {
      navigateTo("event-manager");
    } else {
      fetchMyEvents();
    }
  } catch (err) {
    alert(`Lỗi: ${err.message}`);
  }
}

// --- Logic Modal Tạo/Sửa ---
function openCreateModal() {
  eventIdToEdit = null;
  createForm.reset();
  formError.textContent = "";
  formError.style.display = "none";
  formTitle.textContent = "Tạo sự kiện mới";
  saveEventBtn.textContent = "Tạo sự kiện";
  saveEventBtn.disabled = false;
  createModal.style.display = "";
  createModal.classList.remove("hidden");

  // Reset form upload
  imageFileInput.value = null;
  imagePreview.innerHTML = "<p>Chưa chọn ảnh nào.</p>";
  uploadStatus.textContent = "";
  hiddenImageUrlInput.value = "";
}

async function openEditModal(id) {
  eventIdToEdit = id;
  createForm.reset();
  formError.textContent = "";
  formError.style.display = "none";
  formTitle.textContent = "Đang tải dữ liệu sự kiện...";
  saveEventBtn.textContent = "Cập nhật";
  saveEventBtn.disabled = true;
  createModal.style.display = "";
  createModal.classList.remove("hidden");

  try {
    const res = await fetch(`http://localhost:8000/api/events/${id}`, {
      headers: { Authorization: `${token_type} ${token}` },
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Không thể tải chi tiết sự kiện");
    }
    const eventData = await res.json();

    // Điền dữ liệu text
    document.getElementById("title").value = eventData.title;
    document.getElementById("description").value = eventData.description || "";
    document.getElementById("location").value = eventData.location || "";
    document.getElementById("start_date").value = eventData.start_date;
    document.getElementById("end_date").value = eventData.end_date;
    document.getElementById("category").value = eventData.category;

    // Hiển thị ảnh bìa cũ
    imageFileInput.value = null;
    uploadStatus.textContent = "";
    if (eventData.image_url) {
      const imageUrl = eventData.image_url.startsWith("http")
        ? eventData.image_url
        : `http://localhost:8000${eventData.image_url}`;
      imagePreview.innerHTML = `<img src="${imageUrl}" alt="Ảnh bìa hiện tại" style="max-width: 100%; height: auto;">`;
      hiddenImageUrlInput.value = eventData.image_url;
    } else {
      imagePreview.innerHTML = "<p>Chưa chọn ảnh nào.</p>";
      hiddenImageUrlInput.value = "";
    }

    formTitle.textContent = "Cập nhật sự kiện";
    saveEventBtn.disabled = false;
  } catch (err) {
    console.error("Lỗi khi tải sự kiện để sửa:", err);
    formError.textContent = `Lỗi: ${err.message}`;
    formError.style.display = "block";
  }
}

function closeCreateModal() {
  createModal.style.display = "none";
  createModal.classList.add("hidden");
  eventIdToEdit = null;
}

async function handleFormSubmit(e) {
  e.preventDefault();
  formError.textContent = "";
  formError.style.display = "none";

  const formData = new FormData(createForm);
  const isEditMode = eventIdToEdit !== null;

  const eventData = {
    title: formData.get("title")?.trim(),
    description: formData.get("description")?.trim(),
    location: formData.get("location")?.trim(),
    start_date: formData.get("start_date"),
    end_date: formData.get("end_date"),
    category: formData.get("category"),
    image_url: formData.get("image_url") || null,
  };

  // Validation
  if (
    !eventData.title ||
    !eventData.description ||
    !eventData.location ||
    !eventData.start_date ||
    !eventData.end_date ||
    !eventData.category ||
    !eventData.image_url
  ) {
    formError.textContent = "Vui lòng nhập đầy đủ tất cả các trường.";
    formError.style.display = "block";
    return;
  }

  const startDate = new Date(eventData.start_date);
  const endDate = new Date(eventData.end_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (!isEditMode && startDate < today) {
    formError.textContent = "Ngày bắt đầu không được là một ngày trong quá khứ.";
    formError.style.display = "block";
    return;
  }
  if (endDate < startDate) {
    formError.textContent = "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu.";
    formError.style.display = "block";
    return;
  }

  const url = isEditMode
    ? `http://localhost:8000/api/events/${eventIdToEdit}`
    : "http://localhost:8000/api/events/";
  const method = isEditMode ? "PUT" : "POST";

  try {
    const res = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `${token_type} ${token}`,
      },
      body: JSON.stringify(eventData),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Thao tác thất bại");
    }
    closeCreateModal();
    if (window.location.pathname === "/event-manager") {
      fetchMyEvents();
    }
  } catch (err) {
    formError.textContent = err.message;
    formError.style.display = "block";
  }
}

// ===========================================
// === CÁC HÀM UPLOAD MỚI ĐƯỢC THÊM VÀO ĐÂY ===
// ===========================================

/**
 * Được gọi khi người dùng chọn 1 file
 */
async function handleFileSelected(e) {
  const file = e.target.files[0];
  if (!file) return;

  // 1. Hiển thị preview ngay lập tức
  const reader = new FileReader();
  reader.onload = (event) => {
    imagePreview.innerHTML = `<img src="${event.target.result}" alt="Xem trước" style="max-width: 100%; height: auto;">`;
  };
  reader.readAsDataURL(file);

  // 2. Vô hiệu hóa nút "Lưu" và bắt đầu upload
  saveEventBtn.disabled = true;
  uploadStatus.textContent = "Đang chuẩn bị tải lên...";

  try {
    // 3. Gọi hàm upload
    const finalUrl = await uploadFileToBackend(file);

    // 4. Upload thành công
    uploadStatus.textContent = "Tải ảnh thành công!";
    hiddenImageUrlInput.value = finalUrl;
    saveEventBtn.disabled = false;
  } catch (err) {
    console.error("Upload thất bại:", err);
    uploadStatus.textContent = `Lỗi: ${err.message}`;
  }
}

/**
 * Xử lý logic upload file lên LOCAL BACKEND
 */
async function uploadFileToBackend(file) {
  const formData = new FormData();
  formData.append("file", file, file.name);

  uploadStatus.textContent = "Đang tải ảnh lên (0%)...";

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/api/events/upload_image", true);
    xhr.setRequestHeader("Authorization", `${token_type} ${token}`);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100);
        uploadStatus.textContent = `Đang tải ảnh lên (${percentComplete}%)...`;
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText);
          if (response.final_url) {
            resolve(response.final_url);
          } else {
            reject(new Error("Server không trả về 'final_url'."));
          }
        } catch (e) {
          reject(new Error("Không thể phân tích phản hồi từ server."));
        }
      } else {
        try {
          const err = JSON.parse(xhr.responseText);
          reject(new Error(err.detail || `Lỗi server: ${xhr.status}`));
        } catch {
          reject(new Error(`Lỗi server: ${xhr.status}`));
        }
      }
    };

    xhr.onerror = () => {
      reject(new Error("Lỗi mạng khi đang upload file."));
    };

    xhr.send(formData);
  });
}

// === Hàm tiện ích ===
function formatDate(dateStr) {
  if (!dateStr) return "Chưa có ngày";
  const [year, month, day] = dateStr.split("-");
  return `${day}/${month}/${year}`;
}

// === Khởi tạo trang ===
function initEventManagerPage() {

  // ✅ BƯỚC 1: GÁN GIÁ TRỊ (QUERY DOM) KHI HÀM CHẠY
  // Lỗi "TypeError" và "ReferenceError" của bạn sẽ được sửa ở đây
  mainContainer = document.querySelector(".manager-container");

  // Modal Xóa
  deleteModal = document.getElementById("deleteConfirmModal");
  if (!deleteModal) {
    console.error("❌ Error: deleteConfirmModal not found in DOM");
    console.log("Current DOM body:", document.body.innerHTML);
    throw new Error("Không tìm thấy modal xóa (deleteConfirmModal)");
  }
  closeDeleteBtn = deleteModal.querySelector(".modal-close");
  cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
  confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

  // Modal Tạo/Sửa
  createModal = document.getElementById("createEventModal");
  if (!createModal) {
    console.error("❌ Error: createEventModal not found in DOM");
    throw new Error("Không tìm thấy modal tạo (createEventModal)");
  }
  createForm = document.getElementById("create-event-form");
  closeCreateBtn = createModal.querySelector(".modal-close");
  cancelCreateBtn = document.getElementById("cancelCreateBtn");
  formError = document.getElementById("form-error");
  formTitle = document.getElementById("form-title");
  saveEventBtn = document.getElementById("saveEventBtn");

  // DOM Elements Upload
  imageFileInput = document.getElementById("image_file_input");
  filePickerBtn = document.getElementById("open-file-picker-btn");
  imagePreview = document.getElementById("image-preview");
  uploadStatus = document.getElementById("upload-status");
  hiddenImageUrlInput = document.getElementById("image_url");

  // Gán listener cho các modal (chỉ 1 lần)
  closeDeleteBtn.addEventListener("click", closeDeleteModal);
  cancelDeleteBtn.addEventListener("click", closeDeleteModal);
  deleteModal.addEventListener("click", (e) => {
    if (e.target === deleteModal) closeDeleteModal();
  });
  confirmDeleteBtn.addEventListener("click", confirmDelete);

  closeCreateBtn.addEventListener("click", closeCreateModal);
  cancelCreateBtn.addEventListener("click", closeCreateModal);
  createModal.addEventListener("click", (e) => {
    if (e.target === createModal) closeCreateModal();
  });
  createForm.addEventListener("submit", handleFormSubmit);

  // Gán listener cho UPLOAD
  filePickerBtn.addEventListener("click", () => {
    imageFileInput.click();
  });
  imageFileInput.addEventListener("change", handleFileSelected);

  // Render view danh sách sự kiện
  renderEventListView();
}

// Chạy hàm khởi tạo khi file được import
try {
  console.log("🚀 [EventManager] Script initializing...");
  initEventManagerPage();
  console.log("✅ [EventManager] Initialization complete.");
} catch (err) {
  console.error("❌ [EventManager] Initialization failed:", err);
  alert(`Lỗi khởi tạo trang quản lý: ${err.message}`);
}
