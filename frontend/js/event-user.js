// js/event-user.js


// ==== EXPORT HÀM CHÍNH ====
export async function initEventUserPage() {
  console.log("Module event-user.js đã được import.");

  // 1. Lấy token
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type") || "Bearer";

  // 2. Lấy eventId từ URL
  const path = window.location.pathname;
  const match = path.match(/\/event-user\/(\d+)$/);
  if (!match) {
    console.error("Không thể lấy ID sự kiện từ URL:", path);
    return;
  }
  const eventId = match[1];
  console.log(`✅ Lấy được Event ID: ${eventId}`);

  // 3. Đợi các element chính xuất hiện
  // (Không cần đợi nút "user-view-back-btn" vì script này không còn xử lý nó)
  await waitForElements(["#event-admin-title", "#registration-list-body"]);

  // 4. Lấy các phần tử DOM
  const titleEl = document.getElementById("event-admin-title");
  const tableBody = document.getElementById("registration-list-body");
  
  // 5. Gán sự kiện (Không còn cần gán sự kiện cho nút "Quay lại")

  // 6. Gọi tải dữ liệu
  await loadAllData(eventId, token, token_type, titleEl, tableBody);
}

// ==== HÀM PHỤ TRỢ ====

// Chờ các element xuất hiện
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
        reject(new Error(`Không tìm thấy các element sau ${timeout / 1000}s: ${selectors.join(", ")}`));
      }
    }, interval);
  });
}

// (Hàm handleUserNavClick đã được XÓA để router chính (main.js) xử lý)

// Tải song song dữ liệu
async function loadAllData(eventId, token, token_type, titleEl, tableBody) {
  try {
    await Promise.all([
      fetchEventDetailsForAdmin(eventId, token, token_type, titleEl),
      fetchRegistrations(eventId, token, token_type, tableBody),
    ]);
  } catch (err) {
    console.error("Lỗi khi tải dữ liệu:", err);
  }
}

// Lấy chi tiết sự kiện
async function fetchEventDetailsForAdmin(eventId, token, token_type, titleEl) {
  try {
    const res = await fetch(`http://localhost:8000/api/events/${eventId}`, {
      headers: { Authorization: `${token_type} ${token}` },
    });
    if (!res.ok) throw new Error("Không thể tải chi tiết sự kiện");
    const event = await res.json();
    titleEl.textContent = `Quản lý đơn: ${event.title}`;
  } catch (err) {
    titleEl.textContent = "Lỗi tải tên sự kiện";
    throw err;
  }
}

// Lấy danh sách đăng ký
async function fetchRegistrations(eventId, token, token_type, tableBody) {
  try {
    const res = await fetch(`http://localhost:8000/api/events/${eventId}/registrations`, {
      headers: { Authorization: `${token_type} ${token}` },
    });
    console.log("fetchRegistrations response:", res);
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Không thể tải danh sách đăng ký");
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

      row.innerHTML = `
        <td>${count++}</td>
        <td>${userName}</td>
        <td>${userEmail}</td>
        <td>${userPhone}</td>
        <td><span class="status status-${reg.status}">${reg.status}</span></td>
        <td class="actions-cell" data-reg-id="${reg.registration_id}">
          ${generateActionButtons(reg.status)}
        </td>
      `;

      addEventListenersToAdminButtons(row, reg.registration_id, token, token_type);
      tableBody.appendChild(row);
    });
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="5" class="error">Lỗi: ${err.message}</td></tr>`;
    throw err;
  }
}

// Tạo các nút hành động
function generateActionButtons(status) {
  switch (status) {
    case "pending":
      return `
        <button class="btn btn-success btn-sm" data-action="approved"><i class="fa-solid fa-check"></i> Duyệt</button>
        <button class="btn btn-danger btn-sm" data-action="rejected"><i class="fa-solid fa-times"></i> Từ chối</button>
      `;
    case "approved":
      return `
        <button class="btn btn-primary btn-sm" data-action="completed"><i class="fa-solid fa-clipboard-check"></i> Hoàn thành</button>
        <button class="btn btn-danger btn-sm" data-action="rejected"><i class="fa-solid fa-times"></i> Hủy</button>
      `;
    case "completed":
      return `<span><i class="fa-solid fa-check-circle"></i> Đã hoàn thành</span>`;
    case "rejected":
      return `<span><i class="fa-solid fa-ban"></i> Đã từ chối</span>`;
    default:
      return `<span>N/A</span>`;
  }
}

// Gán sự kiện nút hành động
function addEventListenersToAdminButtons(row, registrationId, token, token_type) {
  row.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async () => {
      const newStatus = button.dataset.action;
      if (newStatus === "rejected" && !confirm("Bạn có chắc muốn từ chối/hủy đơn này?")) return;
      await handleUpdateStatus(registrationId, newStatus, button, token, token_type);
    });
  });
}

// API cập nhật trạng thái đơn
async function handleUpdateStatus(registrationId, newStatus, button, token, token_type) {
  const originalHTML = button.innerHTML;
  button.disabled = true;
  button.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i>...`;

  try {
    const res = await fetch(`http://localhost:8000/api/events/registrations/${registrationId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${token_type} ${token}`,
      },
      body: JSON.stringify({ status: newStatus }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Cập nhật thất bại");
    }

    const updated = await res.json();
    const row = button.closest("tr");
    row.querySelector("td:nth-child(4)").innerHTML = `<span class="status status-${updated.status}">${updated.status}</span>`;
    const actionCell = row.querySelector("td:nth-child(5)");
    actionCell.innerHTML = generateActionButtons(updated.status);
    addEventListenersToAdminButtons(row, registrationId, token, token_type);
  } catch (err) {
    alert(`Lỗi: ${err.message}`);
    console.error("handleUpdateStatus error:", err);
    button.disabled = false;
    button.innerHTML = originalHTML;
  }
}

// Dòng này không cần thiết vì file này được `main.js` import và gọi `initEventUserPage`
initEventUserPage();
