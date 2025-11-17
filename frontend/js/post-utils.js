const reactions = {
  like: { img: "/assets/like.png", text: "Thích", color: "#1877f2" },
  love: { img: "/assets/love.png", text: "Yêu thích", color: "#f33e58" },
  haha: { img: "/assets/haha.png", text: "Haha", color: "#f7b125" },
  wow: { img: "/assets/wow.png", text: "Wow", color: "#f7b125" },
  sad: { img: "/assets/sad.png", text: "Buồn", color: "#f7b125" },
  angry: { img: "/assets/angry.png", text: "Phẫn nộ", color: "#e9710f" },
};

export function formatTimeAgo(createdAt) {
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

export function attachReactions(postElement) {
  const postId = postElement.dataset.postId;
  const likeBtn = postElement.querySelector(".like-btn");
  const reactionPopup = postElement.querySelector(".reaction-popup");
  const likeIcon = likeBtn.querySelector(".like-icon");
  const likeText = likeBtn.querySelector(".like-text");
  const reactCountSpan = postElement.querySelector(".react-count");

  let hideTimer;
  let isHoveringPopup = false;
  let currentReaction = postElement.dataset.userReact?.toLowerCase() || "default";

  // Nếu có overlay -> tìm post chính cùng post_id ở ngoài
  const mainPost =
    !postElement.closest("#overlayPostContent") // chỉ tìm nếu đang trong overlay
      ? null
      : document.querySelector(`.event-post[data-post-id="${postId}"]:not(#overlayPostContent .event-post)`);


  const reactions = {
    like: { img: "/assets/like.png", text: "Thích", color: "#1877f2" },
    love: { img: "/assets/love.png", text: "Yêu thích", color: "#f33e58" },
    haha: { img: "/assets/haha.png", text: "Haha", color: "#f7b125" },
    wow: { img: "/assets/wow.png", text: "Wow", color: "#f7b125" },
    sad: { img: "/assets/sad.png", text: "Buồn", color: "#f7b125" },
    angry: { img: "/assets/angry.png", text: "Phẫn nộ", color: "#e9710f" },
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
        updateReactionUI(type, success.react_count);
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
        updateReactionUI("like", success.react_count);
        currentReaction = "like";
      }
    } else {
      const success = await removeReaction(postId);
      if (success) {
        updateReactionUI("default", success.react_count);
        currentReaction = "default";
      }
    }
  });

  // === CẬP NHẬT COUNT ===
  function updateReactCountExact(newCount) {
    if (newCount <= 0) {
      reactCountSpan.style.display = "none";
      reactCountSpan.textContent = "";
    } else {
      reactCountSpan.style.display = "inline";
      reactCountSpan.textContent = newCount.toString();
    }
  }

  // === CẬP NHẬT GIAO DIỆN SAU KHI REACT ===
  function updateReactionUI(type, newCount) {
    if (type === "default") {
      likeIcon.src = "/assets/like-default.png";
      likeText.textContent = "Thích";
      likeText.style.color = "#65676b";
      likeBtn.classList.remove("active");
    } else {
      const reaction = reactions[type];
      likeIcon.src = reaction.img;
      likeText.textContent = reaction.text;
      likeText.style.color = reaction.color;
      likeBtn.classList.add("active");
    }
    updateReactCountExact(newCount);

    // Nếu đang trong overlay thì cập nhật post chính bên ngoài
    if (mainPost) {
      const mainLikeIcon = mainPost.querySelector(".like-icon");
      const mainLikeText = mainPost.querySelector(".like-text");
      const mainReactCount = mainPost.querySelector(".react-count");

      if (type === "default") {
        mainLikeIcon.src = "/assets/like-default.png";
        mainLikeText.textContent = "Thích";
        mainLikeText.style.color = "#65676b";
        mainLikeText.classList.remove("active");
      } else {
        const reaction = reactions[type];
        mainLikeIcon.src = reaction.img;
        mainLikeText.textContent = reaction.text;
        mainLikeText.style.color = reaction.color;
        mainLikeText.classList.add("active");
      }

      if (newCount <= 0) {
        mainReactCount.style.display = "none";
        mainReactCount.textContent = "";
      } else {
        mainReactCount.style.display = "inline";
        mainReactCount.textContent = newCount.toString();
      }
    }
  }
}

// =================== API CALLS ===================

export async function sendReaction(postId, category) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    console.error("Không có token hợp lệ. Người dùng chưa đăng nhập.");
    return null;
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
      return null;
    }
    // Trả về dữ liệu thật từ API
    const data = await res.json();
    return data; // có react_count
  } catch (err) {
    console.error("Không thể gửi cảm xúc:", err);
    return false;
  }
}

export async function removeReaction(postId) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");
  if (!token || !token_type) {
    console.error("Không có token hợp lệ. Người dùng chưa đăng nhập.");
    return null;
  }

  try {
    const res = await fetch(`http://localhost:8000/api/reacts/posts/${postId}`, {
      method: "DELETE",
      headers: { "Authorization": `${token_type} ${token}` },
    });
    if (!res.ok) {
      console.error("Lỗi bỏ cảm xúc:", await res.text());
      return null;
    }
    // Trả về dữ liệu có react_count
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Không thể bỏ cảm xúc:", err);
    return false;
  }
}