const tabs = document.querySelectorAll(".tab-btn");
const contents = document.querySelectorAll(".event-tab-content");

// Tabs chuyển đổi
tabs.forEach((tab) => {
  tab.addEventListener("click", (e) => {
    e.preventDefault();
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const target = tab.dataset.tab;
    contents.forEach((c) =>
      c.id === target ? c.classList.remove("hidden") : c.classList.add("hidden")
    );
  });
});

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


  // Hàm định dạng thời gian “x phút trước”, “x giờ trước” hoặc ngày/giờ gốc
  function formatTimeAgo(createdAt) {
    const created = new Date(createdAt);
    const now = new Date();

    const diffMs = now - created;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / (24 * 3600000));

    if (diffMins < 60) {
      return `${diffMins} phút trước`;
    } else if (diffHours < 24) {
      return `${diffHours} giờ trước`;
    } else {
      return created.toLocaleString("vi-VN", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
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
      like: { img: "../assets/like.png", text: "Thích", color: "#1877f2" },
      love: { img: "../assets/love.png", text: "Yêu thích", color: "#f33e58" },
      haha: { img: "../assets/haha.png", text: "Haha", color: "#f7b125" },
      wow: { img: "../assets/wow.png", text: "Wow", color: "#f7b125" },
      sad: { img: "../assets/sad.png", text: "Buồn", color: "#f7b125" },
      angry: { img: "../assets/angry.png", text: "Phẫn nộ", color: "#e9710f" },
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
        likeIcon.src = "../assets/like-default.png";
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


function attachReactions(postElement) {
  const postId = postElement.dataset.postId;
  const likeBtn = postElement.querySelector(".like-btn");
  const reactionPopup = postElement.querySelector(".reaction-popup");
  const likeIcon = likeBtn.querySelector(".like-icon");
  const likeText = likeBtn.querySelector(".like-text");
  const reactCountSpan = postElement.querySelector(".react-count");

  let hideTimer;
  let isHoveringPopup = false;
  let currentReaction = postElement.dataset.userReact?.toLowerCase() || "default";


  const reactions = {
    like: { img: "../assets/like.png", text: "Thích", color: "#1877f2" },
    love: { img: "../assets/love.png", text: "Yêu thích", color: "#f33e58" },
    haha: { img: "../assets/haha.png", text: "Haha", color: "#f7b125" },
    wow: { img: "../assets/wow.png", text: "Wow", color: "#f7b125" },
    sad: { img: "../assets/sad.png", text: "Buồn", color: "#f7b125" },
    angry: { img: "../assets/angry.png", text: "Phẫn nộ", color: "#e9710f" },
  };

  // === HIỂN POPUP ===
  likeBtn.addEventListener("mouseenter", () => {
    clearTimeout(hideTimer);
    reactionPopup.classList.add("show");
  });
  likeBtn.addEventListener("mouseleave", () => {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      if (!isHoveringPopup) reactionPopup.classList.remove("show");
    }, 1000);
  });
  reactionPopup.addEventListener("mouseenter", () => {
    isHoveringPopup = true;
    clearTimeout(hideTimer);
  });
  reactionPopup.addEventListener("mouseleave", () => {
    isHoveringPopup = false;
    hideTimer = setTimeout(() => {
      reactionPopup.classList.remove("show");
    }, 200);
  });

  // === CHỌN CẢM XÚC ===
  const reactionImages = postElement.querySelectorAll(".reaction-popup img");
  const reactionTypes = ["like", "love", "haha", "wow", "sad", "angry"];

  reactionImages.forEach((img, i) => {
    img.dataset.type = reactionTypes[i];
    img.addEventListener("click", async () => {
      const type = img.dataset.type;
      const success = await sendReaction(postId, type);
      if (success) {
        const reaction = reactions[type];
        likeIcon.src = reaction.img;
        likeText.textContent = reaction.text;
        likeText.style.color = reaction.color;

        if (currentReaction === "default") updateReactCount(1);
        currentReaction = type;
      }
      reactionPopup.classList.remove("show");
    });
  });

  // === CLICK NÚT LIKE ===
  likeBtn.addEventListener("click", async () => {
    if (currentReaction === "default") {
      const success = await sendReaction(postId, "like");
      if (success) {
        likeIcon.src = "../assets/like.png";
        likeText.textContent = "Thích";
        likeText.style.color = "#1877f2";
        currentReaction = "like";
        updateReactCount(1);
      }
    } else {
      const success = await removeReaction(postId);
      if (success) {
        likeIcon.src = "../assets/like-default.png";
        likeText.textContent = "Thích";
        likeText.style.color = "#65676b";
        currentReaction = "default";
        updateReactCount(-1);
      }
    }
  });

  // === CẬP NHẬT COUNT TRỰC TIẾP ===
  function updateReactCount(delta) {
    let count = parseInt(reactCountSpan.textContent, 10);
    if (isNaN(count)) count = 0; // Đảm bảo count là số
    count += delta;
    if (count <= 0) {
      reactCountSpan.style.display = "none";
      reactCountSpan.textContent = "";
    } else {
      reactCountSpan.style.display = "inline";
      reactCountSpan.textContent = count.toString();
    }
  }
}

