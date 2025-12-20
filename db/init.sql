--
-- PostgreSQL database dump
--

\restrict kgFI4sSvMviHfyf37GdWY37aOrhv76QbG1JgXGA5OQdfcwN9Q0ThHRCqJdLfIPV

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: phamngocdo
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer,
    user_id integer,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.comments OWNER TO phamngocdo;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_comment_id_seq OWNER TO phamngocdo;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: event_registrations; Type: TABLE; Schema: public; Owner: phamngocdo
--

CREATE TABLE public.event_registrations (
    registration_id integer NOT NULL,
    event_id integer,
    user_id integer,
    status character varying(20),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.event_registrations OWNER TO phamngocdo;

--
-- Name: COLUMN event_registrations.status; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.event_registrations.status IS 'pending | approved | rejected | cancelled | completed';


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.event_registrations_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_registrations_registration_id_seq OWNER TO phamngocdo;

--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.event_registrations_registration_id_seq OWNED BY public.event_registrations.registration_id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: phamngocdo
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


ALTER TABLE public.events OWNER TO phamngocdo;

--
-- Name: COLUMN events.status; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.events.status IS 'pending | approved | rejected | completed';


--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_event_id_seq OWNER TO phamngocdo;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: phamngocdo
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


ALTER TABLE public.notifications OWNER TO phamngocdo;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_notification_id_seq OWNER TO phamngocdo;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: phamngocdo
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


ALTER TABLE public.posts OWNER TO phamngocdo;

--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_post_id_seq OWNER TO phamngocdo;

--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: push_subscriptions; Type: TABLE; Schema: public; Owner: phamngocdo
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


ALTER TABLE public.push_subscriptions OWNER TO phamngocdo;

--
-- Name: COLUMN push_subscriptions.endpoint; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.push_subscriptions.endpoint IS 'Web Push subscription endpoint for user';


--
-- Name: COLUMN push_subscriptions.p256dh; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.push_subscriptions.p256dh IS 'Web Push p256dh key';


--
-- Name: COLUMN push_subscriptions.auth; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.push_subscriptions.auth IS 'Web Push auth key';


--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.push_subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.push_subscriptions_id_seq OWNER TO phamngocdo;

--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.push_subscriptions_id_seq OWNED BY public.push_subscriptions.id;


--
-- Name: reacts; Type: TABLE; Schema: public; Owner: phamngocdo
--

CREATE TABLE public.reacts (
    react_id integer CONSTRAINT reacts_like_id_not_null NOT NULL,
    post_id integer,
    user_id integer,
    category character varying(100),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.reacts OWNER TO phamngocdo;

--
-- Name: COLUMN reacts.category; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.reacts.category IS 'like | ...';


--
-- Name: reacts_like_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.reacts_like_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reacts_like_id_seq OWNER TO phamngocdo;

--
-- Name: reacts_like_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.reacts_like_id_seq OWNED BY public.reacts.react_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: phamngocdo
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


ALTER TABLE public.users OWNER TO phamngocdo;

--
-- Name: COLUMN users.role; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.users.role IS 'volunteer | manager | admin';


--
-- Name: COLUMN users.status; Type: COMMENT; Schema: public; Owner: phamngocdo
--

COMMENT ON COLUMN public.users.status IS 'active | banned | pending';


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: phamngocdo
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO phamngocdo;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phamngocdo
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: event_registrations registration_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.event_registrations ALTER COLUMN registration_id SET DEFAULT nextval('public.event_registrations_registration_id_seq'::regclass);


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: notifications notification_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);


--
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: push_subscriptions id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.push_subscriptions ALTER COLUMN id SET DEFAULT nextval('public.push_subscriptions_id_seq'::regclass);


--
-- Name: reacts react_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.reacts ALTER COLUMN react_id SET DEFAULT nextval('public.reacts_like_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.comments (comment_id, post_id, user_id, content, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event_registrations; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.event_registrations (registration_id, event_id, user_id, status, created_at, updated_at) FROM stdin;
15	6	20	approved	2025-12-20 14:58:27.179099	2025-12-20 15:11:29.156002
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.events (event_id, manager_id, title, image_url, description, category, location, start_date, end_date, status, created_at, updated_at) FROM stdin;
6	19	Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch	public/events/9d7b8687-8835-4090-ad91-1da6a7595be7.png	Sự kiện “Ngày Chủ Nhật Xanh” được tổ chức nhằm nâng cao ý thức bảo vệ môi trường trong cộng đồng, đặc biệt là giới trẻ. Người tham gia sẽ cùng nhau dọn dẹp rác thải tại các khu dân cư, công viên và tuyến đường công cộng. Ngoài hoạt động thu gom rác, chương trình còn có các buổi chia sẻ về phân loại rác, tái chế và lối sống xanh. Sự kiện hướng tới việc xây dựng thói quen sống thân thiện với môi trường và lan tỏa tinh thần trách nhiệm xã hội.	Môi trường	Dịch Vọng Hậu, Hà Nội	2025-12-20	2025-12-21	approved	2025-12-20 14:51:31.215938	2025-12-20 14:52:21.830114
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.notifications (notification_id, user_id, event_id, message, is_read, created_at, updated_at) FROM stdin;
33	20	6	Đơn đăng ký tham gia sự kiện 'Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch' của bạn đã được duyệt.	f	2025-12-20 15:11:29.170828	2025-12-20 15:11:29.170828
27	22	\N	Bạn đã bị khóa tài khoản.	f	2025-12-20 14:41:37.75911	2025-12-20 14:41:37.75911
28	19	6	Sự kiện Ngày Chủ Nhật Xanh – Vì Một Thành Phố Sạch được duyệt thành công	t	2025-12-20 14:52:21.84155	2025-12-20 14:52:34.405598
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.posts (post_id, event_id, user_id, images_url, content, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: push_subscriptions; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.push_subscriptions (id, user_id, endpoint, p256dh, auth, created_at, updated_at) FROM stdin;
14	18	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:41:20.802212	2025-12-20 14:41:20.802212
15	19	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:41:55.822696	2025-12-20 14:41:55.822696
16	20	https://fcm.googleapis.com/fcm/send/eEI6lQaKn7U:APA91bHFrcwAE2skFy7kiR9aJom5vsMiXO3rpuhfqwZyyV0U2QFWhqmBpbaBQJ2fohT8jPqG0zsda973a0hT_6ZxzBuTLrAiM0235eOtOZaTkLZyO62SDlXnwhfZxkWMVK6X-yKGTc-A	BIMYU7DmsOEprJLvdcjiCLne31ORWWR40Q57HHOr1VGltYy9iB2Unt6NK6i6KrvKnBNffac+ZeN1Xh4D9G7Imic=	Hr+ExZypRupkUit3jCPwYg==	2025-12-20 14:58:25.320116	2025-12-20 14:58:25.320116
\.


--
-- Data for Name: reacts; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.reacts (react_id, post_id, user_id, category, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: phamngocdo
--

COPY public.users (user_id, first_name, last_name, email, password, phone_number, role, status, created_at, updated_at, avatar_url) FROM stdin;
20	Phạm	Ngọc Đô	phamdo@gmail.com	$2b$12$Gx1Z0rXee5SbJJtHwhhL9OkcYQZD5Af/rt/hBf2HVs2hrMLbmsqBy	0969670190	volunteer	active	2025-12-20 14:33:08.418165	2025-12-20 14:33:08.418165	\N
19	Phạm	Cương	manager@gmail.com	$2b$12$C8FTou61HyXeBtxO2F5OBusxqIjGSJyJSWQ6a8c9U1nUYlLfAh7FC	0961611349	manager	active	2025-12-20 14:30:31.244241	2025-12-20 14:30:31.244241	\N
18	Phạm	Đô	admin@gmail.com	$2b$12$FDVlNuuH5zb/TPjqgfkm7e9PpOj8Nu3GWcND6rJV/eFT1rZq/3nHK	0906212132	admin	active	2025-12-20 14:29:40.979365	2025-12-20 14:29:40.979365	\N
21	Nguyễn Quang	Duy	duyquang@gmail.com	$2b$12$6RqPjBzqH6MEMI7CSfMU2uVPtEgdhP/pXH8O4q3/2wtDLcAcFplvu	0923465569	volunteer	active	2025-12-20 14:39:30.073403	2025-12-20 14:39:30.073403	\N
23	Cường	Nguyễn	ngcuong@gmail.com	$2b$12$1SZIpJZJKVpZICGOnaM/J.SZri9QJsgzGECFjG9ZQKiueVwW3XdA6	0954363598	volunteer	active	2025-12-20 14:41:03.382111	2025-12-20 14:41:03.382111	\N
22	Doãn	Minh	ddminh@gmail.com	$2b$12$VeOubMxAmVoHNeyOImRKTuCgIAYk.T./lt.WKwW4R66n3F6RMQeUS	0936463953	volunteer	banned	2025-12-20 14:40:01.491753	2025-12-20 14:41:37.747149	\N
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 8, true);


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.event_registrations_registration_id_seq', 15, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.events_event_id_seq', 6, true);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.notifications_notification_id_seq', 33, true);


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 8, true);


--
-- Name: push_subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.push_subscriptions_id_seq', 16, true);


--
-- Name: reacts_like_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.reacts_like_id_seq', 10, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phamngocdo
--

SELECT pg_catalog.setval('public.users_user_id_seq', 23, true);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: event_registrations event_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_pkey PRIMARY KEY (registration_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: push_subscriptions push_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.push_subscriptions
    ADD CONSTRAINT push_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: reacts reacts_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_pkey PRIMARY KEY (react_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: event_registrations_event_id_user_id_idx; Type: INDEX; Schema: public; Owner: phamngocdo
--

CREATE UNIQUE INDEX event_registrations_event_id_user_id_idx ON public.event_registrations USING btree (event_id, user_id);


--
-- Name: push_subscriptions_user_id_endpoint_idx; Type: INDEX; Schema: public; Owner: phamngocdo
--

CREATE UNIQUE INDEX push_subscriptions_user_id_endpoint_idx ON public.push_subscriptions USING btree (user_id, endpoint);


--
-- Name: reacts_post_id_user_id_idx; Type: INDEX; Schema: public; Owner: phamngocdo
--

CREATE UNIQUE INDEX reacts_post_id_user_id_idx ON public.reacts USING btree (post_id, user_id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: event_registrations event_registrations_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: event_registrations event_registrations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: events events_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.users(user_id);


--
-- Name: push_subscriptions fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.push_subscriptions
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: notifications notifications_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: posts posts_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reacts reacts_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: reacts reacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phamngocdo
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

\unrestrict kgFI4sSvMviHfyf37GdWY37aOrhv76QbG1JgXGA5OQdfcwN9Q0ThHRCqJdLfIPV

