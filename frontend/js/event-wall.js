import { fetchJoinedEvents } from "./joined-event-tab.js";
import { fetchMyPosts } from "./my-post-tab.js"
import { formatTimeAgo, attachReactions } from "./post-utils.js";

export function initTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  const contents = document.querySelectorAll(".event-tab-content");

  const role = localStorage.getItem("role");
  const joinedTab = document.querySelector('.tab-btn[data-tab="joined"]');

  if (joinedTab) {
    if (role === "volunteer") {
      joinedTab.textContent = "Đã tham gia";
    } else if (role === "manager") {
      joinedTab.textContent = "Sự kiện quản lý";
    }
  }

  // Tabs chuyển đổi
  tabs.forEach((tab) => {
    tab.addEventListener("click", (e) => {
      e.preventDefault();
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const target = tab.dataset.tab;
      contents.forEach((c) => {
        if (c.id === target) {
          c.classList.remove("hidden");
        } else {
          c.classList.add("hidden");
        }
      });

      // Cuộn trang về đầu khi chuyển tab
      window.scrollTo({ top: 0, behavior: "smooth" });

      // Nếu bấm tab "joined", gọi module
      if (target === "joined") {
        fetchJoinedEvents();
      } else if (target === "my-post") {
        fetchMyPosts();
      }
    });
  });
}

export function initPostsPage() {
  const container = document.getElementById("all");
  if (!container) return;

  let allPosts = [];

  async function fetchPosts() {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    // Chưa có token chuyển sang login
    if (!token || !token_type) {
      window.location.href = "/login";
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/posts/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `${token_type} ${token}`,
        },
      });

      if (!res.ok) throw new Error(await res.text());
      allPosts = await res.json();
      renderPosts(allPosts);
    } catch (err) {
      console.error("Không thể tải bài post:", err);
    }
  }

  async function renderPosts(posts) {
    container.innerHTML = ""; // Xóa cũ

    // Đọc template HTML của 1 post (từ file event-post.html)
    const response = await fetch("../pages/event-post.html");
    let postHTML = await response.text();
    const match = postHTML.match(/<div class="event-post">[\s\S]*<\/div>/);
    if (!match) {
      console.error("Không tìm thấy khối event-post trong file HTML!");
      return;
    }
    postHTML = match[0];

    // Map cảm xúc giống attachReactions()
    const reactions = {
      like: { img: "/assets/like.png", text: "Thích", color: "#1877f2" },
      love: { img: "/assets/love.png", text: "Yêu thích", color: "#f33e58" },
      haha: { img: "/assets/haha.png", text: "Haha", color: "#f7b125" },
      wow: { img: "/assets/wow.png", text: "Wow", color: "#f7b125" },
      sad: { img: "/assets/sad.png", text: "Buồn", color: "#f7b125" },
      angry: { img: "/assets/angry.png", text: "Phẫn nộ", color: "#e9710f" },
    };

    posts.forEach(post => {
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = postHTML.trim();
      const postElement = tempDiv.firstElementChild;
      postElement.dataset.postId = post.post_id;

      // Họ tên
      const fullName =
        (post.first_name || "") + (post.last_name ? ` ${post.last_name}` : "");
      postElement.querySelector(".post-info h4").textContent =
        fullName.trim() || `User ${post.user_id}`;

      // Thời gian (hiển thị theo “bao lâu trước”)
      postElement.querySelector(".post-info p").textContent = formatTimeAgo(
        post.created_at
      );

      // Nội dung
      postElement.querySelector(".event-content").textContent = post.content;

      // Ảnh
      const imgEl = postElement.querySelector(".event-img");
      if (post.images_url) {
        imgEl.src = post.images_url;
        imgEl.alt = "Post image";
      } else {
        imgEl.style.display = "none"; // Không có ảnh thì ẩn
      }

      // --- Hiển thị số lượng react và comment ---
      const reactCountEl = postElement.querySelector(".react-count");
      const commentCountEl = postElement.querySelector(".comment-count");

      // Ẩn nếu bằng 0 hoặc null
      if (post.react_count && post.react_count > 0) {
        reactCountEl.textContent = post.react_count.toString();
        reactCountEl.style.display = "inline";
      } else {
        reactCountEl.style.display = "none";
        reactCountEl.textContent = "";
      }

      if (post.comment_count && post.comment_count > 0) {
        commentCountEl.textContent = post.comment_count.toString();
        commentCountEl.style.display = "inline";
      } else {
        commentCountEl.style.display = "none";
      }

      // --- Thiết lập giao diện cảm xúc ban đầu ---
      const likeBtn = postElement.querySelector(".like-btn");
      const likeIcon = postElement.querySelector(".like-icon");
      const likeText = postElement.querySelector(".like-text");

      if (post.user_react) {
        const type = post.user_react.toLowerCase();
        const reaction = reactions[type] || reactions.like;
        likeIcon.src = reaction.img;
        likeText.textContent = reaction.text;
        likeText.style.color = reaction.color;
        likeBtn.classList.add("active");
      } else {
        // Mặc định nếu chưa react
        likeIcon.src = "/assets/like-default.png";
        likeText.textContent = "Thích";
        likeText.style.color = "#65676b";
        likeBtn.classList.remove("active");
      }
      // Gắn thông tin cảm xúc hiện tại để attachReactions() biết
      postElement.dataset.userReact = post.user_react || "default";


      // --- Gắn vào container ---
      container.appendChild(postElement);

      // --- Gắn sự kiện cảm xúc ---
      if (typeof attachReactions === "function") attachReactions(postElement);
    });
  }

  fetchPosts();
}

