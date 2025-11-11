import { initPush } from './web-push.js';

async function loadComponent(id, path) {
  const container = document.getElementById(id);
  const res = await fetch(path);
  container.innerHTML = await res.text();
}

await loadComponent("header-container", "./components/header.html");
initHeader();

export function initHeader() {
  const toggle = document.getElementById("menu-toggle");
  const nav = document.getElementById("main-nav");
  const overlay = document.getElementById("overlay");
  const navList = document.querySelector(".nav-list");
  const actions = document.getElementById("actions");
  const mobileActions = document.getElementById("mobile-actions");
  const userArea = document.getElementById("user-area");

  const menuByRole = {
    guest: [
      { href: "/", label: "Trang chủ" },
      { href: "/contact", label: "Liên hệ" },
      { href: "/about", label: "Về chúng tôi" },
    ],
    volunteer: [
      { href: "/", label: "Trang chủ" },
      { href: "/event-wall", label: "Kênh trao đổi" },
      { href: "/contact", label: "Liên hệ" },
      { href: "/about", label: "Về chúng tôi" },
    ],
    manager: [
      { href: "/", label: "Trang chủ" },
      { href: "/event-wall", label: "Kênh trao đổi" },
      { href: "/event-manager", label: "Quản lý sự kiện" },
      { href: "/contact", label: "Liên hệ" },
      { href: "/about", label: "Về chúng tôi" },
    ],
    admin: [
      { href: "/", label: "Trang chủ" },
      { href: "/event-admin", label: "Quản lý sự kiện" },
      { href: "/user-admin", label: "Quản lý người dùng" },
    ],
  };

  toggle.addEventListener("click", e => {
    e.stopPropagation();
    nav.classList.toggle("open");
    overlay.classList.toggle("show");
  });

  document.addEventListener("click", e => {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove("open");
      overlay.classList.remove("show");
    }

    document.querySelectorAll(".user-dropdown").forEach(drop => {
      const avatar = drop.previousElementSibling;
      if (!drop.contains(e.target) && !avatar.contains(e.target) && !nav.contains(e.target)) {
        drop.classList.remove("show");
      }
    });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      nav.classList.remove("open");
      overlay.classList.remove("show");
    }
  });

  loadUserHeader();

  function loadUserHeader() {
    try {
      const user = getTokenPayload();
      if (!user) {
        renderGuestActions();
        renderMenu("guest");
        return;
      }
      const role = user.role;
      renderMenu(role);
      renderUserActions(role, user);
    } catch {
      renderGuestActions();
      renderMenu("guest");
      localStorage.setItem("role", "guest");
    }
  }

  function renderMenu(role) {
    navList.innerHTML = "";
    (menuByRole[role] || menuByRole["guest"]).forEach(item => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = item.href;
      a.textContent = item.label;
      if (location.pathname === item.href) li.classList.add("active");
      li.appendChild(a);
      navList.appendChild(li);
    });
  }

  function renderGuestActions() {

    const html = `<a href="/login" class="btn btn-ghost">Đăng nhập</a>
                  <a href="/register" class="btn btn-primary">Đăng ký</a>`;
    actions.innerHTML = html;
    mobileActions.innerHTML = html;
  }

  async function setupNotifications() {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    const headers = { "Authorization": `${token_type} ${token}` };

    const btn = document.querySelector(".notification-btn");
    const countSpan = document.querySelector(".notification-count");
    const dropdown = document.createElement("div");

    dropdown.className = "notification-dropdown hidden";
    btn.parentNode.insertBefore(dropdown, btn.nextSibling);

    const res = await fetch("http://localhost:8000/api/notifications/", { headers });
    if (!res.ok) return;
    const notifications = await res.json();

    const unread = notifications.filter(n => n.is_read === false).length;

    if (unread > 0) countSpan.textContent = unread;
    else countSpan.style.display = "none";

    dropdown.innerHTML = notifications.length === 0
      ? "<div class='ntf-empty'>Không có thông báo</div>"
      : notifications.map(n => `
        <div class="ntf-item ${n.is_read ? "read" : "unread"}">
          <div class="ntf-message">${n.message}</div>
          <div class="ntf-time">${new Date(n.created_at).toLocaleString()}</div>
        </div>
      `).join("");

    btn.addEventListener("click", async (ev) => {
      ev.stopPropagation();
      dropdown.classList.toggle("hidden");

      if (!dropdown.classList.contains("hidden") && unread > 0) {
        const patchRes = await fetch("http://localhost:8000/api/notifications/", {
          method: "PATCH",
          headers
        });

        if (patchRes.ok) {
          countSpan.style.display = "none";
          dropdown.querySelectorAll(".ntf-item").forEach(e => e.classList.add("read"));
        }
      }
    });

    document.addEventListener("click", () => {
      dropdown.classList.add("hidden");
    });

    dropdown.addEventListener("click", ev => ev.stopPropagation());
  }


  function renderUserActions(role, user) {
    initPush();

    const avatarUrl = user.avatar_url ? avatar_url : "../assets/default-avatar.png";
    const html = `
      <button class="notification-btn" aria-label="Thông báo"><i class="fa-solid fa-bell"></i><span class="notification-count">3</span></button>
      <div class="user-avatar user-menu-toggle"><img src="${avatarUrl}" alt="Avatar"></div>
      <div class="user-dropdown">
        ${role === "volunteer" ? '<a href="/history">Lịch sử tham gia</a>' : ''}
        <a href="/profile">Thông tin</a>
        <button class="logout-btn">Đăng xuất</button>
      </div>
    `;
    userArea.innerHTML = html;
    setupNotifications();

    const logoutBtn = userArea.querySelector(".logout-btn");
    if (logoutBtn) logoutBtn.addEventListener("click", async () => {
      try {
        const token = localStorage.getItem("access_token");
        const token_type = localStorage.getItem("token_type");

        const res = await fetch("http://localhost:8000/auth/logout", {
          method: "POST",
          credentials: "include",
          headers: { "Authorization": `${token_type} ${token}` }

        });
        if (res.ok) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("token_type");
          localStorage.removeItem("role");
          localStorage.removeItem("status");
          location.href = "/login";
        }
        else alert("Đăng xuất thất bại");
      } catch {
        alert("Lỗi kết nối");
      }
    });

    const avatar = userArea.querySelector(".user-menu-toggle");
    const dropdown = avatar.nextElementSibling;
    avatar.addEventListener("click", e => { e.stopPropagation(); dropdown.classList.toggle("show"); });
  }
}

