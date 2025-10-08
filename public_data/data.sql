--
-- PostgreSQL database dump
--

\restrict I0f10GCi7Xr9U9sVKOJNRjTc8bUrJqdz3B4d9gLvZWyMXhRnpeEdzt10UqY8MRm

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
-- Name: comments; Type: TABLE; Schema: public; Owner: duy
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer,
    user_id integer,
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.comments OWNER TO duy;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_comment_id_seq OWNER TO duy;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: event_registrations; Type: TABLE; Schema: public; Owner: duy
--

CREATE TABLE public.event_registrations (
    registration_id integer NOT NULL,
    event_id integer,
    user_id integer,
    status character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.event_registrations OWNER TO duy;

--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.event_registrations_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_registrations_registration_id_seq OWNER TO duy;

--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.event_registrations_registration_id_seq OWNED BY public.event_registrations.registration_id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: duy
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.events OWNER TO duy;

--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_event_id_seq OWNER TO duy;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: duy
--

CREATE TABLE public.notifications (
    notification_id integer NOT NULL,
    user_id integer,
    event_id integer,
    message text,
    is_read boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.notifications OWNER TO duy;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_notification_id_seq OWNER TO duy;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: duy
--

CREATE TABLE public.posts (
    post_id integer NOT NULL,
    event_id integer,
    user_id integer,
    images_url character varying(200),
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.posts OWNER TO duy;

--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_post_id_seq OWNER TO duy;

--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: reacts; Type: TABLE; Schema: public; Owner: duy
--

CREATE TABLE public.reacts (
    like_id integer NOT NULL,
    post_id integer,
    user_id integer,
    category character varying(100),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.reacts OWNER TO duy;

--
-- Name: reacts_like_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.reacts_like_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reacts_like_id_seq OWNER TO duy;

--
-- Name: reacts_like_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.reacts_like_id_seq OWNED BY public.reacts.like_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: duy
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
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO duy;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: duy
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO duy;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: duy
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: event_registrations registration_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.event_registrations ALTER COLUMN registration_id SET DEFAULT nextval('public.event_registrations_registration_id_seq'::regclass);


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: notifications notification_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);


--
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: reacts like_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.reacts ALTER COLUMN like_id SET DEFAULT nextval('public.reacts_like_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.comments (comment_id, post_id, user_id, content, created_at, updated_at) FROM stdin;
1	1	2	Tốt lắm, cảm ơn bạn đã tham gia!	2025-10-08 10:47:25.203167+00	2025-10-08 10:47:25.203167+00
2	1	3	Mình cũng ở đó, rất vui!	2025-10-08 10:47:25.203167+00	2025-10-08 10:47:25.203167+00
3	3	4	Một nghĩa cử thật cao đẹp.	2025-10-08 10:47:25.203167+00	2025-10-08 10:47:25.203167+00
4	4	2	Sự kiện thật thành công!	2025-10-08 10:47:25.203167+00	2025-10-08 10:47:25.203167+00
5	5	5	Mong được gặp mọi người ở sự kiện tới!	2025-10-08 10:47:25.203167+00	2025-10-08 10:47:25.203167+00
\.


--
-- Data for Name: event_registrations; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.event_registrations (registration_id, event_id, user_id, status, created_at, updated_at) FROM stdin;
1	1	1	approved	2025-10-08 10:46:46.165894+00	2025-10-08 10:46:46.165894+00
2	1	3	approved	2025-10-08 10:46:46.165894+00	2025-10-08 10:46:46.165894+00
3	2	1	pending	2025-10-08 10:46:46.165894+00	2025-10-08 10:46:46.165894+00
4	3	5	cancelled	2025-10-08 10:46:46.165894+00	2025-10-08 10:46:46.165894+00
5	4	1	completed	2025-10-08 10:46:46.165894+00	2025-10-08 10:46:46.165894+00
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.events (event_id, manager_id, title, image_url, description, category, location, start_date, end_date, status, created_at, updated_at) FROM stdin;
1	4	Dọn rác bãi biển Đà Nẵng	https://example.com/beach.jpg	Cùng nhau làm sạch bãi biển Mỹ Khê.	Môi trường	Đà Nẵng	2025-11-10	2025-11-11	approved	2025-10-08 10:46:23.529548+00	2025-10-08 10:46:23.529548+00
2	4	Trồng cây tại công viên Thống Nhất	https://example.com/trees.jpg	Sự kiện trồng 500 cây xanh.	Môi trường	Hà Nội	2025-11-15	2025-11-15	pending	2025-10-08 10:46:23.529548+00	2025-10-08 10:46:23.529548+00
3	4	Hiến máu nhân đạo	https://example.com/blood.jpg	Chương trình hiến máu cứu người.	Sức khỏe	TP. HCM	2025-12-01	2025-12-02	approved	2025-10-08 10:46:23.529548+00	2025-10-08 10:46:23.529548+00
4	4	Chạy bộ gây quỹ	https://example.com/run.jpg	Chạy bộ 5km gây quỹ ủng hộ trẻ em nghèo.	Từ thiện	Huế	2025-12-10	2025-12-10	completed	2025-10-08 10:46:23.529548+00	2025-10-08 10:46:23.529548+00
5	4	Phát cơm miễn phí	https://example.com/food.jpg	Phát cơm từ thiện tại bệnh viện.	Từ thiện	Hà Nội	2025-11-20	2025-11-20	pending	2025-10-08 10:46:23.529548+00	2025-10-08 10:46:23.529548+00
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.notifications (notification_id, user_id, event_id, message, is_read, created_at, updated_at) FROM stdin;
1	1	1	Sự kiện "Dọn rác bãi biển Đà Nẵng" đã được phê duyệt.	f	2025-10-08 10:47:56.726467+00	2025-10-08 10:47:56.726467+00
2	3	2	Bạn đã đăng ký sự kiện "Trồng cây tại công viên Thống Nhất".	t	2025-10-08 10:47:56.726467+00	2025-10-08 10:47:56.726467+00
3	5	3	Trạng thái sự kiện "Hiến máu nhân đạo" đã thay đổi.	f	2025-10-08 10:47:56.726467+00	2025-10-08 10:47:56.726467+00
4	1	4	Sự kiện "Chạy bộ gây quỹ" đã hoàn thành.	t	2025-10-08 10:47:56.726467+00	2025-10-08 10:47:56.726467+00
5	3	5	Bạn có thông báo mới từ quản lý sự kiện.	f	2025-10-08 10:47:56.726467+00	2025-10-08 10:47:56.726467+00
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.posts (post_id, event_id, user_id, images_url, content, created_at, updated_at) FROM stdin;
1	1	1	https://example.com/post1.jpg	Buổi dọn rác hôm nay thật ý nghĩa!	2025-10-08 10:47:06.264195+00	2025-10-08 10:47:06.264195+00
2	1	3	https://example.com/post2.jpg	Mọi người rất nhiệt tình và vui vẻ.	2025-10-08 10:47:06.264195+00	2025-10-08 10:47:06.264195+00
3	3	5	https://example.com/post3.jpg	Hiến máu cứu người – một hành động nhỏ, ý nghĩa lớn.	2025-10-08 10:47:06.264195+00	2025-10-08 10:47:06.264195+00
4	4	1	https://example.com/post4.jpg	Chạy bộ 5km cùng bạn bè thật tuyệt!	2025-10-08 10:47:06.264195+00	2025-10-08 10:47:06.264195+00
5	2	3	https://example.com/post5.jpg	Mong chờ ngày trồng cây sắp tới!	2025-10-08 10:47:06.264195+00	2025-10-08 10:47:06.264195+00
\.


--
-- Data for Name: reacts; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.reacts (like_id, post_id, user_id, category, created_at, updated_at) FROM stdin;
1	1	2	like	2025-10-08 10:47:43.681325+00	2025-10-08 10:47:43.681325+00
2	1	3	love	2025-10-08 10:47:43.681325+00	2025-10-08 10:47:43.681325+00
3	3	1	wow	2025-10-08 10:47:43.681325+00	2025-10-08 10:47:43.681325+00
4	4	2	haha	2025-10-08 10:47:43.681325+00	2025-10-08 10:47:43.681325+00
5	5	5	like	2025-10-08 10:47:43.681325+00	2025-10-08 10:47:43.681325+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: duy
--

COPY public.users (user_id, first_name, last_name, email, password, phone_number, role, status, created_at, updated_at) FROM stdin;
1	Duy	Nguyen	duy@gmail.com	123456	0123456789	volunteer	pending	2025-10-08 10:46:07.252372+00	2025-10-08 10:46:07.252372+00
2	Do	Pham	do@gmail.com	123456	0987654321	admin	active	2025-10-08 10:46:07.252372+00	2025-10-08 10:46:07.252372+00
3	Minh	Doan	minh@gmail.com	123456	0112233445	volunteer	pending	2025-10-08 10:46:07.252372+00	2025-10-08 10:46:07.252372+00
4	Trang	Le	trang@gmail.com	123456	0998877665	manager	active	2025-10-08 10:46:07.252372+00	2025-10-08 10:46:07.252372+00
5	Tuan	Pham	tuan@gmail.com	123456	0909090909	volunteer	banned	2025-10-08 10:46:07.252372+00	2025-10-08 10:46:07.252372+00
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 5, true);


--
-- Name: event_registrations_registration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.event_registrations_registration_id_seq', 5, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.events_event_id_seq', 5, true);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.notifications_notification_id_seq', 5, true);


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 5, true);


--
-- Name: reacts_like_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.reacts_like_id_seq', 5, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: duy
--

SELECT pg_catalog.setval('public.users_user_id_seq', 5, true);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: event_registrations event_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_pkey PRIMARY KEY (registration_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: reacts reacts_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_pkey PRIMARY KEY (like_id);


--
-- Name: event_registrations unique_event_user; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT unique_event_user UNIQUE (event_id, user_id);


--
-- Name: reacts unique_post_user_react; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT unique_post_user_react UNIQUE (post_id, user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: ix_comments_comment_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_comments_comment_id ON public.comments USING btree (comment_id);


--
-- Name: ix_event_registrations_registration_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_event_registrations_registration_id ON public.event_registrations USING btree (registration_id);


--
-- Name: ix_events_event_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_events_event_id ON public.events USING btree (event_id);


--
-- Name: ix_notifications_notification_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_notifications_notification_id ON public.notifications USING btree (notification_id);


--
-- Name: ix_posts_post_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_posts_post_id ON public.posts USING btree (post_id);


--
-- Name: ix_reacts_like_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_reacts_like_id ON public.reacts USING btree (like_id);


--
-- Name: ix_users_user_id; Type: INDEX; Schema: public; Owner: duy
--

CREATE INDEX ix_users_user_id ON public.users USING btree (user_id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: event_registrations event_registrations_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: event_registrations event_registrations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: events events_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.users(user_id);


--
-- Name: notifications notifications_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: posts posts_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reacts reacts_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: reacts reacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: duy
--

ALTER TABLE ONLY public.reacts
    ADD CONSTRAINT reacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

\unrestrict I0f10GCi7Xr9U9sVKOJNRjTc8bUrJqdz3B4d9gLvZWyMXhRnpeEdzt10UqY8MRm

