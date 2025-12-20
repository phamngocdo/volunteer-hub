/**
 * @file: event-user.js
 * @description: Quản lý logic cho trang chi tiết sự kiện của người dùng (quản lý danh sách đăng ký).
 */

const statusMap = {
  pending: "Chờ duyệt",
  approved: "Đã duyệt",
  rejected: "Đã từ chối",
  cancelled: "Đã hủy",
  completed: "Hoàn thành",
};

/**
 * Khởi tạo trang quản lý sự kiện cho User (Manager/Volunteer Leader)
 */
export async function initEventUserPage() {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type") || "Bearer";

  const path = window.location.pathname;
  const match = path.match(/\/event-user\/(\d+)$/);

  const eventId = match[1];

  await waitForElements(["#event-admin-title", "#registration-list-body"]);

  const titleEl = document.getElementById("event-admin-title");
  const tableBody = document.getElementById("registration-list-body");

  await loadAllData(eventId, token, token_type, titleEl, tableBody);
}

async function waitForElements(selectors, timeout = 2000) {
  return new Promise((resolve, reject) => {
    const interval = 50;
    let waited = 0;
    const timer = setInterval(() => {
      const allFound = selectors.every((sel) => document.querySelector(sel));
      if (allFound) {
        clearInterval(timer);
        resolve();
      } else if ((waited += interval) >= timeout) {
        clearInterval(timer);
        reject(new Error(`Timeout: ${selectors.join(", ")}`));
      }
    }, interval);
  });
}

/**
 * Tải toàn bộ dữ liệu cần thiết (Thông tin sự kiện + Danh sách đăng ký)
 * @param {string} eventId - ID sự kiện
 */
async function loadAllData(eventId, token, token_type, titleEl, tableBody) {
  try {
    await Promise.all([
      fetchEventDetailsForAdmin(eventId, token, token_type, titleEl),
      fetchRegistrations(eventId, token, token_type, tableBody),
    ]);
  } catch (err) {
    console.error(err);
  }
}

async function fetchEventDetailsForAdmin(eventId, token, token_type, titleEl) {
  try {
    const res = await fetch(`http://localhost:8000/api/events/${eventId}`, {
      headers: {
        Authorization: `${token_type} ${token}`
      },
    });
    if (!res.ok) throw new Error("Error fetching event details");
    const event = await res.json();
    titleEl.textContent = `Quản lý đơn: ${event.title}`;
  } catch (err) {
    titleEl.textContent = "Lỗi tải tên sự kiện";
    throw err;
  }
}

/**
 * Gọi API lấy danh sách người đã đăng ký tham gia sự kiện và render bảng
 */
async function fetchRegistrations(eventId, token, token_type, tableBody) {
  try {
    const res = await fetch(`http://localhost:8000/api/events/${eventId}/registrations`, {
      headers: {
        Authorization: `${token_type} ${token}`
      },
    });
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Error fetching registrations");
    }

    const registrations = await res.json();
    if (registrations.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;">Chưa có ai đăng ký.</td></tr>`;
      return;
    }

    tableBody.innerHTML = "";
    let count = 1;

    registrations.forEach((reg) => {
      const row = document.createElement("tr");
      const fName = reg.user?.first_name || "";
      const lName = reg.user?.last_name || "";
      const userName = (fName + " " + lName).trim() || "N/A";
      const userEmail = reg.user?.email || "N/A";
      const userPhone = reg.user?.phone_number || "N/A";
      const statusText = statusMap[reg.status] || reg.status;

      row.innerHTML = `
        <td>${count++}</td>
        <td>${userName}</td>
        <td>${userEmail}</td>
        <td>${userPhone}</td>
        <td><span class="status status-${reg.status}">${statusText}</span></td>
        <td class="actions-cell" data-reg-id="${reg.registration_id}">
          ${generateActionButtons(reg.status)}
        </td>
      `;

      addEventListenersToAdminButtons(row, reg.registration_id, token, token_type);
      tableBody.appendChild(row);
    });
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="6" class="error">Lỗi: ${err.message}</td></tr>`;
    throw err;
  }
}

/**
 * Tạo các nút hành động (Duyệt/Từ chối) dựa trên trạng thái hiện tại
 * @param {string} status - Trạng thái đăng ký hiện tại
 * @returns {string} - HTML string các nút bấm tương ứng
 */
function generateActionButtons(status) {
  switch (status) {
    case "pending":
      return `
        <button class="btn btn-success btn-sm" data-action="approved"><i class="fa-solid fa-check"></i> Duyệt</button>
        <button class="btn btn-danger btn-sm" data-action="rejected"><i class="fa-solid fa-times"></i> Từ chối</button>
      `;
    case "approved":
      return `
        <button class="btn btn-danger btn-sm" data-action="rejected"><i class="fa-solid fa-ban"></i> Hủy đơn</button>
      `;
    case "rejected":
      return `
        <button class="btn btn-success btn-sm" data-action="approved"><i class="fa-solid fa-check"></i> Duyệt lại</button>
      `;
    default:
      return `<span>${status}</span>`;
  }
}

function addEventListenersToAdminButtons(row, registrationId, token, token_type) {
  row.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async () => {
      const newStatus = button.dataset.action;
      await handleUpdateStatus(registrationId, newStatus, button, token, token_type);
    });
  });
}

/**
 * Xử lý logic cập nhật trạng thái đăng ký khi nhấn nút
 * @param {string} registrationId - ID đăng ký
 * @param {string} newStatus - Trạng thái mới (approved/rejected)
 */
async function handleUpdateStatus(registrationId, newStatus, button, token, token_type) {
  const originalHTML = button.innerHTML;
  button.disabled = true;
  button.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i>`;

  try {
    const res = await fetch(`http://localhost:8000/api/events/registrations/${registrationId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${token_type} ${token}`,
      },
      body: JSON.stringify({
        status: newStatus
      }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Cập nhật thất bại");
    }

    const updated = await res.json();
    const row = button.closest("tr");
    const statusText = statusMap[updated.status] || updated.status;

    const statusCell = row.querySelector("td:nth-child(5)");
    if (statusCell) {
      statusCell.innerHTML = `<span class="status status-${updated.status}">${statusText}</span>`;
    }

    const actionCell = row.querySelector(".actions-cell");
    if (actionCell) {
      actionCell.innerHTML = generateActionButtons(updated.status);
    }

    addEventListenersToAdminButtons(row, registrationId, token, token_type);
  } catch (err) {
    alert(`Lỗi: ${err.message}`);
    console.error(err);
    button.disabled = false;
    button.innerHTML = originalHTML;
  }
}

initEventUserPage();