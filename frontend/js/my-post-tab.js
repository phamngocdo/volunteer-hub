import { formatTimeAgo, attachReactions } from "./post-utils.js";

export async function fetchMyPosts() {
  const container = document.getElementById("my-post");
  if (!container) return;

  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch(`http://localhost:8000/api/posts/users/me`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `${token_type} ${token}`,
      },
    });

    if (!res.ok) throw new Error(await res.text());
    const allPosts = await res.json();
    renderPosts(allPosts);
  } catch (err) {
    console.error("Không thể tải bài viết của tôi:", err);
    container.innerHTML = `<p>Không thể tải bài viết của bạn.</p>`;
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
}