await loadComponent("footer-container", "./components/footer.html");

const main = document.getElementById("main-content");

export function getTokenPayload() {
  try {
    const token = localStorage.getItem("access_token");
    const payload = token.split(".")[1];
    const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decoded);
  } catch (e) {
    return null;
  }
}

export async function navigateTo(page) {
  const status = getTokenPayload()?.status;
  if (status === "banned") {
    const res = await fetch(`./pages/banned.html`);
    const html = await res.text();
    main.innerHTML = html;
    window.history.pushState({}, "", `/${page}`);
    return;
  }
  const res = await fetch(`./pages/${page}.html`);
  const html = await res.text();
  main.innerHTML = html;
  window.history.pushState({}, "", `/${page}`);

  document.querySelectorAll(`script[data-page]`).forEach(s => s.remove());

  const script = document.createElement("script");
  script.src = `./js/${page}.js?cacheBust=${Date.now()}`;
  script.type = "module";
  script.dataset.page = page;
  document.body.appendChild(script);
}

document.body.addEventListener("click", (e) => {
  const link = e.target.closest("a");
  if (link && link.getAttribute("href")?.startsWith("/")) {
    e.preventDefault();
    const page = link.getAttribute("href").replace("/", "");
    navigateTo(page || "home");
  }
});

window.addEventListener("popstate", () => {
  const path = window.location.pathname.replace("/", "") || "home";
  navigateTo(path);
});

const currentPath = window.location.pathname.replace("/", "") || "home";
navigateTo(currentPath);