// =================== API CALLS ===================

async function sendReaction(postId, category) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    console.error("Không có token hợp lệ. Người dùng chưa đăng nhập.");
    return false;
  }

  try {
    const res = await fetch(`http://localhost:8000/api/reacts/posts/${postId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `${token_type} ${token}`,
      },
      body: JSON.stringify({ category }),
    });
    if (!res.ok) {
      console.error("Lỗi thả cảm xúc:", await res.text());
      return false;
    }
    return true;
  } catch (err) {
    console.error("Không thể gửi cảm xúc:", err);
    return false;
  }
}

async function removeReaction(postId) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    console.error("Không có token hợp lệ. Người dùng chưa đăng nhập.");
    return false;
  }

  try {
    const res = await fetch(`http://localhost:8000/api/reacts/posts/${postId}`, {
      method: "DELETE",
      headers: { "Authorization": `${token_type} ${token}` },
    });
    if (!res.ok) {
      console.error("Lỗi bỏ cảm xúc:", await res.text());
      return false;
    }
    return true;
  } catch (err) {
    console.error("Không thể bỏ cảm xúc:", err);
    return false;
  }
}


// ======= HIỂN THỊ OVERLAY KHI BÌNH LUẬN =======
document.addEventListener("click", async function (e) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");

  // Mở overlay
  if (e.target.closest(".comment-btn")) {
    const postElement = e.target.closest(".event-post");
    const postId = postElement.dataset.postId;
    const overlay = document.getElementById("postOverlay");
    const overlayContent = document.getElementById("overlayPostContent");
    const commentList = document.getElementById("commentList");

    overlayContent.innerHTML = "";
    const clonedPost = postElement.cloneNode(true); // sao chép toàn bộ node
    overlayContent.appendChild(clonedPost);

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
          <img src="../assets/default-avatar.png" class="avatar-sm" alt="user" />
          <div class="comment-content">
            <p><strong>${c.first_name} ${c.last_name}</strong> ${c.content}</p>
          </div>`;
        commentList.appendChild(div);
      });

    } catch (err) {
      console.error("Không thể tải bình luận:", err);
    }
  }

  // Đóng overlay
  if (e.target.id === "closeOverlayBtn" || e.target.classList.contains("post-overlay")) {
    document.getElementById("postOverlay").classList.add("hidden");
  }

  // Gửi bình luận
  if (e.target.id === "overlaySendBtn") {
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

      const newComment = await res.json(); // API trả về comment vừa tạo
      const div = document.createElement("div");
      div.classList.add("comment-item");
      div.innerHTML = `
        <img src="../assets/default-avatar.png" class="avatar-sm" alt="user" />
        <div class="comment-content">
          <p><strong>${newComment.first_name} ${newComment.last_name}</strong> ${newComment.content}</p>
        </div>`;
      commentList.appendChild(div);
      input.value = "";

      // === Cập nhật số lượng comment ở giao diện chính ===
      const mainPost = document.querySelector(`.event-post[data-post-id="${postId}"]`);
      if (mainPost) {
        const countEl = mainPost.querySelector(".comment-count");
        const count = Number(newComment.comment_count) || 0; // lấy từ API

        if (count <= 0) {
          countEl.textContent = "";
          countEl.style.display = "none";
        } else {
          countEl.textContent = count.toString();
          countEl.style.display = "inline";
        }
      }

    } catch (err) {
      console.error("Không thể gửi bình luận:", err);
    }
  }
});


initPostsPage();