export function initCommentsOverlay() {
  // Nếu đã gắn listener rồi thì không gắn nữa
  if (window.commentOverlayInitialized) return;
  window.commentOverlayInitialized = true;

  document.addEventListener("click", async function (e) {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");

    // Mở overlay
    if (e.target.closest(".comment-btn")) {
      const postElement = e.target.closest(".event-post");
      const postId = postElement.dataset.postId;
      const overlay = document.getElementById("postOverlay");
      const overlayContent = document.getElementById("overlayPostContent");
      const overlayAuthorName = document.getElementById("overlayAuthorName");
      const commentList = document.getElementById("commentList");

      // Lấy tên tác giả từ bài post gốc
      const authorNameEl = postElement.querySelector(".post-info h4");
      const authorName = authorNameEl ? authorNameEl.textContent.trim() : "Người dùng";

      // Gán tiêu đề overlay
      overlayAuthorName.textContent = `Bài viết của ${authorName}`;

      overlayContent.innerHTML = "";
      const clonedPost = postElement.cloneNode(true); // sao chép toàn bộ node
      overlayContent.appendChild(clonedPost);

      // Gắn lại sự kiện cảm xúc cho post trong overlay
      if (typeof attachReactions === "function") {
        attachReactions(clonedPost);
      }

      overlay.classList.remove("hidden");

      // --- Fetch comment theo post_id ---
      if (!token || !token_type) {
        console.warn("Chưa đăng nhập, chuyển đến login");
        window.location.href = "/login";
        return;
      }

      try {
        const res = await fetch(`http://localhost:8000/api/comments/posts/${postId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token_type} ${token}`
          }
        });

        if (!res.ok) {
          console.error("Lỗi tải bình luận:", await res.text());
          return;
        }

        const comments = await res.json();
        commentList.innerHTML = ""; // Xóa comment cũ

        comments.forEach(c => {
          const div = document.createElement("div");
          div.classList.add("comment-item");
          div.innerHTML = `
            <img src="/assets/default-avatar.png" class="avatar-comment" alt="user" />
            <div class="comment-content">
              <p><strong>${c.first_name} ${c.last_name}</strong> ${c.content}</p>
            </div>`;
          commentList.appendChild(div);
        });
        const commentCount = comments.length;
        // Cập nhật comment_count cho post gốc
        const countEl = postElement.querySelector(".comment-count");
        if (commentCount <= 0) {
          countEl.textContent = "";
          countEl.style.display = "none";
        } else {
          countEl.textContent = commentCount.toString();
          countEl.style.display = "inline";
        }

      } catch (err) {
        console.error("Không thể tải bình luận:", err);
      }
    }

    // Đóng overlay
    if (e.target.id === "closeOverlayBtn" || e.target.classList.contains("post-overlay")) {
      document.getElementById("postOverlay").classList.add("hidden");
    }

    // Gửi bình luận
    if (e.target.id === "overlaySendBtn" || e.target.closest("#overlaySendBtn")) {
      const input = document.getElementById("overlayCommentInput");
      const commentList = document.getElementById("commentList");
      const text = input.value.trim();
      if (!text) return;

      const overlayContent = document.getElementById("overlayPostContent");
      const postId = overlayContent.querySelector(".event-post").dataset.postId;

      try {
        const res = await fetch(`http://localhost:8000/api/comments/posts/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token_type} ${token}`
          },
          body: JSON.stringify({ content: text })
        });

        if (!res.ok) {
          console.error("Lỗi gửi bình luận:", await res.text());
          return;
        }

        const newComment = await res.json();
        const div = document.createElement("div");
        div.classList.add("comment-item");
        div.innerHTML = `
        <img src="/assets/default-avatar.png" class="avatar-comment" alt="user" />
        <div class="comment-content">
          <p><strong>${newComment.first_name} ${newComment.last_name}</strong> ${newComment.content}</p>
        </div>`;
        commentList.appendChild(div);
        input.value = "";

        // === Lấy comment_count mới từ API (đảm bảo là số) ===
        const commentCount =
          typeof newComment.comment_count === "number"
            ? newComment.comment_count
            : parseInt(newComment.comment_count || "0", 10);

        // === Cập nhật số comment ở bài post chính ===
        const mainPost = document.querySelector(`.event-post[data-post-id="${postId}"]`);
        if (mainPost) {
          const countEl = mainPost.querySelector(".comment-count");
          if (commentCount > 0) {
            countEl.textContent = commentCount.toString();
            countEl.style.display = "inline";
          } else {
            countEl.textContent = "";
            countEl.style.display = "none";
          }
        }

        // === Cập nhật số comment ở overlay ===
        const overlayPost = overlayContent.querySelector(".event-post");
        if (overlayPost) {
          const countEl = overlayPost.querySelector(".comment-count");
          if (commentCount > 0) {
            countEl.textContent = commentCount.toString();
            countEl.style.display = "inline";
          } else {
            countEl.textContent = "";
            countEl.style.display = "none";
          }
        }
      } catch (err) {
        console.error("Không thể gửi bình luận:", err);
      }
    }

  });
}
// ======= HIỂN THỊ OVERLAY KHI BÌNH LUẬN =======


initTabs();
initPostsPage();
initCommentsOverlay();