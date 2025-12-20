/**
 * @file: event-joined.js
 * @description: Quản lý logic hiển thị danh sách bài viết trong một sự kiện cụ thể mà người dùng đã tham gia.
 */

import { formatTimeAgo, attachReactions } from "/js/post-utils.js";

let currentEventId = null;


/**
 * Tải danh sách bài viết theo ID sự kiện
 * @param {number} event_id - ID sự kiện cần tải bài viết
 */
export async function loadPostsByEvent(event_id) {
  const container = document.getElementById("all");
  if (!container) return;

  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");

  if (!token) return;

  try {
    const res = await fetch(`http://localhost:8000/api/posts/events/${event_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `${token_type} ${token}`,
      },
    });

    if (!res.ok) throw new Error(await res.text());
    const allPosts = await res.json();
    await renderPosts(allPosts, container);
  } catch (err) {
    console.error("Không thể tải bài post:", err);
    container.innerHTML = "<p style='text-align:center'>Không thể tải bài viết.</p>";
  }
}


/**
 * Render danh sách bài viết ra container
 * @param {Array} posts - Mảng bài viết
 * @param {HTMLElement} container - Element chứa danh sách bài viết
 */
async function renderPosts(posts, container) {
  container.innerHTML = "";

  let postTemplate = "";
  try {
    const response = await fetch("/pages/event-post.html");
    if (response.ok) {
      let text = await response.text();
      const match = text.match(/<div class="event-post">[\s\S]*<\/div>/);
      if (match) postTemplate = match[0];
    }
  } catch (e) { console.error("Lỗi tải template post", e); }

  if (!postTemplate) {
    container.innerHTML = "Lỗi template bài viết";
    return;
  }

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
    tempDiv.innerHTML = postTemplate.trim();
    const postElement = tempDiv.firstElementChild;

    postElement.dataset.postId = post.post_id;

    const fullName = (post.first_name || "") + (post.last_name ? ` ${post.last_name}` : "");
    postElement.querySelector(".post-info h4").textContent = fullName.trim() || `User ${post.user_id}`;
    postElement.querySelector(".post-info p").textContent = formatTimeAgo(post.created_at);
    postElement.querySelector(".event-content").textContent = post.content;

    const imgEl = postElement.querySelector(".event-img");
    if (post.images_url) {
      imgEl.src = post.images_url;
      imgEl.style.display = "block";
    } else {
      imgEl.style.display = "none";
    }

    const reactCountEl = postElement.querySelector(".react-count");
    if (post.react_count > 0) {
      reactCountEl.textContent = post.react_count;
      reactCountEl.style.display = "inline";
    } else {
      reactCountEl.style.display = "none";
    }

    const commentCountEl = postElement.querySelector(".comment-count");
    if (post.comment_count > 0) {
      commentCountEl.textContent = post.comment_count;
      commentCountEl.style.display = "inline";
    } else {
      commentCountEl.style.display = "none";
    }

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
      likeIcon.src = "/assets/like-default.png";
      likeText.textContent = "Thích";
      likeText.style.color = "#65676b";
      likeBtn.classList.remove("active");
    }
    postElement.dataset.userReact = post.user_react || "default";

    container.appendChild(postElement);

    try {
      if (typeof attachReactions === "function") attachReactions(postElement);
    } catch (err) {
      console.error("Error attaching reactions:", err);
    }

    const commentBtn = postElement.querySelector(".comment-btn");
    if (commentBtn) {
      console.log("Attached click event to comment button for post", post.post_id);
      commentBtn.addEventListener("click", (e) => {
        console.log("Comment button clicked for post", post.post_id);
        e.stopPropagation();
        openCommentOverlay(post);
      });
    }
  });
}


/**
 * Khởi tạo Overlay tạo bài viết mới
 */
export function initCreatePostOverlay() {
  const openBtn = document.getElementById("openCreatePostOverlay");
  const overlay = document.getElementById("createPostOverlay");
  const closeBtn = document.getElementById("closeCreatePostBtn");

  if (!openBtn || !overlay || !closeBtn) return;

  openBtn.addEventListener("click", () => overlay.classList.remove("hidden"));
  closeBtn.addEventListener("click", () => overlay.classList.add("hidden"));
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.classList.add("hidden");
  });
}


/**
 * Khởi tạo input và upload ảnh trong Overlay tạo bài viết
 */
export function initInputPost() {
  const textarea = document.getElementById("createPostInput");
  const imageUpload = document.getElementById("imageUpload");
  const imagePreviewContainer = document.getElementById("imagePreviewContainer");

  if (!textarea || !imageUpload) return;

  textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  });

  imageUpload.addEventListener("change", (event) => {
    const file = event.target.files[0];
    imagePreviewContainer.innerHTML = "";

    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const imgWrapper = document.createElement("div");
      imgWrapper.style.position = "relative";
      imgWrapper.style.display = "inline-block";

      const img = document.createElement("img");
      img.src = e.target.result;
      img.style.maxWidth = "100%";
      img.style.maxHeight = "200px";

      const removeBtn = document.createElement("button");
      removeBtn.innerHTML = "&times;";
      removeBtn.className = "remove-img-btn";
      removeBtn.style.position = "absolute";
      removeBtn.style.top = "5px";
      removeBtn.style.right = "5px";
      removeBtn.style.background = "rgba(0,0,0,0.5)";
      removeBtn.style.color = "white";
      removeBtn.style.border = "none";
      removeBtn.style.borderRadius = "50%";
      removeBtn.style.width = "24px";
      removeBtn.style.height = "24px";
      removeBtn.style.cursor = "pointer";

      removeBtn.onclick = () => {
        imgWrapper.remove();
        imageUpload.value = "";
      };

      imgWrapper.appendChild(img);
      imgWrapper.appendChild(removeBtn);
      imagePreviewContainer.appendChild(imgWrapper);
    };
    reader.readAsDataURL(file);
  });
}


/**
 * Xử lý sự kiện đăng bài viết mới
 * @param {number} eventId - ID sự kiện đang đăng bài
 */
export function initSubmitPost(eventId) {
  const submitBtn = document.getElementById("submitCreatePost");
  const textarea = document.getElementById("createPostInput");
  const imageUpload = document.getElementById("imageUpload");
  const overlay = document.getElementById("createPostOverlay");

  if (!submitBtn) return;

  const newBtn = submitBtn.cloneNode(true);
  submitBtn.parentNode.replaceChild(newBtn, submitBtn);

  newBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("access_token");
    const token_type = localStorage.getItem("token_type");
    const content = textarea.value.trim();
    const file = imageUpload.files[0];

    if (!content && !file) {
      showToast("Vui lòng nhập nội dung hoặc chọn ảnh!", 3000, "#f44336");
      return;
    }

    try {
      let imageUrl = null;

      if (file) {
        const formData = new FormData();
        formData.append("file", file);

        const uploadResponse = await fetch("http://localhost:8000/api/posts/upload-image", {
          method: "POST",
          body: formData,
          headers: { "Authorization": `${token_type} ${token}` },
        });

        if (!uploadResponse.ok) throw new Error("Upload ảnh thất bại!");
        const data = await uploadResponse.json();
        imageUrl = data.url || data;
      }

      const res = await fetch(`http://localhost:8000/api/posts/events/${eventId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `${token_type} ${token}`,
        },
        body: JSON.stringify({
          content,
          images_url: imageUrl,
        }),
      });

      if (!res.ok) {
        const error = await res.json();
        showToast(`Đăng bài thất bại: ${error.detail || "Lỗi"}`, 4000, "#f44336");
        return;
      }

      // Reset form
      textarea.value = "";
      imageUpload.value = "";
      document.getElementById("imagePreviewContainer").innerHTML = "";
      overlay.classList.add("hidden");

      showToast("Đăng bài thành công!", 3000, "#4CAF50");

      await loadPostsByEvent(eventId);

    } catch (err) {
      console.error("Lỗi khi đăng bài:", err);
      showToast("Lỗi hệ thống!", 4000, "#f44336");
    }
  });
}


/**
 * Hiển thị thông báo Toast
 * @param {string} message - Nội dung thông báo
 * @param {number} duration - Thời gian hiển thị (ms)
 * @param {string} bgColor - Màu nền
 */
export function showToast(message, duration = 3000, bgColor = "#333") {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.style.backgroundColor = bgColor;
  toast.textContent = message;
  toast.style.position = "fixed";
  toast.style.bottom = "20px";
  toast.style.left = "50%";
  toast.style.transform = "translateX(-50%)";
  toast.style.color = "white";
  toast.style.padding = "10px 20px";
  toast.style.borderRadius = "5px";
  toast.style.zIndex = "9999";

  document.body.appendChild(toast);

  setTimeout(() => toast.remove(), duration);
}

const pathSegments = window.location.pathname.split("/");
currentEventId = pathSegments[pathSegments.length - 1] || pathSegments[pathSegments.length - 2];
if (currentEventId && !isNaN(currentEventId)) {
  loadPostsByEvent(currentEventId);
  initCreatePostOverlay();
  initInputPost();
  initSubmitPost(currentEventId);
} else {
  console.error("Không tìm thấy Event ID hợp lệ từ URL");
}