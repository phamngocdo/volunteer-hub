import { formatTimeAgo, attachReactions } from "../post-utils.js";

export function initPostsPage(event_id) {
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
      const res = await fetch(`http://localhost:8000/api/posts/events/${event_id}`, {
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
    const response = await fetch("../../pages/event-post.html");
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

export function initCreatePostOverlay() {
  const openBtn = document.getElementById("openCreatePostOverlay");
  const overlay = document.getElementById("createPostOverlay");
  const closeBtn = document.getElementById("closeCreatePostBtn");

  if (!openBtn || !overlay || !closeBtn) return;

  // Mở overlay khi click vào input
  openBtn.addEventListener("click", () => {
    overlay.classList.remove("hidden");
  });

  // Đóng overlay khi click nút ×
  closeBtn.addEventListener("click", () => {
    overlay.classList.add("hidden");
  });

  // Đóng overlay khi click ra ngoài box
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      overlay.classList.add("hidden");
    }
  });
}

export function initInputPost() {
  const textarea = document.getElementById("createPostInput");
  const imageUpload = document.getElementById("imageUpload");
  const imagePreviewContainer = document.getElementById("imagePreviewContainer");

  textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  });

  imageUpload.addEventListener("change", (event) => {
    const file = event.target.files[0]; // chỉ lấy 1 file
    imagePreviewContainer.innerHTML = ""; // xóa ảnh cũ

    if (!file) return; // nếu không chọn file thì thoát

    const reader = new FileReader();
    reader.onload = (e) => {
      const imgWrapper = document.createElement("div");
      imgWrapper.style.position = "relative";

      const img = document.createElement("img");
      img.src = e.target.result;

      const removeBtn = document.createElement("button");
      removeBtn.innerHTML = "×";
      removeBtn.classList.add("remove-img");
      removeBtn.onclick = () => {
        imgWrapper.remove();
        imageUpload.value = ""; // cho phép chọn lại ảnh khác
      };

      imgWrapper.appendChild(img);
      imgWrapper.appendChild(removeBtn);
      imagePreviewContainer.appendChild(imgWrapper);
    };
    reader.readAsDataURL(file);
  });
}

export function initSubmitPost(eventId) {
  const submitBtn = document.getElementById("submitCreatePost");
  const textarea = document.getElementById("createPostInput");
  const imageUpload = document.getElementById("imageUpload");
  const overlay = document.getElementById("createPostOverlay");

  submitBtn.addEventListener("click", async () => {
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

      // Nếu có ảnh thì upload lên Cloudinary trước
      if (file) {
        const formData = new FormData();
        formData.append("file", file);

        const uploadResponse = await fetch("http://localhost:8000/api/posts/upload-image", {
          method: "POST",
          body: formData,
        });

        if (!uploadResponse.ok) {
          throw new Error("Upload ảnh thất bại!");
        }

        const uploadData = await uploadResponse.json();
        console.log("uploadData:", uploadData); // xem key trả về
        imageUrl = uploadData.images_url;
        console.log("Ảnh đã upload lên Cloudinary:", imageUrl);
      }

      // Gửi post lên API backend
      const res = await fetch(`http://localhost:8000/api/posts/events/${eventId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // nhớ có biến token toàn cục hoặc import vào
        },
        body: JSON.stringify({
          content,
          images_url: imageUrl, // gửi link Cloudinary thay vì file
        }),
      });

      if (!res.ok) {
        const error = await res.json();
        console.error("Lỗi đăng bài:", error);
        showToast(`Đăng bài thất bại: ${error.detail || "Không rõ lỗi"}`, 4000, "#f44336");
        return;
      }

      const newPost = await res.json();
      console.log("Đăng bài thành công:", newPost);

      // Reset form
      textarea.value = "";
      imageUpload.value = "";
      document.getElementById("imagePreviewContainer").innerHTML = "";

      // Đóng overlay
      overlay.classList.add("hidden");

      // Gọi lại hàm load danh sách bài viết
      if (typeof loadPostsByEvent === "function") {
        await loadPostsByEvent(eventId);
      }

      showToast("Đăng bài thành công!", 3000, "#4CAF50");
    } catch (err) {
      console.error("Lỗi khi đăng bài:", err);
      showToast("Không thể kết nối đến server!", 4000, "#f44336");
    }
  });
}

export function showToast(message, duration = 3000, bgColor = "#333") {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.style.backgroundColor = bgColor;
  toast.textContent = message;
  document.body.appendChild(toast);

  // Hiển thị
  setTimeout(() => toast.classList.add("show"), 50);

  // Ẩn sau duration
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300); // remove sau animation
  }, duration);
}





const event_id = window.location.pathname.split("/").pop();
initPostsPage(event_id);
initCreatePostOverlay();
initInputPost();
initSubmitPost(event_id);

