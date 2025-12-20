/**
 * @file: history.js
 * @description: Quản lý trang lịch sử tham gia sự kiện của Volunteer.
 */

import { getTokenPayload } from "/js/main.js";

const API_BASE = "http://localhost:8000/api";
const token = localStorage.getItem("access_token");
const token_type = localStorage.getItem("token_type");

const tableContainer = document.getElementById("historyTable");
const statusFilter = document.getElementById("statusFilter");
const modal = document.getElementById("cancelModal");
const modalClose = modal.querySelector(".modal-close");
const modalCancelBtn = document.getElementById("modalCancelBtn");
const modalConfirmBtn = document.getElementById("modalConfirmBtn");
let selectedEventId = null;


/**
 * Lấy danh sách lịch sử tham gia từ API
 */
async function fetchHistory() {
  try {
    const res = await fetch(`${API_BASE}/users/me/history`, {
      headers: { Authorization: `${token_type} ${token}` },
    });
    if (!res.ok) throw new Error("Không thể tải lịch sử tham gia.");
    const data = await res.json();
    renderTable(data);
  } catch (err) {
    tableContainer.innerHTML = `<p style="color:red">${err.message}</p>`;
  }
}


/**
 * Render bảng lịch sử ra HTML
 * @param {Array} data - Danh sách lịch sử
 */
function renderTable(data) {
  const sorted = [...data].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  const filterValue = statusFilter.value;
  const filtered = filterValue ? sorted.filter(h => h.status === filterValue) : sorted;

  if (filtered.length === 0) {
    tableContainer.innerHTML = `<p class="empty-message">Không có sự kiện nào.</p>`;
    return;
  }

  const rows = filtered
    .map(item => {
      const ev = item.event;
      if (item.status !== "approved" && item.status !== "completed") { return "" };
      const statusMap = { approved: "Đã tham gia", completed: "Đã hoàn thành" };
      const statusText = statusMap[item.status];
      const statusClass = `status ${item.status}`;
      const cancelBtn =
        item.status === "approved"
          ? `<button class="action-btn cancel" data-event-id="${ev.event_id}">
              <i class="fa-solid fa-xmark"></i> Hủy tham gia
            </button>`
          : "";
      return `
        <tr>
          <td>${ev.title}</td>
          <td>${ev.location}</td>
          <td>${formatDate(ev.start_date)} - ${formatDate(ev.end_date)}</td>
          <td class="${statusClass}">${statusText}</td>
          <td>${cancelBtn}</td>
        </tr>
      `;
    })
    .join("");

  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Tên sự kiện</th>
          <th>Địa điểm</th>
          <th>Thời gian</th>
          <th>Trạng thái</th>
          <th>Hành động</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;

  attachCancelHandlers();
}


/**
 * Gắn sự kiện click cho các nút hủy
 */
function attachCancelHandlers() {
  document.querySelectorAll(".action-btn.cancel").forEach(btn => {
    btn.addEventListener("click", () => {
      selectedEventId = btn.getAttribute("data-event-id");
      openModal();
    });
  });
}

function openModal() {
  modal.classList.remove("hidden");
}

function closeModal() {
  modal.classList.add("hidden");
  selectedEventId = null;
}


/**
 * Gửi request hủy tham gia sự kiện đã chọn
 */
async function confirmCancel() {
  if (!selectedEventId) return;
  try {
    const res = await fetch(`${API_BASE}/events/${selectedEventId}/registration`, {
      method: "DELETE",
      headers: { Authorization: `${token_type} ${token}` },
    });
    if (!res.ok) {
      const txt = await res.text().catch(() => "");
      throw new Error(txt || "Không thể hủy sự kiện");
    }
    closeModal();
    await fetchHistory();
  } catch (err) {
    closeModal();
    alert(err.message);
  }
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;

  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

const payload = getTokenPayload();
if (payload && payload.role === "volunteer") {
  modalClose.addEventListener("click", closeModal);
  modalCancelBtn.addEventListener("click", closeModal);
  modalConfirmBtn.addEventListener("click", confirmCancel);
  statusFilter.addEventListener("change", fetchHistory);

  fetchHistory();
} else {
  window.location.href = "/login";
}
