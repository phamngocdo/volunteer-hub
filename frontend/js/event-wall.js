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


async function loadPosts() {
  const container = document.querySelector("#all");

  try {
    const response = await fetch("../pages/event-post.html");
    let postHTML = await response.text();

    // 🔽 chỉ lấy phần bên trong <div class="event-post">...</div>
    const match = postHTML.match(/<div class="event-post">[\s\S]*<\/div>/);
    if (!match) throw new Error("Không tìm thấy khối event-post trong file HTML!");
    postHTML = match[0];


    const posts = [
      {
        name: "Nguyễn Minh Anh",
        time: "2 giờ trước",
        content: "🌿 Hôm nay nhóm mình vừa hoàn thành buổi dọn rác bãi biển Cửa Lò!",
        image: "../img_data/event1-img.jpg",
      },
      {
        name: "Lê Hồng Phúc",
        time: "5 giờ trước",
        content: "🌸 Tham gia chương trình trồng cây gây rừng thật ý nghĩa!",
        image: "../img_data/event2-img.jpg",
      },
      {
        name: "Trần Thị Mai",
        time: "Hôm qua",
        content: "💧 Ngày hội hiến máu diễn ra suôn sẻ, cảm ơn mọi người!",
        image: "../img_data/event3-img.jpg",
      },
    ];

    posts.forEach(post => {
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = postHTML.trim();
      const postElement = tempDiv.firstElementChild;

      postElement.querySelector(".post-info h4").textContent = post.name;
      postElement.querySelector(".post-info p").textContent = post.time;
      postElement.querySelector(".event-content").textContent = post.content;
      postElement.querySelector(".event-img").src = post.image;

      container.appendChild(postElement);
      // Gắn logic cảm xúc cho từng post
      attachReactions(postElement);
    });
  } catch (error) {
    console.error("Không thể tải event-post.html:", error);
  }
}

loadPosts();

function attachReactions(postElement) {
  // ====== CẢM XÚC (REACTION) ======
  const likeBtn = postElement.querySelector(".like-btn");
  const reactionPopup = postElement.querySelector(".reaction-popup");
  const likeIcon = likeBtn.querySelector(".like-icon");
  const likeText = likeBtn.querySelector(".like-text");

  let hideTimer;
  let isHoveringPopup = false;
  let currentReaction = "default";

  const reactions = {
    like: { img: "../img_data/like.png", text: "Thích", color: "#1877f2" },
    love: { img: "../img_data/love.png", text: "Yêu thích", color: "#f33e58" },
    haha: { img: "../img_data/haha.png", text: "Haha", color: "#f7b125" },
    wow: { img: "../img_data/wow.png", text: "Wow", color: "#f7b125" },
    sad: { img: "../img_data/sad.png", text: "Buồn", color: "#f7b125" },
    angry: { img: "../img_data/angry.png", text: "Phẫn nộ", color: "#e9710f" },
  };

  // === HIỂN POPUP ===
  likeBtn.addEventListener("mouseenter", () => {
    clearTimeout(hideTimer);
    reactionPopup.classList.add("show");
  });

  // === ẨN POPUP SAU 1 GIÂY NẾU KHÔNG HOVER ===
  likeBtn.addEventListener("mouseleave", () => {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      if (!isHoveringPopup) {
        reactionPopup.classList.remove("show");
      }
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

  // === XỬ LÝ CHỌN CẢM XÚC ===
  const reactionImages = postElement.querySelectorAll(".reaction-popup img");
  const reactionTypes = ["like", "love", "haha", "wow", "sad", "angry"];

  reactionImages.forEach((img, i) => {
    img.dataset.type = reactionTypes[i];
    img.addEventListener("click", () => {
      const type = img.dataset.type;
      const reaction = reactions[type];

      likeIcon.src = reaction.img;
      likeText.textContent = reaction.text;
      likeText.style.color = reaction.color;
      currentReaction = type;

      reactionPopup.classList.remove("show");
    });
  });

  // Khi click vào nút Like
  likeBtn.addEventListener("click", () => {
    if (currentReaction === "default") {
      // Đổi thành "đã thích"
      likeIcon.src = "../img_data/like.png";
      likeText.textContent = "Thích";
      likeText.style.color = "#1877f2";
      currentReaction = "like";
    } else {
      // Quay về mặc định
      likeIcon.src = "../img_data/like-default.png";
      likeText.textContent = "Thích";
      likeText.style.color = "#65676b";
      currentReaction = "default";
    }
  });
}

// Gắn sự kiện click cho các nút "Bình luận"
document.addEventListener("click", function (e) {
  if (e.target.closest(".comment-btn")) {
    const btn = e.target.closest(".comment-btn");
    const post = btn.closest(".event-post");
    let commentSection = post.querySelector(".comments-section");

    // Nếu chưa có thì tạo mới
    if (!commentSection) {
      commentSection = document.createElement("div");
      commentSection.classList.add("comments-section");
      commentSection.innerHTML = `
          <div class="comment-item">
            <img src="../assets/default-avatar.png" class="avatar-sm" alt="user" />
            <div class="comment-content">
              <p><strong>Trần Đức</strong> Tuyệt vời quá! ❤️</p>
            </div>
          </div>

          <div class="comment-form">
            <input type="text" placeholder="Viết bình luận..." class="comment-input" />
            <button class="send-comment-btn">Gửi</button>
          </div>
        `;
      post.appendChild(commentSection);
    }

    // Ẩn/hiện phần bình luận
    commentSection.classList.toggle("show");
  }

  // Gửi bình luận mới
  if (e.target.classList.contains("send-comment-btn")) {
    const form = e.target.closest(".comment-form");
    const input = form.querySelector(".comment-input");
    const text = input.value.trim();
    if (text) {
      const newComment = document.createElement("div");
      newComment.classList.add("comment-item");
      newComment.innerHTML = `
          <img src="../assets/default-avatar.png" class="avatar-sm" alt="user" />
          <div class="comment-content">
            <p><strong>Bạn</strong> ${text}</p>
          </div>
        `;
      form.before(newComment);
      input.value = "";
    }
  }
});