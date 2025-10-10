document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menu-toggle");
  const nav = document.querySelector(".main-nav");
  const overlay = document.getElementById("overlay");

  // Toggle mở/đóng menu
  toggle.addEventListener("click", (e) => {
    e.stopPropagation();
    nav.classList.toggle("open");
    overlay.classList.toggle("show");
  });

  // Khi click ra ngoài -> đóng menu
  document.addEventListener("click", (e) => {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove("open");
      overlay.classList.remove("show");
    }
  });

  // Khi resize -> reset lại trạng thái
  window.addEventListener("resize", () => {
    if (window.innerWidth > 860) {
      nav.classList.remove("open");
      overlay.classList.remove("show");
    }
  });
});
