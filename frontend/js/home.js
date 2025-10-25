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
  const modalLocation = document.getElementById("modalLocation");
  const modalDate = document.getElementById("modalDate");
  const modalDescription = document.getElementById("modalDescription");
  const joinBtn = document.getElementById("joinEventBtn");
  const joinError = document.getElementById("joinError");
  const closeBtn = document.querySelector(".modal-close");

  let allEvents = [];
  let currentEvent = null;

  async function fetchEvents() {
    try {
      const res = await fetch("http://localhost:8000/api/events/");
      allEvents = await res.json();
      renderEvents(allEvents);
    } catch (err) {
      console.error("Lỗi tải sự kiện:", err);
    }
  }

  function formatDate(dateStr) {
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
  }

  function renderEvents(events) {
    container.innerHTML = "";
    if (events.length === 0) {
      container.innerHTML = "<p>Không có sự kiện nào phù hợp.</p>";
      return;
    }

    events.forEach(ev => {
      const start = formatDate(ev.start_date);
      const end = formatDate(ev.end_date);

      const card = document.createElement("div");
      card.className = "event-card";
      card.innerHTML = `
        ${ev.hot ? '<span class="event-hot">HOT</span>' : ""}
        <img src="${ev.image_url}" class="event-image" alt="${ev.title}" />
        <div class="event-content">
          <h3 class="event-title">${ev.title}</h3>
          <p class="event-meta"><i class="fa-solid fa-location-dot"></i> <strong>Địa điểm:</strong> ${ev.location}</p>
          <p class="event-meta"><strong>Ngày bắt đầu:</strong> ${start}</p>
          <p class="event-meta"><strong>Ngày kết thúc:</strong> ${end}</p>
        </div>
      `;
      card.addEventListener("click", () => openModal(ev));
      container.appendChild(card);
    });
  }

  function openModal(ev) {
    currentEvent = ev;
    modalImage.src = ev.image_url;
    modalTitle.textContent = ev.title;
    modalLocation.textContent = `📍 ${ev.location}`;
    modalDate.textContent = `📅 ${formatDate(ev.start_date)} - ${formatDate(ev.end_date)}`;
    modalDescription.textContent = ev.description || "Không có mô tả.";
    joinError.textContent = "";
    modal.classList.remove("hidden");
    updateJoinButton(ev.event_id);
  }

  async function fetchRegistrationStatus(eventId) {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    if (!token || !token_type) return "not_registered";

    try {
      const res = await fetch(`http://localhost:8000/api/events/${eventId}/status/`, {
        headers: {
          "Authorization": `${token_type} ${token}`
        }
      });
      if (!res.ok) return "not_registered";
      const data = await res.json();
      return data.status;
    } catch {
      return "not_registered";
    }
  }

  async function updateJoinButton(eventId) {
    const status = await fetchRegistrationStatus(eventId);
    joinBtn.disabled = false;
    joinBtn.classList.remove("disabled");

    switch (status) {
      case "approved":
        joinBtn.textContent = "❌ Hủy đăng ký";
        joinBtn.onclick = async () => await cancelEvent(eventId);
        break;
      case "completed":
        joinBtn.textContent = "✅ Đã hoàn thành";
        joinBtn.disabled = true;
        break;
      case "pending":
        joinBtn.textContent = "⏳ Đang chờ duyệt";
        joinBtn.disabled = true;
        break;
      case "rejected":
        joinBtn.textContent = "🔁 Đăng ký lại";
        joinBtn.onclick = async () => await joinEvent();
        break;
      default:
        joinBtn.textContent = "➕ Tham gia sự kiện";
        joinBtn.onclick = async () => await joinEvent();
        break;
    }
  }

  async function joinEvent() {
    if (!currentEvent) return;
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    if (!token || !token_type) {
      window.location.href = "/login";
      return;
    }
    joinError.textContent = "";

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

      alert("✅ Tham gia sự kiện thành công!");
      modal.classList.add("hidden");
    } catch {
      joinError.textContent = "❌ Không thể tham gia. Vui lòng thử lại.";
    }
  }

  async function cancelEvent(eventId) {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    if (!token || !token_type) {
      window.location.href = "/login";
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/api/events/${eventId}/cancel-registration`, {
        method: "POST",
        headers: {
          "Authorization": `${token_type} ${token}`
        }
      });
      if (!res.ok) throw new Error("Hủy thất bại");
      alert("❌ Bạn đã hủy đăng ký sự kiện này.");
      modal.classList.add("hidden");
    } catch {
      joinError.textContent = "Không thể hủy. Vui lòng thử lại.";
    }
  }

  function closeModal() {
    modal.classList.add("hidden");
  }

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

  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", e => {
    if (e.target === modal) closeModal();
  });

  fetchEvents();
}

initHomePage();
