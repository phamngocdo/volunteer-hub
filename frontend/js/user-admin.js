import { checkAuth, authedFetch, initAdminModal, downloadFile } from './admin.js'; // Đổi tên file này nếu cần

// --- 0. Khởi tạo ---
if (!checkAuth()) {
  // Dừng thực thi nếu chưa xác thực
  throw new Error("Chưa xác thực người dùng.");
}

// Khởi tạo modal và lấy hàm điều khiển
const { openModal, closeModal } = initAdminModal();
const API_BASE_URL = "http://localhost:8000/api/admin";

// --- 1. Lấy các phần tử DOM ---
const usersTableContainer = document.getElementById("usersTableContainer");
const exportUsersCSV = document.getElementById("exportUsersCSV");
const exportUsersJSON = document.getElementById("exportUsersJSON");
const userStatusFilter = document.getElementById("userStatusFilter"); // <-- THÊM MỚI

// --- 2. Logic Quản lý Người dùng ---

// Lấy và hiển thị người dùng
async function fetchUsers() {
  // Đọc giá trị từ bộ lọc
  const status = userStatusFilter.value; 
  
  // Tạo URL động (theo đúng kiểu của fetchEvents)
  const url = status 
    ? `${API_BASE_URL}/users?status=${status}` 
    : `${API_BASE_URL}/users`;
    
  try {
    const res = await authedFetch(url); // Sử dụng URL động
    if (!res.ok) throw new Error("Failed to fetch users");
    const users = await res.json();

    // Sắp xếp
    users.sort((a, b) => a.user_id - b.user_id);

    renderUsersTable(users);
  } catch (err) {
    usersTableContainer.innerHTML = `<p class="error">Lỗi tải danh sách người dùng.</p>`;
  }
}

// Tạo bảng HTML cho người dùng
function renderUsersTable(users) {
  if (users.length === 0) {
    usersTableContainer.innerHTML = "<p>Không có người dùng nào.</p>";
    return;
  }
  const table = `
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Tên</th>
          <th>Email</th>
          <th>Vai trò</th>
          <th>Trạng thái</th>
          <th>Hành động</th>
        </tr>
      </thead>
      <tbody>
        ${users.map(user => `
          <tr>
            <td>${user.user_id}</td>
            <td>${user.first_name} ${user.last_name}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td>
              <span class="status-badge status-${user.status}">${user.status}</span>
            </td>
            <td>
              ${user.status === 'active'
      ? `<button class="action-btn btn-ban" data-action="ban" data-id="${user.user_id}">Cấm</button>`
      : `<button class="action-btn btn-activate" data-action="activate" data-id="${user.user_id}">Kích hoạt</button>`
    }
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>`;
  usersTableContainer.innerHTML = table;
}

// Cập nhật trạng thái người dùng (Cấm/Kích hoạt)
async function updateUserStatus(userId, newStatus) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/users/${userId}`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) throw new Error("Cập nhật thất bại");
    closeModal();
    fetchUsers(); // Tải lại danh sách
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

// Xử lý click vào bảng người dùng (Event Delegation)
usersTableContainer.addEventListener("click", (e) => {
  const action = e.target.dataset.action;
  const id = e.target.dataset.id;
  if (!action || !id) return;

  if (action === "ban") {
    openModal(
      "Xác nhận Cấm",
      `Bạn có chắc muốn cấm người dùng ID: ${id}?`,
      () => updateUserStatus(id, "banned"),
      "danger" 
    );
  } else if (action === "activate") {
    openModal(
      "Xác nhận Kích hoạt",
      `Bạn có chắc muốn kích hoạt người dùng ID: ${id}?`,
      () => updateUserStatus(id, "active")
    );
  }
});

// --- 3. Lắng nghe sự kiện ---

// Lắng nghe bộ lọc
userStatusFilter.addEventListener("change", fetchUsers); // <-- THÊM MỚI

// Logic Export
exportUsersCSV.addEventListener("click", () => {
  downloadFile(`${API_BASE_URL}/export/users?format=csv`, "users_export.csv");
});
exportUsersJSON.addEventListener("click", () => {
  downloadFile(`${API_BASE_URL}/export/users?format=json`, "users_export.json");
});

// --- 4. Tải dữ liệu ban đầu ---
fetchUsers();