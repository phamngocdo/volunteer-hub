import { checkAuth, authedFetch, initAdminModal, downloadFile } from './admin.js';

// --- 0. Khởi tạo ---
if (!checkAuth()) {
  // Dừng thực thi nếu chưa xác thực
  throw new Error("Chưa xác thực người dùng.");
}

// Khởi tạo modal và lấy hàm điều khiển
const { openModal, closeModal } = initAdminModal();
const API_BASE_URL = "http://localhost:8000/api/admin"; // (Hoặc import từ common)

// --- 1. Lấy các phần tử DOM ---
const eventsTableContainer = document.getElementById("eventsTableContainer");
const eventStatusFilter = document.getElementById("eventStatusFilter");
const exportEventsCSV = document.getElementById("exportEventsCSV");
const exportEventsJSON = document.getElementById("exportEventsJSON");

// --- 2. Logic Quản lý Sự kiện ---

// Lấy và hiển thị sự kiện
async function fetchEvents() {
  const status = eventStatusFilter.value;
  const url = status 
    ? `${API_BASE_URL}/events?status=${status}` 
    : `${API_BASE_URL}/events`;
    
  try {
    const res = await authedFetch(url);
    if (!res.ok) throw new Error("Failed to fetch events");
    const events = await res.json();
    renderEventsTable(events);
  } catch (err) {
    eventsTableContainer.innerHTML = `<p class="error">Lỗi tải danh sách sự kiện.</p>`;
  }
}

// Tạo bảng HTML cho sự kiện
function renderEventsTable(events) {
  if (events.length === 0) {
    eventsTableContainer.innerHTML = "<p>Không có sự kiện nào.</p>";
    return;
  }
  const table = `
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
        ${events.map(event => `
          <tr>
            <td>${event.event_id}</td>
            <td>${event.title}</td>
            <td>
              <span class="status-badge status-${event.status}">${event.status}</span>
            </td>
            <td>
              ${event.status === 'pending' ? `
                <button class="action-btn btn-approve" data-action="approve" data-id="${event.event_id}">Duyệt</button>
                <button class="action-btn btn-reject" data-action="reject" data-id="${event.event_id}">Từ chối</button>
              ` : ''}
              <button class="action-btn btn-delete" data-action="delete" data-id="${event.event_id}">Xóa</button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>`;
  eventsTableContainer.innerHTML = table;
}
 
// Cập nhật trạng thái sự kiện (Duyệt/Từ chối)
async function updateEventStatus(eventId, newStatus) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/events/${eventId}`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) throw new Error("Cập nhật thất bại");
    closeModal();
    fetchEvents(); // Tải lại danh sách
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

// Xóa sự kiện
async function deleteEvent(eventId) {
  try {
    const res = await authedFetch(`${API_BASE_URL}/events/${eventId}`, {
      method: "DELETE"
    });
    if (!res.ok) throw new Error("Xóa thất bại");
    closeModal();
    fetchEvents(); // Tải lại danh sách
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
}

// Xử lý click vào bảng sự kiện (Event Delegation)
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

// Lắng nghe bộ lọc
eventStatusFilter.addEventListener("change", fetchEvents);

// --- 3. Logic Export ---
exportEventsCSV.addEventListener("click", () => {
  downloadFile(`${API_BASE_URL}/export/events?format=csv`, "events_export.csv");
});
exportEventsJSON.addEventListener("click", () => {
  downloadFile(`${API_BASE_URL}/export/events?format=json`, "events_export.json");
});

// --- 4. Tải dữ liệu ban đầu ---
fetchEvents();