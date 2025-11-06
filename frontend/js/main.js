async function loadComponent(id, path) {
  const container = document.getElementById(id);
  const res = await fetch(path);
  container.innerHTML = await res.text();
}

await loadComponent("header-container", "./components/header.html");
await initHeader();

export async function initHeader() {
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

  await loadUserHeader();

  async function loadUserHeader() {
    try {
      const token = localStorage.getItem("access_token");
      const token_type = localStorage.getItem("token_type");
      const res = await fetch("http://localhost:8000/api/users/me", {
        headers: { "Authorization": `${token_type} ${token}` }
      });
      if (res.status === 401) { renderGuestActions(); renderMenu("guest"); return; }
      if (!res.ok) throw new Error(`Unexpected status: ${res.status}`);
      const user = await res.json();
      const role = user.role || "guest";
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

  function renderUserActions(role, user) {
    const avatarUrl = "../assets/default-avatar.png";
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

    const logoutBtn = userArea.querySelector(".logout-btn");
    if (logoutBtn) logoutBtn.addEventListener("click", async () => {
      try {
        const token = localStorage.getItem("access_token");
        const token_type = localStorage.getItem("token_type");
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        localStorage.removeItem("role");
        localStorage.removeItem("status");
        const res = await fetch("http://localhost:8000/auth/logout", {
          method: "POST",
          credentials: "include",
          headers: { "Authorization": `${token_type} ${token}` }

        });
        if (res.ok) location.href = "/login";
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

export async function navigateTo(page) {
  const status = localStorage.getItem("status");
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