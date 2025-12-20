/**
 * @file: joined-event-tab.js
 * @description: Logic tải và hiển thị danh sách các sự kiện mà người dùng đã tham gia (Tab "Đã tham gia").
 */

/**
 * Tải danh sách sự kiện đã tham gia từ API
 */
export async function fetchJoinedEvents() {
  const container = document.getElementById("joinedEventsContainer");
  if (!container) return;

  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/api/events/joined", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `${token_type} ${token}`
      }
    });

    if (!res.ok) throw new Error(await res.text());
    const events = await res.json();

    container.innerHTML = ""; // Xóa cũ
    events.forEach(event => {
      const div = document.createElement("div");
      div.classList.add("joined-event");
      div.innerHTML = `
        <img src="${event.image_url || '../assets/default-event.png'}" alt="Event" class="event-avatar" />
        <div class="event-info">
          <h4 class="event-name">${event.title}</h4>
          <p class="member-count">${event.member_count} thành viên</p>
        </div>
      `;

      div.addEventListener("click", () => {
        window.location.href = `/event-wall/joined/${event.event_id}`;
      });
      container.appendChild(div);
    });

  } catch (err) {
    console.error("Không thể tải events đã tham gia:", err);
  }
}
