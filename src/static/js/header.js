document.addEventListener("DOMContentLoaded", async () => {
  const toggle = document.getElementById("menu-toggle");
  const nav = document.getElementById("main-nav");
  const overlay = document.getElementById("overlay");
  const navList = document.querySelector(".nav-list");
  const actions = document.getElementById("actions");
  const mobileActions = document.getElementById("mobile-actions");

  const menuByRole = {
    volunteer: [
      { href: "/", label: "Trang chủ" },
      { href: "/event-wall", label: "Kênh trao đổi" },
      { href: "/contact", label: "Liên hệ" },
      { href: "/about", label: "Về chúng tôi" },
    ],
    manager: [
      { href: "/", label: "Trang chủ" },
      { href: "/event-wall", label: "Kênh trao đổi" },
      { href: "/manage-events", label: "Quản lý sự kiện" },
      { href: "/contact", label: "Liên hệ" },
      { href: "/about", label: "Về chúng tôi" },
    ],
    admin: [
      { href: "/", label: "Trang chủ" },
      { href: "/manage-events", label: "Quản lý sự kiện" },
      { href: "/manage-users", label: "Quản lý người dùng" },
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
    if (window.innerWidth > 860) {
      nav.classList.remove("open");
      overlay.classList.remove("show");
    }
  });

  await loadUserHeader();

  async function loadUserHeader() {
    try {
      const res = await fetch("/api/users/me");
      if (res.status === 401) { renderGuestActions(); renderMenu("volunteer"); return; }
      if (!res.ok) throw new Error(`Unexpected status: ${res.status}`);
      const user = await res.json();
      const role = user.role || "volunteer";
      renderMenu(role);
      renderUserActions(role, user);
    } catch {
      renderGuestActions();
      renderMenu("volunteer");
    }
  }

  function renderMenu(role) {
    navList.innerHTML = "";
    (menuByRole[role] || menuByRole["volunteer"]).forEach(item => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = item.href; a.textContent = item.label;
      if (location.pathname === item.href) li.classList.add("active");
      li.appendChild(a); navList.appendChild(li);
    });
  }

  function renderGuestActions() {
    const html = `<a href="/login" class="btn btn-ghost">Đăng nhập</a><a href="/register" class="btn btn-primary">Đăng ký</a>`;
    actions.innerHTML = html; mobileActions.innerHTML = html;
  }

  function renderUserActions(role, user) {
    const avatarUrl = user.avatar || "/static/images/default-avatar.png";
    const html = `
      <button class="notification-btn" aria-label="Thông báo">🔔<span class="notification-count">3</span></button>
      <div class="user-avatar user-menu-toggle"><img src="${avatarUrl}" alt="Avatar"></div>
      <div class="user-dropdown">${role === "volunteer" ? '<a href="/history">Lịch sử tham gia</a>' : ''}<a href="/profile">Thông tin</a><button class="logout-btn">Đăng xuất</button></div>
    `;
    const userArea = document.getElementById("user-area");
    userArea.innerHTML = html;

    const logoutBtn = userArea.querySelector(".logout-btn");
    if (logoutBtn) logoutBtn.addEventListener("click", async () => {
      try {
        const res = await fetch("/auth/logout", { method: "POST" });
        if (res.ok) location.href = "/login"; else alert("Đăng xuất thất bại");
      } catch { alert("Lỗi kết nối"); }
    });

    const avatar = userArea.querySelector(".user-menu-toggle");
    const dropdown = avatar.nextElementSibling;
    avatar.addEventListener("click", e => { e.stopPropagation(); dropdown.classList.toggle("show"); });
  }
});
