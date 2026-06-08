--
-- PostgreSQL database dump
--

\restrict 1GX7ZT0baa7a9OF54FCfR0m8G7l7Z6eznLl8NiVIp1OhIEXT1CVSMdXImU9mr46

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: action_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.action_logs (
    id integer NOT NULL,
    store_id integer,
    user_id integer,
    action_type character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.action_logs OWNER TO postgres;

--
-- Name: action_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.action_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.action_logs_id_seq OWNER TO postgres;

--
-- Name: action_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.action_logs_id_seq OWNED BY public.action_logs.id;


--
-- Name: agencies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agencies (
    id integer NOT NULL,
    name character varying NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.agencies OWNER TO postgres;

--
-- Name: agencies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agencies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agencies_id_seq OWNER TO postgres;

--
-- Name: agencies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agencies_id_seq OWNED BY public.agencies.id;


--
-- Name: competitor_metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competitor_metrics (
    id integer NOT NULL,
    keyword character varying,
    name character varying,
    rating double precision,
    review_count integer,
    rank integer,
    checked_at timestamp without time zone
);


ALTER TABLE public.competitor_metrics OWNER TO postgres;

--
-- Name: competitor_metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.competitor_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.competitor_metrics_id_seq OWNER TO postgres;

--
-- Name: competitor_metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.competitor_metrics_id_seq OWNED BY public.competitor_metrics.id;


--
-- Name: competitors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competitors (
    id integer NOT NULL,
    org_id integer,
    keyword character varying,
    name character varying,
    place_id character varying,
    rating double precision,
    review_count integer,
    "position" integer
);


ALTER TABLE public.competitors OWNER TO postgres;

--
-- Name: competitors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.competitors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.competitors_id_seq OWNER TO postgres;

--
-- Name: competitors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.competitors_id_seq OWNED BY public.competitors.id;


--
-- Name: keyword_rankings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keyword_rankings (
    id integer NOT NULL,
    store_id integer,
    keyword character varying,
    rank integer,
    checked_at timestamp without time zone
);


ALTER TABLE public.keyword_rankings OWNER TO postgres;

--
-- Name: keyword_rankings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.keyword_rankings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.keyword_rankings_id_seq OWNER TO postgres;

--
-- Name: keyword_rankings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.keyword_rankings_id_seq OWNED BY public.keyword_rankings.id;


--
-- Name: keywords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keywords (
    id integer NOT NULL,
    org_id integer NOT NULL,
    keyword character varying(255) NOT NULL,
    category character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.keywords OWNER TO postgres;

--
-- Name: keywords_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.keywords_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.keywords_id_seq OWNER TO postgres;

--
-- Name: keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.keywords_id_seq OWNED BY public.keywords.id;


--
-- Name: metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metrics (
    id integer NOT NULL,
    store_id integer,
    keyword text,
    metric_date date,
    google_rank integer,
    hpb_clicks integer,
    phone_calls integer,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.metrics OWNER TO postgres;

--
-- Name: metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metrics_id_seq OWNER TO postgres;

--
-- Name: metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metrics_id_seq OWNED BY public.metrics.id;


--
-- Name: orgs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orgs (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.orgs OWNER TO postgres;

--
-- Name: orgs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orgs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orgs_id_seq OWNER TO postgres;

--
-- Name: orgs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orgs_id_seq OWNED BY public.orgs.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    store_id integer NOT NULL,
    status character varying(50) NOT NULL,
    title character varying(255),
    content text NOT NULL,
    source_title character varying(300),
    source_url character varying(600) NOT NULL,
    google_post_id character varying(200),
    posted_at timestamp without time zone,
    last_error text,
    created_at timestamp without time zone DEFAULT now(),
    org_id integer NOT NULL
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    store_id integer,
    rating integer,
    comment text,
    reviewer_name character varying(200),
    review_time timestamp without time zone,
    reply_draft text,
    reply_strategy character varying,
    reply_text text,
    replied_at timestamp without time zone,
    google_review_id character varying(200),
    created_at timestamp without time zone DEFAULT now(),
    staff_name character varying,
    menu_name character varying
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_id_seq OWNER TO postgres;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: store_keywords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_keywords (
    id integer NOT NULL,
    store_id integer NOT NULL,
    keyword_id integer NOT NULL,
    is_active boolean NOT NULL,
    priority integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.store_keywords OWNER TO postgres;

--
-- Name: store_keywords_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_keywords_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.store_keywords_id_seq OWNER TO postgres;

--
-- Name: store_keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_keywords_id_seq OWNED BY public.store_keywords.id;


--
-- Name: store_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_users (
    id integer NOT NULL,
    store_id integer,
    user_id integer
);


ALTER TABLE public.store_users OWNER TO postgres;

--
-- Name: store_users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.store_users_id_seq OWNER TO postgres;

--
-- Name: store_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_users_id_seq OWNED BY public.store_users.id;


--
-- Name: stores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stores (
    id integer NOT NULL,
    store_code character varying(50),
    name character varying(255),
    place_id character varying,
    station character varying(255),
    hpb_url character varying(500),
    location_id character varying(255),
    post_interval_days integer,
    strategy_key character varying(100),
    phone_number character varying(50),
    cta_url character varying(500),
    org_id integer,
    created_at timestamp without time zone,
    google_place_id character varying(255),
    line_user_id character varying,
    area character varying,
    main_menu character varying
);


ALTER TABLE public.stores OWNER TO postgres;

--
-- Name: stores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stores_id_seq OWNER TO postgres;

--
-- Name: stores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stores_id_seq OWNED BY public.stores.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    store_id integer,
    review_id integer,
    type character varying(50),
    title character varying(255),
    description text,
    status character varying(50),
    priority character varying(50),
    assigned_to character varying(50),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    line_user_id character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: action_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.action_logs ALTER COLUMN id SET DEFAULT nextval('public.action_logs_id_seq'::regclass);


--
-- Name: agencies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agencies ALTER COLUMN id SET DEFAULT nextval('public.agencies_id_seq'::regclass);


--
-- Name: competitor_metrics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competitor_metrics ALTER COLUMN id SET DEFAULT nextval('public.competitor_metrics_id_seq'::regclass);


--
-- Name: competitors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competitors ALTER COLUMN id SET DEFAULT nextval('public.competitors_id_seq'::regclass);


--
-- Name: keyword_rankings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyword_rankings ALTER COLUMN id SET DEFAULT nextval('public.keyword_rankings_id_seq'::regclass);


--
-- Name: keywords id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keywords ALTER COLUMN id SET DEFAULT nextval('public.keywords_id_seq'::regclass);


--
-- Name: metrics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics ALTER COLUMN id SET DEFAULT nextval('public.metrics_id_seq'::regclass);


--
-- Name: orgs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs ALTER COLUMN id SET DEFAULT nextval('public.orgs_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: store_keywords id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_keywords ALTER COLUMN id SET DEFAULT nextval('public.store_keywords_id_seq'::regclass);


--
-- Name: store_users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_users ALTER COLUMN id SET DEFAULT nextval('public.store_users_id_seq'::regclass);


--
-- Name: stores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores ALTER COLUMN id SET DEFAULT nextval('public.stores_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: action_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.action_logs (id, store_id, user_id, action_type, created_at) FROM stdin;
1	2	1	review_reply	2026-04-06 11:14:32.045516
2	2	1	review_reply	2026-04-06 13:13:26.01796
\.


--
-- Data for Name: agencies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agencies (id, name, created_at) FROM stdin;
\.


--
-- Data for Name: competitor_metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.competitor_metrics (id, keyword, name, rating, review_count, rank, checked_at) FROM stdin;
\.


--
-- Data for Name: competitors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.competitors (id, org_id, keyword, name, place_id, rating, review_count, "position") FROM stdin;
\.


--
-- Data for Name: keyword_rankings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.keyword_rankings (id, store_id, keyword, rank, checked_at) FROM stdin;
\.


--
-- Data for Name: keywords; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.keywords (id, org_id, keyword, category, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metrics (id, store_id, keyword, metric_date, google_rank, hpb_clicks, phone_calls, created_at) FROM stdin;
1	1	\N	2026-04-04	14	11	1	2026-04-04 02:17:25.904256
2	2	\N	2026-04-04	8	28	4	2026-04-04 02:17:25.904256
3	3	\N	2026-04-04	3	54	7	2026-04-04 02:17:25.904256
\.


--
-- Data for Name: orgs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orgs (id, name) FROM stdin;
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (id, store_id, status, title, content, source_title, source_url, google_post_id, posted_at, last_error, created_at, org_id) FROM stdin;
1	2	posted	\N	春の髪質改善カラー特集を公開しました。	春の髪質改善カラー		\N	2026-04-04 02:17:25.91059	\N	2026-04-04 02:17:25.904256	1
3	3	posted	\N	髪質改善トリートメントのビフォーアフターを投稿。	髪質改善トリートメント		\N	2026-04-04 02:17:25.910959	\N	2026-04-04 02:17:25.904256	1
4	3	posted	\N	大人女性向けショート特集を投稿。	大人女性ショート		\N	2026-04-04 02:17:25.910968	\N	2026-04-04 02:17:25.904256	1
2	2	approved	\N	顔まわりレイヤーのおすすめスタイル。	顔まわりレイヤー		\N	\N	\N	2026-04-04 02:17:25.904256	1
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (id, store_id, rating, comment, reviewer_name, review_time, reply_draft, reply_strategy, reply_text, replied_at, google_review_id, created_at, staff_name, menu_name) FROM stdin;
1	1	2	カットと髪質改善カラーで来店しましたが、待ち時間が少し長かったです。仕上がりは良かったです。	山田花子	\N	\N	\N	\N	\N	\N	2026-04-04 02:17:25.904256	藤田	カット＋髪質改善カラー
2	1	5	髪質改善トリートメントが良くて手触りがかなり変わりました！	中村彩	\N	\N	\N	\N	\N	\N	2026-04-04 02:17:25.904256	藤田	髪質改善トリートメント
3	1	4	カットは満足です。またお願いしたいです。	田中一樹	\N	\N	\N	\N	\N	\N	2026-04-04 02:17:25.904256	藤田	カット
4	2	4	ハイライトがきれいで満足です。雰囲気も良かったです。	松本美咲	\N	\N	\N	\N	\N	\N	2026-04-04 02:17:25.904256	藤田	カット＋ハイライト
5	2	5	子連れでも行きやすく、髪質改善カラーの仕上がりも良かったです。	井上里奈	\N	\N	\N	ご来店ありがとうございました！またお待ちしております。	\N	\N	2026-04-04 02:17:25.904256	藤田	髪質改善カラー
7	3	5	髪質改善トリートメントでまとまりが出て大満足です！	木村愛	\N	\N	\N	嬉しい口コミありがとうございます！またお待ちしております。	\N	\N	2026-04-04 02:17:25.904256	藤田	髪質改善トリートメント
8	2	1	最悪でした	\N	\N	\N	\N	\N	\N	\N	2026-04-05 05:51:27.654425	\N	\N
10	2	1	最悪でした	\N	\N	\N	\N	返信内容	\N	\N	2026-04-05 07:14:58.264451	\N	\N
9	2	1	最悪でした	\N	\N	\N	\N	返信内容	\N	\N	2026-04-05 05:52:57.16617	\N	\N
6	3	5	カットもカラーも丁寧で安心して任せられました。	小林舞	\N	\N	\N	\N	\N	\N	2026-04-04 02:17:25.904256	藤田	カット＋カラー
\.


--
-- Data for Name: store_keywords; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.store_keywords (id, store_id, keyword_id, is_active, priority, created_at) FROM stdin;
\.


--
-- Data for Name: store_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.store_users (id, store_id, user_id) FROM stdin;
1	2	1
2	1	1
3	1	1
4	3	1
\.


--
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stores (id, store_code, name, place_id, station, hpb_url, location_id, post_interval_days, strategy_key, phone_number, cta_url, org_id, created_at, google_place_id, line_user_id, area, main_menu) FROM stdin;
1	demo-sakai	AVANCE.深井	\N	深井		\N	2	reservation_push			1	\N	\N	\N	\N	\N
2	demo-fukai	アリオ鳳	\N	鳳		\N	2	reservation_push			1	\N	\N	\N	\N	\N
3	demo-otsu	AVANCE.泉大津	\N	泉大津		\N	2	reservation_push			1	\N	\N	\N	\N	\N
4	test001	テスト店舗	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, store_id, review_id, type, title, description, status, priority, assigned_to, created_at, updated_at) FROM stdin;
17	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-20 07:06:27.185528	\N
18	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-20 07:06:28.439111	\N
19	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-20 10:09:21.993561	\N
20	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-21 00:25:01.317333	\N
21	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-21 00:25:03.098202	\N
22	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-21 00:25:03.256827	\N
23	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-22 00:59:06.895094	\N
24	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-22 00:59:08.596322	\N
25	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-22 00:59:13.264667	\N
26	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-23 00:11:00.06372	\N
27	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-23 00:11:00.695239	\N
28	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-23 00:11:00.838047	\N
29	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-24 00:38:30.209705	\N
30	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-24 00:38:31.15593	\N
31	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-24 00:38:31.263884	\N
32	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-25 02:08:34.870797	\N
33	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-25 02:08:35.503458	\N
34	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-25 02:08:35.62552	\N
35	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-26 00:49:23.11986	\N
36	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-26 00:49:24.695343	\N
37	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-26 00:49:24.950611	\N
38	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-27 01:20:38.920337	\N
39	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-27 01:20:39.338713	\N
40	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-27 01:20:39.461345	\N
41	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-28 00:19:21.234418	\N
42	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-28 00:19:21.944652	\N
43	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-28 00:19:22.137689	\N
44	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-29 00:28:17.150932	\N
45	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-29 00:28:21.558693	\N
46	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-29 00:28:22.375654	\N
47	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-30 00:01:28.442762	\N
48	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-30 00:01:29.218211	\N
49	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-04-30 00:01:29.45649	\N
50	1	\N	review_reply	morning_sent	\N	done	normal	\N	2026-05-01 00:44:48.110683	\N
51	2	\N	review_reply	morning_sent	\N	done	normal	\N	2026-05-01 00:44:49.524742	\N
52	3	\N	review_reply	morning_sent	\N	done	normal	\N	2026-05-01 00:44:50.377146	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, line_user_id) FROM stdin;
1	Uea9d5bf991230a9ff066272797da6cae
\.


--
-- Name: action_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.action_logs_id_seq', 2, true);


--
-- Name: agencies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agencies_id_seq', 1, false);


--
-- Name: competitor_metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.competitor_metrics_id_seq', 1, false);


--
-- Name: competitors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.competitors_id_seq', 1, false);


--
-- Name: keyword_rankings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.keyword_rankings_id_seq', 1, false);


--
-- Name: keywords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.keywords_id_seq', 1, false);


--
-- Name: metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.metrics_id_seq', 3, true);


--
-- Name: orgs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orgs_id_seq', 1, false);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_id_seq', 4, true);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reviews_id_seq', 10, true);


--
-- Name: store_keywords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.store_keywords_id_seq', 1, false);


--
-- Name: store_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.store_users_id_seq', 4, true);


--
-- Name: stores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stores_id_seq', 4, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 52, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: action_logs action_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.action_logs
    ADD CONSTRAINT action_logs_pkey PRIMARY KEY (id);


--
-- Name: agencies agencies_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT agencies_name_key UNIQUE (name);


--
-- Name: agencies agencies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT agencies_pkey PRIMARY KEY (id);


--
-- Name: competitor_metrics competitor_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competitor_metrics
    ADD CONSTRAINT competitor_metrics_pkey PRIMARY KEY (id);


--
-- Name: competitors competitors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competitors
    ADD CONSTRAINT competitors_pkey PRIMARY KEY (id);


--
-- Name: keyword_rankings keyword_rankings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyword_rankings
    ADD CONSTRAINT keyword_rankings_pkey PRIMARY KEY (id);


--
-- Name: keywords keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_pkey PRIMARY KEY (id);


--
-- Name: metrics metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_pkey PRIMARY KEY (id);


--
-- Name: orgs orgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs
    ADD CONSTRAINT orgs_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: store_keywords store_keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_keywords
    ADD CONSTRAINT store_keywords_pkey PRIMARY KEY (id);


--
-- Name: store_users store_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_users
    ADD CONSTRAINT store_users_pkey PRIMARY KEY (id);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: keywords uq_keywords_org_keyword; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT uq_keywords_org_keyword UNIQUE (org_id, keyword);


--
-- Name: store_keywords uq_store_keywords_store_keyword; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_keywords
    ADD CONSTRAINT uq_store_keywords_store_keyword UNIQUE (store_id, keyword_id);


--
-- Name: users users_line_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_line_user_id_key UNIQUE (line_user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_keywords_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_keywords_id ON public.keywords USING btree (id);


--
-- Name: ix_keywords_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_keywords_org_id ON public.keywords USING btree (org_id);


--
-- Name: ix_store_keywords_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_keywords_id ON public.store_keywords USING btree (id);


--
-- Name: ix_store_keywords_keyword_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_keywords_keyword_id ON public.store_keywords USING btree (keyword_id);


--
-- Name: ix_store_keywords_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_keywords_store_id ON public.store_keywords USING btree (store_id);


--
-- Name: ix_tasks_review_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_review_id ON public.tasks USING btree (review_id);


--
-- Name: ix_tasks_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_store_id ON public.tasks USING btree (store_id);


--
-- Name: metrics metrics_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);


--
-- Name: store_keywords store_keywords_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_keywords
    ADD CONSTRAINT store_keywords_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES public.keywords(id);


--
-- Name: store_keywords store_keywords_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_keywords
    ADD CONSTRAINT store_keywords_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);


--
-- Name: store_users store_users_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_users
    ADD CONSTRAINT store_users_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);


--
-- Name: store_users store_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_users
    ADD CONSTRAINT store_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tasks tasks_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 1GX7ZT0baa7a9OF54FCfR0m8G7l7Z6eznLl8NiVIp1OhIEXT1CVSMdXImU9mr46

