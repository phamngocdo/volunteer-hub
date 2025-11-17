export async function navigateTo(page) {
  const main = document.getElementById("main-content");

  let path = `./pages/${page}.html`;
  let scriptPath = `./js/${page}.js`;

  // Nếu page dạng event-wall/joined/1
  if (page.startsWith("event-wall/joined/")) {
    path = `./pages/event-wall/event-joined.html`;
    scriptPath = `./js/event-wall/event-joined.js`;
  }

  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Không tìm thấy file: ${path}`);
    const html = await res.text();
    main.innerHTML = html;

    // Xóa script cũ
    document.querySelectorAll(`script[data-page]`).forEach(s => s.remove());

    // Load script mới
    const script = document.createElement("script");
    script.src = `${scriptPath}?cacheBust=${Date.now()}`;
    script.type = "module";
    script.dataset.page = page;
    document.body.appendChild(script);

    window.history.pushState({}, "", `/${page}`);
  } catch (err) {
    console.error("Lỗi load trang:", err);
  }
}

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

      // dùng navigateTo()
      div.addEventListener("click", () => {
        navigateTo(`event-wall/joined/${event.event_id}`);
      });
      container.appendChild(div);
    });

  } catch (err) {
    console.error("Không thể tải events đã tham gia:", err);
  }
}
