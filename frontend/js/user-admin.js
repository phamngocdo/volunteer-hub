/**
 * @file: user-admin.js
 * @description: Quản lý trang Admin Người dùng (xem, cấm, kích hoạt user).
 */

import { authedFetch, initAdminModal, downloadFile } from '/js/admin.js';
import { getTokenPayload } from "/js/main.js";

const { openModal, closeModal } = initAdminModal();
const API_BASE_URL = "http://localhost:8000/api/admin";

const usersTableContainer = document.getElementById("usersTableContainer");
const userStatusFilter = document.getElementById("userStatusFilter");
const exportUsersCSV = document.getElementById("exportUsersCSV");
const exportUsersJSON = document.getElementById("exportUsersJSON");


/**
 * Tải danh sách người dùng từ API
 */
async function fetchUsers() {
  const url = `${API_BASE_URL}/users`;

  try {
    const res = await authedFetch(url);
    if (!res.ok) throw new Error("Failed to fetch users");

    let users = await res.json();

    users.sort((a, b) => a.user_id - b.user_id);

    const filterValue = userStatusFilter.value.trim();
    if (filterValue) {
      users = users.filter(u => u.status === filterValue);
    }

    renderUsersTable(users);
  } catch (err) {
    usersTableContainer.innerHTML = `<p class="error">Lỗi tải danh sách người dùng.</p>`;
  }
}


/**
 * Render bảng danh sách người dùng
 * @param {Array} users - Danh sách user
 */
function renderUsersTable(users) {
  let table = "";

  if (users.length === 0) {
    table = `
      <table>
        <tbody>
          <tr>
            <td colspan="6" class="no-data">Không có người dùng nào</td>
          </tr>
        </tbody>
      </table>
    `;
  } else {
    const rows = users.map(user => `
      <tr>
        <td>${user.user_id}</td>
        <td>${user.first_name} ${user.last_name}</td>
        <td>${user.email}</td>
        <td>${user.role}</td>
        <td>
          <span class="status-badge status-${user.status}">
            ${user.status}
          </span>
        </td>
        <td>
          ${user.status === 'active'
        ? `<button class="action-btn btn-ban" data-action="ban" data-id="${user.user_id}">Cấm</button>`
        : `<button class="action-btn btn-activate" data-action="activate" data-id="${user.user_id}">Kích hoạt</button>`
      }
        </td>
      </tr>
    `).join("");

    table = `
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
          ${rows}
        </tbody>
      </table>
    `;
  }

  usersTableContainer.innerHTML = table;
}


/**
 * Cập nhật trạng thái người dùng (Cấm/Kích hoạt)
 * @param {number} userId - ID User
 * @param {string} newStatus - Trạng thái mới
 */
async function updateUserStatus(userId, newStatus) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/users/${userId}`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) throw new Error("Cập nhật thất bại");
    closeModal();
    fetchUsers();
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

usersTableContainer.addEventListener("click", (e) => {
  const action = e.target.dataset.action;
  const id = e.target.dataset.id;
  if (!action || !id) return;

  if (action === "ban") {
    openModal("Xác nhận Cấm", `Bạn có chắc muốn cấm người dùng ID: ${id}?`, () => updateUserStatus(id, "banned"), "danger");
  } else if (action === "activate") {
    openModal("Xác nhận Kích hoạt", `Bạn có chắc muốn kích hoạt người dùng ID: ${id}?`, () => updateUserStatus(id, "active"));
  }
});


const payload = getTokenPayload();
if (payload && payload.role === "admin") {
  userStatusFilter.addEventListener("change", fetchUsers);

  exportUsersCSV.addEventListener("click", () => {
    downloadFile(`${API_BASE_URL}/export/users?format=csv`, "users_export.csv");
  });
  exportUsersJSON.addEventListener("click", () => {
    downloadFile(`${API_BASE_URL}/export/users?format=json`, "users_export.json");
  });

  fetchUsers();

} else {
  window.location.href = "/login";
}