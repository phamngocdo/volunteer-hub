--
-- PostgreSQL database dump
--

\restrict N9WusYE2Kw60OhG7biR0PLFbV0aKhfO8z58I7e0VVWjCIXx00o1JKyoRSYvUfnP

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

ALTER TABLE IF EXISTS ONLY public.reacts DROP CONSTRAINT IF EXISTS reacts_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.reacts DROP CONSTRAINT IF EXISTS reacts_post_id_fkey;
ALTER TABLE IF EXISTS ONLY public.posts DROP CONSTRAINT IF EXISTS posts_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.posts DROP CONSTRAINT IF EXISTS posts_event_id_fkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_event_id_fkey;
ALTER TABLE IF EXISTS ONLY public.push_subscriptions DROP CONSTRAINT IF EXISTS fk_user_id;
ALTER TABLE IF EXISTS ONLY public.events DROP CONSTRAINT IF EXISTS events_manager_id_fkey;
ALTER TABLE IF EXISTS ONLY public.event_registrations DROP CONSTRAINT IF EXISTS event_registrations_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.event_registrations DROP CONSTRAINT IF EXISTS event_registrations_event_id_fkey;
ALTER TABLE IF EXISTS ONLY public.comments DROP CONSTRAINT IF EXISTS comments_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.comments DROP CONSTRAINT IF EXISTS comments_post_id_fkey;
DROP INDEX IF EXISTS public.reacts_post_id_user_id_idx;
DROP INDEX IF EXISTS public.push_subscriptions_user_id_endpoint_idx;
DROP INDEX IF EXISTS public.event_registrations_event_id_user_id_idx;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.reacts DROP CONSTRAINT IF EXISTS reacts_pkey;
ALTER TABLE IF EXISTS ONLY public.push_subscriptions DROP CONSTRAINT IF EXISTS push_subscriptions_pkey;
ALTER TABLE IF EXISTS ONLY public.posts DROP CONSTRAINT IF EXISTS posts_pkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_pkey;
ALTER TABLE IF EXISTS ONLY public.events DROP CONSTRAINT IF EXISTS events_pkey;
ALTER TABLE IF EXISTS ONLY public.event_registrations DROP CONSTRAINT IF EXISTS event_registrations_pkey;
ALTER TABLE IF EXISTS ONLY public.comments DROP CONSTRAINT IF EXISTS comments_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.reacts ALTER COLUMN react_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.push_subscriptions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.posts ALTER COLUMN post_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.notifications ALTER COLUMN notification_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.events ALTER COLUMN event_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.event_registrations ALTER COLUMN registration_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.comments ALTER COLUMN comment_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_user_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.reacts_like_id_seq;
DROP TABLE IF EXISTS public.reacts;
DROP SEQUENCE IF EXISTS public.push_subscriptions_id_seq;
DROP TABLE IF EXISTS public.push_subscriptions;
DROP SEQUENCE IF EXISTS public.posts_post_id_seq;
DROP TABLE IF EXISTS public.posts;
DROP SEQUENCE IF EXISTS public.notifications_notification_id_seq;
DROP TABLE IF EXISTS public.notifications;
DROP SEQUENCE IF EXISTS public.events_event_id_seq;
DROP TABLE IF EXISTS public.events;
DROP SEQUENCE IF EXISTS public.event_registrations_registration_id_seq;
DROP TABLE IF EXISTS public.event_registrations;
DROP SEQUENCE IF EXISTS public.comments_comment_id_seq;
DROP TABLE IF EXISTS public.comments;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer,
    user_id integer,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: event_registrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_registrations (
    registration_id integer NOT NULL,
    event_id integer,
    user_id integer,
    status character varying(20),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: COLUMN event_registrations.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.event_registrations.status IS 'pending | approved | rejected | cancelled | completed';


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.event_registrations_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.event_registrations_registration_id_seq OWNED BY public.event_registrations.registration_id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    event_id integer NOT NULL,
    manager_id integer,
    title character varying(200),
    image_url character varying(200),
    description text,
    category character varying(100),
    location character varying(200),
    start_date date,
    end_date date,
    status character varying(20),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: COLUMN events.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.events.status IS 'pending | approved | rejected | completed';


--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    notification_id integer NOT NULL,
    user_id integer,
    event_id integer,
    message text,
    is_read boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.posts (
    post_id integer NOT NULL,
    event_id integer,
    user_id integer,
    images_url character varying(200),
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: push_subscriptions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.push_subscriptions (
    id integer NOT NULL,
    user_id integer,
    endpoint text NOT NULL,
    p256dh text NOT NULL,
    auth text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: COLUMN push_subscriptions.endpoint; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.push_subscriptions.endpoint IS 'Web Push subscription endpoint for user';


--
-- Name: COLUMN push_subscriptions.p256dh; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.push_subscriptions.p256dh IS 'Web Push p256dh key';


--
-- Name: COLUMN push_subscriptions.auth; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.push_subscriptions.auth IS 'Web Push auth key';


--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.push_subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.push_subscriptions_id_seq OWNED BY public.push_subscriptions.id;


--
-- Name: reacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reacts (
    react_id integer CONSTRAINT reacts_like_id_not_null NOT NULL,
    post_id integer,
    user_id integer,
    category character varying(100),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: COLUMN reacts.category; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.reacts.category IS 'like | ...';


--
-- Name: reacts_like_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reacts_like_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reacts_like_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reacts_like_id_seq OWNED BY public.reacts.react_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    email character varying(100) NOT NULL,
    password text NOT NULL,
    phone_number character varying(100),
    role character varying(20),
    status character varying(20),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    avatar_url character varying(200)
);


--
-- Name: COLUMN users.role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.role IS 'volunteer | manager | admin';


--
-- Name: COLUMN users.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.status IS 'active | banned | pending';


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: event_registrations registration_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_registrations ALTER COLUMN registration_id SET DEFAULT nextval('public.event_registrations_registration_id_seq'::regclass);


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: notifications notification_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);


--
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: push_subscriptions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_subscriptions ALTER COLUMN id SET DEFAULT nextval('public.push_subscriptions_id_seq'::regclass);


--
-- Name: reacts react_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reacts ALTER COLUMN react_id SET DEFAULT nextval('public.reacts_like_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.comments (comment_id, post_id, user_id, content, created_at, updated_at) FROM stdin;
9	9	21	Tự hào vì đã góp phần làm nên bữa cơm!	2025-12-21 13:26:52.004086	2025-12-21 13:26:52.004086
10	11	19	Quá nhiều lợi ích luôn đó chứ	2025-12-21 13:32:53.39056	2025-12-21 13:32:53.39056
\.


--
-- Data for Name: event_registrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.event_registrations (registration_id, event_id, user_id, status, created_at, updated_at) FROM stdin;
15	6	20	approved	2025-12-20 14:58:27.179099	2025-12-20 15:11:29.156002
16	10	21	approved	2025-12-21 13:26:15.024357	2025-12-21 13:26:25.152937
17	10	23	approved	2025-12-21 13:29:06.699212	2025-12-21 13:29:12.57204
18	7	23	approved	2025-12-21 13:31:19.967398	2025-12-21 13:31:26.416998
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.events (event_id, manager_id, title, image_url, description, category, location, start_date, end_date, status, created_at, updated_at) FROM stdin;
6	19	Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch	public/events/e0fc3d3b-06f4-4c29-82a2-40783f894f0d.png	Sự kiện “Ngày Chủ Nhật Xanh” được tổ chức nhằm nâng cao ý thức bảo vệ môi trường trong cộng đồng, đặc biệt là giới trẻ. Người tham gia sẽ cùng nhau dọn dẹp rác thải tại các khu dân cư, công viên và tuyến đường công cộng. Ngoài hoạt động thu gom rác, chương trình còn có các buổi chia sẻ về phân loại rác, tái chế và lối sống xanh. Sự kiện hướng tới việc xây dựng thói quen sống thân thiện với môi trường và lan tỏa tinh thần trách nhiệm xã hội.	Môi trường	Dịch Vọng Hậu, Hà Nội	2025-12-20	2025-12-21	completed	2025-12-20 14:51:31.215938	2025-12-20 14:52:21.830114
9	19	Green Campus Day – Trồng 1.000 cây xanh cho tương lai	public/events/4a862da2-8471-4ffb-bb43-b050d51f0021.png	Green Campus Day – Trồng 1.000 cây xanh cho tương lai là sự kiện môi trường nhằm cải thiện cảnh quan và nâng cao ý thức bảo vệ môi trường trong cộng đồng sinh viên. Sự kiện huy động đông đảo sinh viên và cán bộ tham gia trồng cây tại khuôn viên trường và các khu vực lân cận. Thông qua hoạt động này, chương trình hướng đến việc lan tỏa lối sống xanh, giảm thiểu tác động tiêu cực đến môi trường và góp phần xây dựng không gian học tập xanh – sạch – đẹp.	Môi trường	Thành Phố Hồ Chí Minh	2025-12-22	2025-12-23	approved	2025-12-21 13:10:49.229641	2025-12-21 13:12:54.138752
7	19	Ngày hội Hiến máu Nhân đạo	public/events/d3d97114-98ca-4ae0-81cf-3167f37ebeb4.jpg	Ngày hội Hiến máu Nhân đạo được tổ chức nhằm lan tỏa tinh thần nhân ái và trách nhiệm cộng đồng thông qua hành động hiến máu cứu người. Sự kiện thu hút sự tham gia của đông đảo sinh viên, cán bộ giảng viên và người dân địa phương, góp phần bổ sung nguồn máu dự trữ phục vụ công tác cấp cứu và điều trị tại các bệnh viện. Bên cạnh hoạt động hiến máu, chương trình còn có các khu vực tư vấn sức khỏe, hướng dẫn chăm sóc sau hiến máu, cũng như các hoạt động giao lưu, chia sẻ nhằm nâng cao nhận thức về tầm quan trọng của hiến máu tình nguyện. Ngày hội không chỉ mang ý nghĩa nhân đạo sâu sắc mà còn góp phần xây dựng lối sống tích cực, biết sẻ chia trong cộng đồng.	Từ thiện	Bệnh viện Chấn thương Chỉnh hình Tp HCM	2025-12-22	2025-12-23	approved	2025-12-21 13:03:12.064723	2025-12-21 13:03:42.7515
10	19	Bữa Cơm 0 Đồng – San sẻ yêu thương	public/events/71808df6-a584-4523-a157-620e1381a42e.png	Bữa Cơm 0 Đồng – San sẻ yêu thương là hoạt động từ thiện hướng đến người lao động nghèo, người vô gia cư và bệnh nhân có hoàn cảnh khó khăn. Các suất ăn miễn phí được chuẩn bị và phát tận tay người cần hỗ trợ, đảm bảo vệ sinh và dinh dưỡng. Chương trình thể hiện tinh thần nhân ái, sự sẻ chia và trách nhiệm xã hội của cộng đồng đối với những hoàn cảnh kém may mắn.	Từ thiện	Hà Nội	2025-12-22	2026-02-01	approved	2025-12-21 13:21:05.986199	2025-12-21 13:21:23.465889
8	19	Chương trình Thiện nguyện “Áo ấm cho em”	public/events/dfda3949-9f32-4ab2-8fda-41568573b9d4.jpg	Chương trình Thiện nguyện “Áo ấm mùa đông” hướng đến việc hỗ trợ trẻ em và người dân có hoàn cảnh khó khăn tại các vùng cao, vùng sâu, vùng xa trong mùa đông giá rét. Thông qua việc quyên góp quần áo, chăn ấm, sách vở và các nhu yếu phẩm cần thiết, chương trình mong muốn mang lại sự ấm áp cả về vật chất lẫn tinh thần cho những hoàn cảnh kém may mắn. Bên cạnh hoạt động trao quà, các tình nguyện viên còn tổ chức giao lưu, sinh hoạt tập thể và các trò chơi dành cho trẻ em, góp phần mang đến niềm vui và động lực để các em tiếp tục vươn lên trong học tập và cuộc sống.	Từ thiện	Đồng Nai	2025-12-22	2026-02-01	approved	2025-12-21 13:07:23.20372	2025-12-21 13:14:20.41957
11	19	STEM for Kids – Khám phá khoa học cùng học sinh tiểu học	public/events/ee8bb200-207a-418d-89a5-46e17b93808b.jpg	STEM for Kids – Khám phá khoa học cùng học sinh tiểu học là chương trình giáo dục trải nghiệm, giúp học sinh làm quen với khoa học, công nghệ, kỹ thuật và toán học thông qua các hoạt động thực hành. Các mô hình thí nghiệm, trò chơi khoa học và bài học tương tác được thiết kế phù hợp với lứa tuổi, tạo hứng thú học tập và khơi dậy niềm đam mê khám phá khoa học từ sớm.	Giáo dục	Huế	2025-12-22	2026-02-01	approved	2025-12-21 13:23:25.808253	2025-12-21 13:23:36.16486
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (notification_id, user_id, event_id, message, is_read, created_at, updated_at) FROM stdin;
33	20	6	Đơn đăng ký tham gia sự kiện 'Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch' của bạn đã được duyệt.	f	2025-12-20 15:11:29.170828	2025-12-20 15:11:29.170828
34	19	7	Sự kiện Ngày hội Hiến máu Nhân đạo được duyệt thành công	t	2025-12-21 13:03:42.762982	2025-12-21 13:13:21.960239
35	19	9	Sự kiện Green Campus Day – Trồng 1.000 cây xanh cho tương lai được duyệt thành công	t	2025-12-21 13:12:54.140718	2025-12-21 13:13:21.960239
36	19	8	Sự kiện Chương trình Thiện nguyện “Áo ấm mùa đông” được duyệt thành công	t	2025-12-21 13:12:55.901099	2025-12-21 13:13:21.960239
37	19	10	Sự kiện Bữa Cơm 0 Đồng – San sẻ yêu thương được duyệt thành công	t	2025-12-21 13:21:23.4767	2025-12-21 13:21:48.763049
39	21	10	Đơn đăng ký tham gia sự kiện 'Bữa Cơm 0 Đồng – San sẻ yêu thương' của bạn đã được duyệt.	t	2025-12-21 13:26:25.162339	2025-12-21 13:28:19.726266
40	23	10	Đơn đăng ký tham gia sự kiện 'Bữa Cơm 0 Đồng – San sẻ yêu thương' của bạn đã được duyệt.	t	2025-12-21 13:29:12.579161	2025-12-21 13:31:11.783293
41	23	7	Đơn đăng ký tham gia sự kiện 'Ngày hội Hiến máu Nhân đạo' của bạn đã được duyệt.	f	2025-12-21 13:31:26.427066	2025-12-21 13:31:26.427066
38	19	11	Sự kiện STEM for Kids – Khám phá khoa học cùng học sinh tiểu học được duyệt thành công	t	2025-12-21 13:23:36.175704	2025-12-21 13:32:59.578515
27	22	\N	Bạn đã bị khóa tài khoản.	f	2025-12-20 14:41:37.75911	2025-12-20 14:41:37.75911
28	19	6	Sự kiện Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch được duyệt thành công	t	2025-12-20 14:52:21.84155	2025-12-20 14:52:34.405598
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.posts (post_id, event_id, user_id, images_url, content, created_at, updated_at) FROM stdin;
9	10	19	public/posts/6e7b8d88-452c-4f7a-a53c-b3c7d736efe1.jpg	Cơm làm ngon quá cả nhà ơi :v	2025-12-21 13:25:34.412767	2025-12-21 13:25:34.412767
10	10	23	\N	Nay hơi mỏi nhưng cũng đáng đó.	2025-12-21 13:30:44.187831	2025-12-21 13:30:44.187831
11	7	23	public/posts/eda95a22-3d0a-4ac9-b856-c59c42f486f7.jpg	Lợi ích nè cả nhà. Hãy rủ thêm người thân nhá :v	2025-12-21 13:32:31.433626	2025-12-21 13:32:31.433626
\.


--
-- Data for Name: push_subscriptions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.push_subscriptions (id, user_id, endpoint, p256dh, auth, created_at, updated_at) FROM stdin;
14	18	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:41:20.802212	2025-12-20 14:41:20.802212
15	19	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:41:55.822696	2025-12-20 14:41:55.822696
16	20	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:58:25.320116	2025-12-20 14:58:25.320116
\.


--
-- Data for Name: reacts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reacts (react_id, post_id, user_id, category, created_at, updated_at) FROM stdin;
11	9	21	haha	2025-12-21 13:26:32.107217	2025-12-21 13:26:32.107217
12	9	23	love	2025-12-21 13:30:10.84057	2025-12-21 13:30:10.84057
13	11	19	haha	2025-12-21 13:32:41.342925	2025-12-21 13:32:41.342925
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, first_name, last_name, email, password, phone_number, role, status, created_at, updated_at, avatar_url) FROM stdin;
20	Phạm	Ngọc Đô	phamdo@gmail.com	$2b$12$Gx1Z0rXee5SbJJtHwhhL9OkcYQZD5Af/rt/hBf2HVs2hrMLbmsqBy	0969670190	volunteer	active	2025-12-20 14:33:08.418165	2025-12-20 14:33:08.418165	\N
18	Phạm	Đô	admin@gmail.com	$2b$12$FDVlNuuH5zb/TPjqgfkm7e9PpOj8Nu3GWcND6rJV/eFT1rZq/3nHK	0906212132	admin	active	2025-12-20 14:29:40.979365	2025-12-20 14:29:40.979365	\N
23	Cường	Nguyễn	ngcuong@gmail.com	$2b$12$1SZIpJZJKVpZICGOnaM/J.SZri9QJsgzGECFjG9ZQKiueVwW3XdA6	0954363598	volunteer	active	2025-12-20 14:41:03.382111	2025-12-20 14:41:03.382111	\N
22	Doãn	Minh	ddminh@gmail.com	$2b$12$VeOubMxAmVoHNeyOImRKTuCgIAYk.T./lt.WKwW4R66n3F6RMQeUS	0936463953	volunteer	banned	2025-12-20 14:40:01.491753	2025-12-20 14:41:37.747149	\N
21	Nguyễn Quang	Duy	duyquang@gmail.com	$2b$12$6RqPjBzqH6MEMI7CSfMU2uVPtEgdhP/pXH8O4q3/2wtDLcAcFplvu	0923465569	volunteer	active	2025-12-20 14:39:30.073403	2025-12-21 13:28:14.464365	public/users/117012b4-d908-4802-b7b7-cd5b9b40ccd7.jpeg
19	Phạm	Cương	manager@gmail.com	$2b$12$C8FTou61HyXeBtxO2F5OBusxqIjGSJyJSWQ6a8c9U1nUYlLfAh7FC	0961611349	manager	active	2025-12-20 14:30:31.244241	2025-12-21 13:34:13.061621	public/users/787d73c9-8482-439e-a612-9c6ba94171ed.jpg
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 10, true);


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.event_registrations_registration_id_seq', 18, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.events_event_id_seq', 11, true);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notifications_notification_id_seq', 41, true);


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 11, true);


--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.push_subscriptions_id_seq', 16, true);


--
-- Name: reacts_like_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reacts_like_id_seq', 13, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 23, true);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: event_registrations event_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_pkey PRIMARY KEY (registration_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: push_subscriptions push_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_subscriptions
    ADD CONSTRAINT push_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: reacts reacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_pkey PRIMARY KEY (react_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: event_registrations_event_id_user_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX event_registrations_event_id_user_id_idx ON public.event_registrations USING btree (event_id, user_id);


--
-- Name: push_subscriptions_user_id_endpoint_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX push_subscriptions_user_id_endpoint_idx ON public.push_subscriptions USING btree (user_id, endpoint);


--
-- Name: reacts_post_id_user_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX reacts_post_id_user_id_idx ON public.reacts USING btree (post_id, user_id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: event_registrations event_registrations_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: event_registrations event_registrations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: events events_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.users(user_id);


--
-- Name: push_subscriptions fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_subscriptions
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: notifications notifications_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: posts posts_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reacts reacts_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: reacts reacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

\unrestrict N9WusYE2Kw60OhG7biR0PLFbV0aKhfO8z58I7e0VVWjCIXx00o1JKyoRSYvUfnP

