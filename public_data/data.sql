-- XÓA BẢNG NẾU ĐÃ TỒN TẠI (THEO THỨ TỰ PHỤ THUỘC)
DROP TABLE IF EXISTS "notifications" CASCADE;
DROP TABLE IF EXISTS "reacts" CASCADE;
DROP TABLE IF EXISTS "comments" CASCADE;
DROP TABLE IF EXISTS "posts" CASCADE;
DROP TABLE IF EXISTS "event_registrations" CASCADE;
DROP TABLE IF EXISTS "events" CASCADE;
DROP TABLE IF EXISTS "users" CASCADE;

-- ================= USERS =================
CREATE TABLE "users" (
  "user_id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(100),
  "last_name" VARCHAR(100),
  "email" VARCHAR(100) UNIQUE NOT NULL,
  "password" TEXT NOT NULL,
  "phone_number" VARCHAR(100),
  "role" VARCHAR(20),
  "status" VARCHAR(20),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= EVENTS =================
CREATE TABLE "events" (
  "event_id" SERIAL PRIMARY KEY,
  "manager_id" INT,
  "title" VARCHAR(200),
  "image_url" VARCHAR(200),
  "description" TEXT,
  "category" VARCHAR(100),
  "location" VARCHAR(200),
  "start_date" DATE,
  "end_date" DATE,
  "status" VARCHAR(20),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= EVENT_REGISTRATIONS =================
CREATE TABLE "event_registrations" (
  "registration_id" SERIAL PRIMARY KEY,
  "event_id" INT,
  "user_id" INT,
  "status" VARCHAR(20),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= POSTS =================
CREATE TABLE "posts" (
  "post_id" SERIAL PRIMARY KEY,
  "event_id" INT,
  "user_id" INT,
  "images_url" VARCHAR(200),
  "content" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= COMMENTS =================
CREATE TABLE "comments" (
  "comment_id" SERIAL PRIMARY KEY,
  "post_id" INT,
  "user_id" INT,
  "content" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= REACTS =================
CREATE TABLE "reacts" (
  "like_id" SERIAL PRIMARY KEY,
  "post_id" INT,
  "user_id" INT,
  "category" VARCHAR(100),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= NOTIFICATIONS =================
CREATE TABLE "notifications" (
  "notification_id" SERIAL PRIMARY KEY,
  "user_id" INT,
  "event_id" INT,
  "message" TEXT,
  "is_read" BOOLEAN DEFAULT false,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

-- ================= INDEXES =================
CREATE UNIQUE INDEX ON "event_registrations" ("event_id", "user_id");
CREATE UNIQUE INDEX ON "reacts" ("post_id", "user_id");

-- ================= COMMENTS =================
COMMENT ON COLUMN "users"."role" IS 'volunteer | manager | admin';
COMMENT ON COLUMN "users"."status" IS 'active | banned | pending';
COMMENT ON COLUMN "events"."status" IS 'pending | approved | rejected | completed';
COMMENT ON COLUMN "event_registrations"."status" IS 'pending | approved | rejected | cancelled | completed';
COMMENT ON COLUMN "reacts"."category" IS 'like | ...';

-- ================= FOREIGN KEYS =================
ALTER TABLE "events" ADD FOREIGN KEY ("manager_id") REFERENCES "users" ("user_id");
ALTER TABLE "event_registrations" ADD FOREIGN KEY ("event_id") REFERENCES "events" ("event_id");
ALTER TABLE "event_registrations" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
ALTER TABLE "posts" ADD FOREIGN KEY ("event_id") REFERENCES "events" ("event_id");
ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
ALTER TABLE "comments" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");
ALTER TABLE "comments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
ALTER TABLE "reacts" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");
ALTER TABLE "reacts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
ALTER TABLE "notifications" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");
ALTER TABLE "notifications" ADD FOREIGN KEY ("event_id") REFERENCES "events" ("event_id");

-- ================= SAMPLE DATA =================
INSERT INTO users (first_name, last_name, email, password, phone_number, role, status)
VALUES 
('Duy', 'Nguyen', 'duy@gmail.com', '123456', '0123456789', 'volunteer', 'pending'),
('Do', 'Pham', 'do@gmail.com', '123456', '0987654321', 'admin', 'active'),
('Minh', 'Doan', 'minh@gmail.com', '123456', '0112233445', 'volunteer', 'pending'),
('Trang', 'Le', 'trang@gmail.com', '123456', '0998877665', 'manager', 'active'),
('Tuan', 'Pham', 'tuan@gmail.com', '123456', '0909090909', 'volunteer', 'banned');

INSERT INTO events (manager_id, title, image_url, description, category, location, start_date, end_date, status)
VALUES
(4, 'Dọn rác bãi biển Đà Nẵng', 'https://example.com/beach.jpg', 'Cùng nhau làm sạch bãi biển Mỹ Khê.', 'Môi trường', 'Đà Nẵng', '2025-11-10', '2025-11-11', 'approved'),
(4, 'Trồng cây tại công viên Thống Nhất', 'https://example.com/trees.jpg', 'Sự kiện trồng 500 cây xanh.', 'Môi trường', 'Hà Nội', '2025-11-15', '2025-11-15', 'pending'),
(4, 'Hiến máu nhân đạo', 'https://example.com/blood.jpg', 'Chương trình hiến máu cứu người.', 'Sức khỏe', 'TP. HCM', '2025-12-01', '2025-12-02', 'approved'),
(4, 'Chạy bộ gây quỹ', 'https://example.com/run.jpg', 'Chạy bộ 5km gây quỹ ủng hộ trẻ em nghèo.', 'Từ thiện', 'Huế', '2025-12-10', '2025-12-10', 'completed'),
(4, 'Phát cơm miễn phí', 'https://example.com/food.jpg', 'Phát cơm từ thiện tại bệnh viện.', 'Từ thiện', 'Hà Nội', '2025-11-20', '2025-11-20', 'pending');

INSERT INTO event_registrations (event_id, user_id, status)
VALUES
(1, 1, 'approved'),
(1, 3, 'approved'),
(2, 1, 'pending'),
(3, 5, 'cancelled'),
(4, 1, 'completed');

INSERT INTO posts (event_id, user_id, images_url, content)
VALUES
(1, 1, 'https://example.com/post1.jpg', 'Buổi dọn rác hôm nay thật ý nghĩa!'),
(1, 3, 'https://example.com/post2.jpg', 'Mọi người rất nhiệt tình và vui vẻ.'),
(3, 5, 'https://example.com/post3.jpg', 'Hiến máu cứu người – một hành động nhỏ, ý nghĩa lớn.'),
(4, 1, 'https://example.com/post4.jpg', 'Chạy bộ 5km cùng bạn bè thật tuyệt!'),
(2, 3, 'https://example.com/post5.jpg', 'Mong chờ ngày trồng cây sắp tới!');

INSERT INTO comments (post_id , user_id , content)
VALUES
(1, 2, 'Tốt lắm, cảm ơn bạn đã tham gia!'),
(1, 3, 'Mình cũng ở đó, rất vui!'),
(3, 4, 'Một nghĩa cử thật cao đẹp.'),
(4, 2, 'Sự kiện thật thành công!'),
(5, 5, 'Mong được gặp mọi người ở sự kiện tới!');

INSERT INTO reacts (post_id, user_id, category)
VALUES
(1, 2, 'like'),
(1, 3, 'love'),
(3, 1, 'wow'),
(4, 2, 'haha'),
(5, 5, 'like');

INSERT INTO notifications (user_id, event_id, message, is_read)
VALUES
(1, 1, 'Sự kiện "Dọn rác bãi biển Đà Nẵng" đã được phê duyệt.', false),
(3, 2, 'Bạn đã đăng ký sự kiện "Trồng cây tại công viên Thống Nhất".', true),
(5, 3, 'Trạng thái sự kiện "Hiến máu nhân đạo" đã thay đổi.', false),
(1, 4, 'Sự kiện "Chạy bộ gây quỹ" đã hoàn thành.', true),
(3, 5, 'Bạn có thông báo mới từ quản lý sự kiện.', false);