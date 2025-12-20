/**
 * @file: event-admin.js
 * @description: Quản lý trang Admin Sự kiện (duyệt, từ chối, xóa sự kiện).
 */

import { authedFetch, initAdminModal, downloadFile } from '/js/admin.js';
import { getTokenPayload } from "/js/main.js";

const { openModal, closeModal } = initAdminModal();
const API_BASE_URL = "http://localhost:8000/api/admin";

const eventsTableContainer = document.getElementById("eventsTableContainer");
const eventStatusFilter = document.getElementById("eventStatusFilter");
const exportEventsCSV = document.getElementById("exportEventsCSV");
const exportEventsJSON = document.getElementById("exportEventsJSON");


/**
 * Tải danh sách tất cả sự kiện (Admin Only)
 */
async function fetchEvents() {
  const url = `${API_BASE_URL}/events`;

  try {
    const res = await authedFetch(url);
    if (!res.ok) throw new Error("Failed to fetch events");

    let events = await res.json();

    const filterValue = eventStatusFilter.value.trim();
    if (filterValue) {
      events = events.filter(ev => ev.status === filterValue);
    }

    renderEventsTable(events);
  } catch (err) {
    eventsTableContainer.innerHTML = `<p class="error">Lỗi tải danh sách sự kiện.</p>`;
  }
}

// Tạo bảng HTML cho sự kiện

/**
 * Render bảng danh sách sự kiện Admin
 * @param {Array} events - Danh sách sự kiện
 */
function renderEventsTable(events) {
  let table = "";

  if (events.length === 0) {
    // Không render thead
    table = `
      <table>
        <tbody>
          <tr>
            <td colspan="4" class="no-data">Không có sự kiện nào</td>
          </tr>
        </tbody>
      </table>
    `;
  } else {
    // Có dữ liệu → render đầy đủ bảng
    const rows = events.map(event => `
      <tr>
        <td>${event.event_id}</td>
        <td>${event.title}</td>
        <td>
          <span class="status-badge status-${event.status}">
            ${event.status}
          </span>
        </td>
        <td>
          ${event.status === 'pending' ? `
            <button class="action-btn btn-approve" data-action="approve" data-id="${event.event_id}">Duyệt</button>
            <button class="action-btn btn-reject" data-action="reject" data-id="${event.event_id}">Từ chối</button>
          ` : ''}
          <button class="action-btn btn-delete" data-action="delete" data-id="${event.event_id}">Xóa</button>
        </td>
      </tr>
    `).join("");

    table = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Tiêu đề</th>
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

  eventsTableContainer.innerHTML = table;
}


/**
 * Cập nhật trạng thái sự kiện (Duyệt/Từ chối)
 * @param {number} eventId - ID sự kiện
 * @param {string} newStatus - Trạng thái mới
 */
async function updateEventStatus(eventId, newStatus) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/events/${eventId}`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) throw new Error("Cập nhật thất bại");
    closeModal();
    fetchEvents();
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

async function deleteEvent(eventId) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/events/${eventId}`, {
      method: "DELETE"
    });
    if (!res.ok) throw new Error("Xóa thất bại");
    closeModal();
    fetchEvents();
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

eventsTableContainer.addEventListener("click", (e) => {
  const action = e.target.dataset.action;
  const id = e.target.dataset.id;
  if (!action || !id) return;

  if (action === "approve") {
    openModal("Xác nhận Duyệt", `Duyệt sự kiện ID: ${id}?`, () => updateEventStatus(id, "approved"));
  } else if (action === "reject") {
    openModal("Xác nhận Từ chối", `Từ chối sự kiện ID: ${id}?`, () => updateEventStatus(id, "rejected"));
  } else if (action === "delete") {
    openModal("Xác nhận Xóa", `Bạn có chắc muốn XÓA vĩnh viễn sự kiện ID: ${id}?`, () => deleteEvent(id), "delete");
  }
});


const payload = getTokenPayload();
if (payload && payload.role === "admin") {
  eventStatusFilter.addEventListener("change", fetchEvents);
  exportEventsCSV.addEventListener("click", () => {
    downloadFile(`${API_BASE_URL}/export/events?format=csv`, "events_export.csv");
  });
  exportEventsJSON.addEventListener("click", () => {
    downloadFile(`${API_BASE_URL}/export/events?format=json`, "events_export.json");
  });

  fetchEvents();

} else {
  window.location.href = "/login";
}