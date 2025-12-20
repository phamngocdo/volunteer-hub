/**
 * @file: home.js
 * @description: Logic cho trang chủ, bao gồm hiển thị danh sách sự kiện, bộ lọc, và popup chi tiết sự kiện.
 */

import { navigateTo, getTokenPayload } from "/js/main.js";

/**
 * Khởi tạo trang chủ
 * Lấy dữ liệu sự kiện, render danh sách, và xử lý các bộ lọc.
 */
export function initHomePage() {
  const container = document.getElementById("eventsContainer");
  if (!container) return;

  const searchInput = document.getElementById("searchInput");
  const statusFilter = document.getElementById("statusFilter");
  const categoryFilter = document.getElementById("categoryFilter");
  const dateFilter = document.getElementById("dateFilter");

  const modal = document.getElementById("eventModal");
  const modalImage = document.getElementById("modalImage");
  const modalTitle = document.getElementById("modalTitle");
  const modalDescription = document.getElementById("modalDescription");
  const joinBtn = document.getElementById("joinEventBtn");
  const joinError = document.getElementById("joinError");
  const closeBtn = document.querySelector(".modal-close");

  let allEvents = [];
  let currentEvent = null;


  /**
   * Tải danh sách sự kiện từ API (có cache sessionStorage)
   */
  async function fetchEvents() {
    try {
      const cached = sessionStorage.getItem("events_data");
      const cacheTime = sessionStorage.getItem("events_cache_time");
      const now = Date.now();

      if (cached && cacheTime && now - parseInt(cacheTime) < 60000) {
        allEvents = JSON.parse(cached);
        renderEvents(allEvents);
        return;
      }

      const res = await fetch("http://localhost:8000/api/events/");
      allEvents = await res.json();

      sessionStorage.setItem("events_data", JSON.stringify(allEvents));
      sessionStorage.setItem("events_cache_time", now.toString());

      renderEvents(allEvents);
    } catch (err) {
      console.error("Lỗi tải sự kiện:", err);
    }
  }

  function formatDate(dateStr) {
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
  }


  /**
   * Render danh sách sự kiện ra giao diện
   * @param {Array} events - Mảng các object sự kiện
   */
  function renderEvents(events) {
    container.innerHTML = "";
    if (events.length === 0) {
      container.innerHTML = "<p>Không có sự kiện nào phù hợp.</p>";
      return;
    }

    events.forEach(ev => {
      const start = formatDate(ev.start_date);
      const end = formatDate(ev.end_date);
      const volunteer_number = ev.volunteer_number;
      const hot = ev.volunteer_number > 1;

      const card = document.createElement("div");
      card.className = "event-card";
      card.innerHTML = `
        ${hot ? '<span class="event-hot">HOT</span>' : ""}
        <img src="${ev.image_url}" class="event-image" alt="${ev.title}" />
        <div class="event-content">
          <h3 class="event-title">${ev.title}</h3>
          <p class="event-meta"><i class="fa-solid fa-location-dot"></i> <strong>Địa điểm:</strong> ${ev.location}</p>
          <p class="event-meta"><i class="fa-solid fa-person"></i> <strong>Số người đã tham gia:</strong> ${volunteer_number}</p>
          <p class="event-meta"><i class="fa-solid fa-calendar-days"></i> <strong>Thời gian:</strong> ${start} - ${end}</p>
        </div>
      `;

      card.addEventListener("click", () => openModal(ev));
      container.appendChild(card);
    });
  }


  /**
   * Mở modal chi tiết sự kiện
   * @param {Object} ev - Object sự kiện
   */
  function openModal(ev) {
    currentEvent = ev;
    modalImage.src = ev.image_url;

    modalTitle.textContent = ev.title;

    modalDescription.innerHTML = `
    <p class="event-meta"><i class="fa-solid fa-location-dot"></i> <strong>Địa điểm:</strong> ${ev.location}</p>
    <p class="event-meta"><i class="fa-solid fa-person"></i> <strong>Số người đã tham gia:</strong> ${ev.volunteer_number}</p>
    <p class="event-meta"><i class="fa-solid fa-calendar-days"></i> <strong>Thời gian:</strong> ${formatDate(ev.start_date)} - ${formatDate(ev.end_date)}</p>
    </br>
    <h2 class="modal-subtitle">Mô tả sự kiện</h2>
    </br>
    <div class="event-desc-text">${ev.description || "Không có mô tả."}</div>
  `;

    joinError.textContent = "";
    modal.classList.remove("hidden");
    updateJoinButton(ev.event_id);

    history.pushState({ modal: true, eventId: ev.event_id }, "", `?event=${ev.event_id}`);
  }


  /**
   * Đóng modal chi tiết sự kiện
   * @param {boolean} push - Có cập nhật lại URL history hay không
   */
  function closeModal(push = true) {
    modal.classList.add("hidden");
    currentEvent = null;
    if (push) history.pushState({ modal: false }, "", "/home");
  }


  /**
   * Kiểm tra trạng thái đăng ký của user đối với sự kiện
   * @param {number} eventId - ID sự kiện
   * @returns {string} - Trạng thái đăng ký (pending, approved, etc.) hoặc "not_registered"
   */
  async function fetchRegistrationStatus(eventId) {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    if (!token || !token_type) return "not_registered";

    try {
      const res = await fetch(`http://localhost:8000/api/events/${eventId}/registration-status/`, {
        headers: { "Authorization": `${token_type} ${token}` }
      });
      if (!res.ok) return "not_registered";
      const data = await res.json();
      return data.registration_status;
    } catch {
      return "not_registered";
    }
  }


  /**
   * Cập nhật nút tham gia/hủy dựa trên trạng thái đăng ký và role user
   * @param {number} eventId - ID sự kiện
   */
  async function updateJoinButton(eventId) {
    const userRole = getTokenPayload()?.role || "guest";

    if (userRole === "manager" || userRole === "admin") {
      joinBtn.style.display = "none";
      return;
    }

    joinBtn.disabled = false;
    joinBtn.classList.remove("disabled");

    joinBtn.innerHTML = "";

    if (userRole === "guest") {
      joinBtn.innerHTML = `<i class="fa-solid fa-plus"></i> Tham gia sự kiện`;
      joinBtn.onclick = async () => await navigateTo("/login");
      return;
    }

    const status = await fetchRegistrationStatus(eventId);

    switch (status) {
      case "approved":
        joinBtn.innerHTML = `<i class="fa-solid fa-xmark"></i> Hủy đăng ký`;
        joinBtn.onclick = async () => await cancelEvent(eventId);
        break;

      case "completed":
      case "event_ended":
        joinBtn.innerHTML = `<i class="fa-solid fa-circle-check"></i> Sự kiện đã kết thúc`;
        joinBtn.disabled = true;
        break;


      case "pending":
        joinBtn.innerHTML = `<i class="fa-solid fa-hourglass-half"></i> Đang chờ duyệt`;
        joinBtn.disabled = true;
        break;

      case "rejected":
        joinBtn.innerHTML = `<i class="fa-solid fa-rotate-right"></i> Đăng ký lại`;
        joinBtn.onclick = async () => await joinEvent();
        break;

      default:
        joinBtn.innerHTML = `<i class="fa-solid fa-plus"></i> Tham gia sự kiện`;
        joinBtn.onclick = async () => await joinEvent();
        break;
    }
  }


  /**
   * Xử lý hành động tham gia sự kiện
   */
  async function joinEvent() {
    if (!currentEvent) return;

    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    const joinError = document.getElementById("joinError");
    joinError.textContent = "";
    if (!token || !token_type) {
      window.location.href = "/login";
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/api/events/${currentEvent.event_id}/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `${token_type} ${token}`
        }
      });

      if (res.status === 403) {
        joinError.textContent = "Bạn không có quyền tham gia sự kiện này.";
        joinError.style.color = "red";
        return;
      }

      if (!res.ok) throw new Error("Lỗi đăng ký");

      joinError.textContent = "Tham gia sự kiện thành công!";
      joinError.style.color = "green";

      setTimeout(closeModal, 1000);
    } catch {
      joinError.textContent = "Không thể tham gia. Vui lòng thử lại.";
      joinError.style.color = "red";
    }
  }



  /**
   * Xử lý hành động hủy tham gia sự kiện
   * @param {number} eventId - ID sự kiện
   */
  async function cancelEvent(eventId) {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    const joinError = document.getElementById("joinError");
    joinError.textContent = "";
    if (!token || !token_type) {
      window.location.href = "/login";
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/api/events/${eventId}/registration`, {
        method: "DELETE",
        headers: { "Authorization": `${token_type} ${token}` }
      });
      if (!res.ok) throw new Error("Hủy thất bại");
      joinError.textContent = "Hủy tham gia sự kiện thành công!";
      joinError.style.color = "green";
      setTimeout(closeModal, 1000);

    } catch {
      joinError.textContent = "Không thể hủy. Vui lòng thử lại.";
    }
  }


  /**
   * Áp dụng bộ lọc (tìm kiếm, trạng thái, danh mục, ngày) lên danh sách sự kiện
   */
  function applyFilters() {
    const keyword = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    const category = categoryFilter.value;
    const date = dateFilter.value ? new Date(dateFilter.value) : null;

    const filtered = allEvents.filter(ev => {
      const matchesSearch = ev.title.toLowerCase().includes(keyword);
      const matchesStatus = status ? ev.status === status : true;
      const matchesCategory = category ? ev.category === category : true;
      const matchesDate = date ? new Date(ev.start_date) >= date : true;
      const validStatus = ["approved", "completed"].includes(ev.status);
      return matchesSearch && matchesStatus && matchesCategory && matchesDate && validStatus;
    });

    renderEvents(filtered);
  }

  [searchInput, statusFilter, categoryFilter, dateFilter].forEach(el =>
    el.addEventListener("input", applyFilters)
  );

  closeBtn.addEventListener("click", () => closeModal());
  modal.addEventListener("click", e => {
    if (e.target === modal) closeModal();
  });

  fetchEvents();
}

initHomePage();