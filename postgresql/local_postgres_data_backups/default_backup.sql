--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5
-- Dumped by pg_dump version 10.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT "django_admin_log_user_id_c564eba6_fk_LogIn_Man";
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE ONLY public."LogIn_Management_user_groups" DROP CONSTRAINT "LogIn_Management_user_groups_group_id_84db3e0e_fk_auth_group_id";
ALTER TABLE ONLY public."LogIn_Management_user_groups" DROP CONSTRAINT "LogIn_Management_use_user_id_a7e13076_fk_LogIn_Man";
ALTER TABLE ONLY public."LogIn_Management_user_user_permissions" DROP CONSTRAINT "LogIn_Management_use_user_id_08db02bd_fk_LogIn_Man";
ALTER TABLE ONLY public."LogIn_Management_user_user_permissions" DROP CONSTRAINT "LogIn_Management_use_permission_id_9b1826c8_fk_auth_perm";
ALTER TABLE ONLY public."LogIn_Management_profile" DROP CONSTRAINT "LogIn_Management_pro_user_id_8450ccb2_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_quizscore" DROP CONSTRAINT "Class_Management_qui_userId_id_9f1d0641_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_quiztracker" DROP CONSTRAINT "Class_Management_qui_userId_id_95b7aa39_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_quiztimer" DROP CONSTRAINT "Class_Management_qui_userId_id_3089c57e_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_quizstatus" DROP CONSTRAINT "Class_Management_qui_userId_id_00a1707d_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_quizscore" DROP CONSTRAINT "Class_Management_qui_quizId_id_ed1c425f_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quiztimer" DROP CONSTRAINT "Class_Management_qui_quizId_id_e7fb481d_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quizstatus" DROP CONSTRAINT "Class_Management_qui_quizId_id_8375504c_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quizscore" DROP CONSTRAINT "Class_Management_qui_code_id_1c65dd40_fk_Assign_Ma";
ALTER TABLE ONLY public."Class_Management_quiztracker" DROP CONSTRAINT "Class_Management_qui_classroom_id_83db111b_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quizstatus" DROP CONSTRAINT "Class_Management_qui_classroom_id_5bbf9c63_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quiztimer" DROP CONSTRAINT "Class_Management_qui_classroom_id_4baabc98_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quiz" DROP CONSTRAINT "Class_Management_qui_classroom_id_3dfc1262_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quizscore" DROP CONSTRAINT "Class_Management_qui_classroom_id_059aa3a7_fk_Class_Man";
ALTER TABLE ONLY public."Class_Management_quiz" DROP CONSTRAINT "Class_Management_qui_category_id_1fe0e92b_fk_Assign_Ma";
ALTER TABLE ONLY public."Class_Management_classroom_user" DROP CONSTRAINT "Class_Management_cla_user_id_bbbf76f7_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_classroom" DROP CONSTRAINT "Class_Management_cla_creator_id_9361d351_fk_LogIn_Man";
ALTER TABLE ONLY public."Class_Management_classroom_user" DROP CONSTRAINT "Class_Management_cla_classroom_id_d3bf0654_fk_Class_Man";
ALTER TABLE ONLY public."Assign_Management_upload" DROP CONSTRAINT "Assign_Management_up_user_id_da31c61f_fk_LogIn_Man";
ALTER TABLE ONLY public."Assign_Management_upload" DROP CONSTRAINT "Assign_Management_up_quiz_id_baaf6fdf_fk_Class_Man";
ALTER TABLE ONLY public."Assign_Management_upload" DROP CONSTRAINT "Assign_Management_up_classroom_id_0557a92e_fk_Class_Man";
ALTER TABLE ONLY public."Assign_Management_exam_tracker" DROP CONSTRAINT "Assign_Management_ex_user_id_80f22c59_fk_LogIn_Man";
ALTER TABLE ONLY public."Assign_Management_exam_upload" DROP CONSTRAINT "Assign_Management_ex_user_id_1ddfb625_fk_LogIn_Man";
ALTER TABLE ONLY public."Assign_Management_exam_score" DROP CONSTRAINT "Assign_Management_ex_user_id_0bc5be8f_fk_LogIn_Man";
ALTER TABLE ONLY public."Assign_Management_exam_score" DROP CONSTRAINT "Assign_Management_ex_quiz_id_92b87429_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_upload" DROP CONSTRAINT "Assign_Management_ex_quiz_id_4ec79334_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_upload" DROP CONSTRAINT "Assign_Management_ex_exam_id_fb709bca_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_score" DROP CONSTRAINT "Assign_Management_ex_exam_id_60b75b4f_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_tracker" DROP CONSTRAINT "Assign_Management_ex_exam_id_4fcc5756_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_score" DROP CONSTRAINT "Assign_Management_ex_code_id_74cab813_fk_Assign_Ma";
ALTER TABLE ONLY public."Assign_Management_exam_quiz" DROP CONSTRAINT "Assign_Management_ex_classroom_id_f9849c51_fk_Class_Man";
ALTER TABLE ONLY public."Assign_Management_exam_data" DROP CONSTRAINT "Assign_Management_ex_classroom_id_6210e067_fk_Class_Man";
ALTER TABLE ONLY public."Assign_Management_exam_quiz" DROP CONSTRAINT "Assign_Management_ex_category_id_397f7051_fk_Assign_Ma";
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6_like;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
DROP INDEX public."LogIn_Management_user_user_permissions_user_id_08db02bd_like";
DROP INDEX public."LogIn_Management_user_user_permissions_user_id_08db02bd";
DROP INDEX public."LogIn_Management_user_user_permissions_permission_id_9b1826c8";
DROP INDEX public."LogIn_Management_user_userId_d1cecdac_like";
DROP INDEX public."LogIn_Management_user_groups_user_id_a7e13076_like";
DROP INDEX public."LogIn_Management_user_groups_user_id_a7e13076";
DROP INDEX public."LogIn_Management_user_groups_group_id_84db3e0e";
DROP INDEX public."LogIn_Management_user_email_a9e4c25f_like";
DROP INDEX public."LogIn_Management_profile_user_id_8450ccb2_like";
DROP INDEX public."Class_Management_quiztracker_userId_id_95b7aa39_like";
DROP INDEX public."Class_Management_quiztracker_userId_id_95b7aa39";
DROP INDEX public."Class_Management_quiztracker_classroom_id_83db111b";
DROP INDEX public."Class_Management_quiztimer_userId_id_3089c57e_like";
DROP INDEX public."Class_Management_quiztimer_userId_id_3089c57e";
DROP INDEX public."Class_Management_quiztimer_quizId_id_e7fb481d";
DROP INDEX public."Class_Management_quiztimer_classroom_id_4baabc98";
DROP INDEX public."Class_Management_quizstatus_userId_id_00a1707d_like";
DROP INDEX public."Class_Management_quizstatus_userId_id_00a1707d";
DROP INDEX public."Class_Management_quizstatus_quizId_id_8375504c";
DROP INDEX public."Class_Management_quizstatus_classroom_id_5bbf9c63";
DROP INDEX public."Class_Management_quizscore_userId_id_9f1d0641_like";
DROP INDEX public."Class_Management_quizscore_userId_id_9f1d0641";
DROP INDEX public."Class_Management_quizscore_quizId_id_ed1c425f";
DROP INDEX public."Class_Management_quizscore_code_id_1c65dd40";
DROP INDEX public."Class_Management_quizscore_classroom_id_059aa3a7";
DROP INDEX public."Class_Management_quiz_quizTitle_3aacd799_like";
DROP INDEX public."Class_Management_quiz_classroom_id_3dfc1262";
DROP INDEX public."Class_Management_quiz_category_id_1fe0e92b";
DROP INDEX public."Class_Management_classroom_user_user_id_bbbf76f7_like";
DROP INDEX public."Class_Management_classroom_user_user_id_bbbf76f7";
DROP INDEX public."Class_Management_classroom_user_classroom_id_d3bf0654";
DROP INDEX public."Class_Management_classroom_creator_id_9361d351_like";
DROP INDEX public."Class_Management_classroom_creator_id_9361d351";
DROP INDEX public."Class_Management_classroom_className_36a9972e_like";
DROP INDEX public."Assign_Management_upload_user_id_da31c61f_like";
DROP INDEX public."Assign_Management_upload_user_id_da31c61f";
DROP INDEX public."Assign_Management_upload_quiz_id_baaf6fdf";
DROP INDEX public."Assign_Management_upload_classroom_id_0557a92e";
DROP INDEX public."Assign_Management_exam_upload_user_id_1ddfb625_like";
DROP INDEX public."Assign_Management_exam_upload_user_id_1ddfb625";
DROP INDEX public."Assign_Management_exam_upload_quiz_id_4ec79334";
DROP INDEX public."Assign_Management_exam_upload_exam_id_fb709bca";
DROP INDEX public."Assign_Management_exam_tracker_user_id_80f22c59_like";
DROP INDEX public."Assign_Management_exam_tracker_user_id_80f22c59";
DROP INDEX public."Assign_Management_exam_tracker_exam_id_4fcc5756";
DROP INDEX public."Assign_Management_exam_score_user_id_0bc5be8f_like";
DROP INDEX public."Assign_Management_exam_score_user_id_0bc5be8f";
DROP INDEX public."Assign_Management_exam_score_quiz_id_92b87429";
DROP INDEX public."Assign_Management_exam_score_exam_id_60b75b4f";
DROP INDEX public."Assign_Management_exam_score_code_id_74cab813";
DROP INDEX public."Assign_Management_exam_quiz_title_d1eabc33_like";
DROP INDEX public."Assign_Management_exam_quiz_classroom_id_f9849c51";
DROP INDEX public."Assign_Management_exam_quiz_category_id_397f7051";
DROP INDEX public."Assign_Management_exam_data_name_e1b3d6e1_like";
DROP INDEX public."Assign_Management_exam_data_classroom_id_6210e067";
DROP INDEX public."Assign_Management_category_slug_11c45a1c_like";
DROP INDEX public."Assign_Management_category_slug_11c45a1c";
DROP INDEX public."Assign_Management_category_name_689b6d4f_like";
ALTER TABLE ONLY public."LogIn_Management_user_user_permissions" DROP CONSTRAINT login_management_user_us_user_id_permission_id_0b8ef45b_uniq;
ALTER TABLE ONLY public."LogIn_Management_user_groups" DROP CONSTRAINT login_management_user_groups_user_id_group_id_7aef063c_uniq;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public."Class_Management_classroom_user" DROP CONSTRAINT class_management_classro_classroom_id_user_id_1bd666e7_uniq;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE ONLY public."LogIn_Management_user_user_permissions" DROP CONSTRAINT "LogIn_Management_user_user_permissions_pkey";
ALTER TABLE ONLY public."LogIn_Management_user" DROP CONSTRAINT "LogIn_Management_user_pkey";
ALTER TABLE ONLY public."LogIn_Management_user_groups" DROP CONSTRAINT "LogIn_Management_user_groups_pkey";
ALTER TABLE ONLY public."LogIn_Management_user" DROP CONSTRAINT "LogIn_Management_user_email_key";
ALTER TABLE ONLY public."LogIn_Management_profile" DROP CONSTRAINT "LogIn_Management_profile_user_id_key";
ALTER TABLE ONLY public."LogIn_Management_profile" DROP CONSTRAINT "LogIn_Management_profile_pkey";
ALTER TABLE ONLY public."Class_Management_quiztracker" DROP CONSTRAINT "Class_Management_quiztracker_pkey";
ALTER TABLE ONLY public."Class_Management_quiztimer" DROP CONSTRAINT "Class_Management_quiztimer_pkey";
ALTER TABLE ONLY public."Class_Management_quizstatus" DROP CONSTRAINT "Class_Management_quizstatus_pkey";
ALTER TABLE ONLY public."Class_Management_quizscore" DROP CONSTRAINT "Class_Management_quizscore_pkey";
ALTER TABLE ONLY public."Class_Management_quiz" DROP CONSTRAINT "Class_Management_quiz_quizTitle_key";
ALTER TABLE ONLY public."Class_Management_quiz" DROP CONSTRAINT "Class_Management_quiz_pkey";
ALTER TABLE ONLY public."Class_Management_classroom_user" DROP CONSTRAINT "Class_Management_classroom_user_pkey";
ALTER TABLE ONLY public."Class_Management_classroom" DROP CONSTRAINT "Class_Management_classroom_pkey";
ALTER TABLE ONLY public."Class_Management_classroom" DROP CONSTRAINT "Class_Management_classroom_className_key";
ALTER TABLE ONLY public."Assign_Management_upload" DROP CONSTRAINT "Assign_Management_upload_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_upload" DROP CONSTRAINT "Assign_Management_exam_upload_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_tracker" DROP CONSTRAINT "Assign_Management_exam_tracker_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_score" DROP CONSTRAINT "Assign_Management_exam_score_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_quiz" DROP CONSTRAINT "Assign_Management_exam_quiz_title_key";
ALTER TABLE ONLY public."Assign_Management_exam_quiz" DROP CONSTRAINT "Assign_Management_exam_quiz_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_data" DROP CONSTRAINT "Assign_Management_exam_data_pkey";
ALTER TABLE ONLY public."Assign_Management_exam_data" DROP CONSTRAINT "Assign_Management_exam_data_name_key";
ALTER TABLE ONLY public."Assign_Management_category" DROP CONSTRAINT "Assign_Management_category_pkey";
ALTER TABLE ONLY public."Assign_Management_category" DROP CONSTRAINT "Assign_Management_category_name_key";
ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."LogIn_Management_user_user_permissions" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."LogIn_Management_user_groups" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."LogIn_Management_profile" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_quiztracker" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_quiztimer" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_quizstatus" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_quizscore" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_quiz" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_classroom_user" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Class_Management_classroom" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_upload" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_exam_upload" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_exam_tracker" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_exam_score" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_exam_quiz" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_exam_data" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public."Assign_Management_category" ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.django_session;
DROP SEQUENCE public.django_migrations_id_seq;
DROP TABLE public.django_migrations;
DROP SEQUENCE public.django_content_type_id_seq;
DROP TABLE public.django_content_type;
DROP SEQUENCE public.django_admin_log_id_seq;
DROP TABLE public.django_admin_log;
DROP SEQUENCE public.auth_permission_id_seq;
DROP TABLE public.auth_permission;
DROP SEQUENCE public.auth_group_permissions_id_seq;
DROP TABLE public.auth_group_permissions;
DROP SEQUENCE public.auth_group_id_seq;
DROP TABLE public.auth_group;
DROP SEQUENCE public."LogIn_Management_user_user_permissions_id_seq";
DROP TABLE public."LogIn_Management_user_user_permissions";
DROP SEQUENCE public."LogIn_Management_user_groups_id_seq";
DROP TABLE public."LogIn_Management_user_groups";
DROP TABLE public."LogIn_Management_user";
DROP SEQUENCE public."LogIn_Management_profile_id_seq";
DROP TABLE public."LogIn_Management_profile";
DROP SEQUENCE public."Class_Management_quiztracker_id_seq";
DROP TABLE public."Class_Management_quiztracker";
DROP SEQUENCE public."Class_Management_quiztimer_id_seq";
DROP TABLE public."Class_Management_quiztimer";
DROP SEQUENCE public."Class_Management_quizstatus_id_seq";
DROP TABLE public."Class_Management_quizstatus";
DROP SEQUENCE public."Class_Management_quizscore_id_seq";
DROP TABLE public."Class_Management_quizscore";
DROP SEQUENCE public."Class_Management_quiz_id_seq";
DROP TABLE public."Class_Management_quiz";
DROP SEQUENCE public."Class_Management_classroom_user_id_seq";
DROP TABLE public."Class_Management_classroom_user";
DROP SEQUENCE public."Class_Management_classroom_id_seq";
DROP TABLE public."Class_Management_classroom";
DROP SEQUENCE public."Assign_Management_upload_id_seq";
DROP TABLE public."Assign_Management_upload";
DROP SEQUENCE public."Assign_Management_exam_upload_id_seq";
DROP TABLE public."Assign_Management_exam_upload";
DROP SEQUENCE public."Assign_Management_exam_tracker_id_seq";
DROP TABLE public."Assign_Management_exam_tracker";
DROP SEQUENCE public."Assign_Management_exam_score_id_seq";
DROP TABLE public."Assign_Management_exam_score";
DROP SEQUENCE public."Assign_Management_exam_quiz_id_seq";
DROP TABLE public."Assign_Management_exam_quiz";
DROP SEQUENCE public."Assign_Management_exam_data_id_seq";
DROP TABLE public."Assign_Management_exam_data";
DROP SEQUENCE public."Assign_Management_category_id_seq";
DROP TABLE public."Assign_Management_category";
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: Assign_Management_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_category" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(50)
);


ALTER TABLE public."Assign_Management_category" OWNER TO postgres;

--
-- Name: Assign_Management_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_category_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_category_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_category_id_seq" OWNED BY public."Assign_Management_category".id;


--
-- Name: Assign_Management_exam_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_exam_data" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    detail text,
    created timestamp with time zone NOT NULL,
    available timestamp with time zone NOT NULL,
    deadline timestamp with time zone NOT NULL,
    max_score double precision NOT NULL,
    classroom_id integer NOT NULL
);


ALTER TABLE public."Assign_Management_exam_data" OWNER TO postgres;

--
-- Name: Assign_Management_exam_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_exam_data_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_exam_data_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_exam_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_exam_data_id_seq" OWNED BY public."Assign_Management_exam_data".id;


--
-- Name: Assign_Management_exam_quiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_exam_quiz" (
    id integer NOT NULL,
    title character varying(55) NOT NULL,
    detail text,
    created timestamp with time zone NOT NULL,
    mode character varying(100) NOT NULL,
    text_template_content text,
    text_testcode_content text NOT NULL,
    text_testcase_content text NOT NULL,
    category_id integer,
    classroom_id integer NOT NULL
);


ALTER TABLE public."Assign_Management_exam_quiz" OWNER TO postgres;

--
-- Name: Assign_Management_exam_quiz_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_exam_quiz_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_exam_quiz_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_exam_quiz_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_exam_quiz_id_seq" OWNED BY public."Assign_Management_exam_quiz".id;


--
-- Name: Assign_Management_exam_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_exam_score" (
    id integer NOT NULL,
    "passOrFail" double precision,
    total_score double precision,
    max_score double precision,
    code_id integer,
    exam_id integer NOT NULL,
    quiz_id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."Assign_Management_exam_score" OWNER TO postgres;

--
-- Name: Assign_Management_exam_score_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_exam_score_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_exam_score_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_exam_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_exam_score_id_seq" OWNED BY public."Assign_Management_exam_score".id;


--
-- Name: Assign_Management_exam_tracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_exam_tracker" (
    id integer NOT NULL,
    picked character varying(255)[],
    exam_id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."Assign_Management_exam_tracker" OWNER TO postgres;

--
-- Name: Assign_Management_exam_tracker_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_exam_tracker_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_exam_tracker_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_exam_tracker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_exam_tracker_id_seq" OWNED BY public."Assign_Management_exam_tracker".id;


--
-- Name: Assign_Management_exam_upload; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_exam_upload" (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    "Uploadfile" character varying(100) NOT NULL,
    score double precision,
    "uploadTime" timestamp with time zone NOT NULL,
    exam_id integer NOT NULL,
    quiz_id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."Assign_Management_exam_upload" OWNER TO postgres;

--
-- Name: Assign_Management_exam_upload_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_exam_upload_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_exam_upload_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_exam_upload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_exam_upload_id_seq" OWNED BY public."Assign_Management_exam_upload".id;


--
-- Name: Assign_Management_upload; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Assign_Management_upload" (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    "Uploadfile" character varying(100) NOT NULL,
    score double precision,
    "uploadTime" timestamp with time zone NOT NULL,
    classroom_id integer NOT NULL,
    quiz_id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."Assign_Management_upload" OWNER TO postgres;

--
-- Name: Assign_Management_upload_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Assign_Management_upload_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Assign_Management_upload_id_seq" OWNER TO postgres;

--
-- Name: Assign_Management_upload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Assign_Management_upload_id_seq" OWNED BY public."Assign_Management_upload".id;


--
-- Name: Class_Management_classroom; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_classroom" (
    id integer NOT NULL,
    "className" character varying(255) NOT NULL,
    creator_id character varying(255)
);


ALTER TABLE public."Class_Management_classroom" OWNER TO postgres;

--
-- Name: Class_Management_classroom_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_classroom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_classroom_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_classroom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_classroom_id_seq" OWNED BY public."Class_Management_classroom".id;


--
-- Name: Class_Management_classroom_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_classroom_user" (
    id integer NOT NULL,
    classroom_id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."Class_Management_classroom_user" OWNER TO postgres;

--
-- Name: Class_Management_classroom_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_classroom_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_classroom_user_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_classroom_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_classroom_user_id_seq" OWNED BY public."Class_Management_classroom_user".id;


--
-- Name: Class_Management_quiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_quiz" (
    id integer NOT NULL,
    "quizTitle" character varying(55) NOT NULL,
    "quizDetail" text,
    deadline timestamp with time zone NOT NULL,
    available timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    hint character varying(255),
    mode character varying(100) NOT NULL,
    max_score double precision NOT NULL,
    text_template_content text,
    text_testcode_content text NOT NULL,
    text_testcase_content text NOT NULL,
    category_id integer,
    classroom_id integer NOT NULL
);


ALTER TABLE public."Class_Management_quiz" OWNER TO postgres;

--
-- Name: Class_Management_quiz_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_quiz_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_quiz_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_quiz_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_quiz_id_seq" OWNED BY public."Class_Management_quiz".id;


--
-- Name: Class_Management_quizscore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_quizscore" (
    id integer NOT NULL,
    "passOrFail" double precision,
    total_score double precision,
    max_score double precision,
    classroom_id integer NOT NULL,
    code_id integer,
    "quizId_id" integer NOT NULL,
    "userId_id" character varying(255) NOT NULL
);


ALTER TABLE public."Class_Management_quizscore" OWNER TO postgres;

--
-- Name: Class_Management_quizscore_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_quizscore_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_quizscore_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_quizscore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_quizscore_id_seq" OWNED BY public."Class_Management_quizscore".id;


--
-- Name: Class_Management_quizstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_quizstatus" (
    id integer NOT NULL,
    status boolean NOT NULL,
    classroom_id integer NOT NULL,
    "quizId_id" integer NOT NULL,
    "userId_id" character varying(255) NOT NULL
);


ALTER TABLE public."Class_Management_quizstatus" OWNER TO postgres;

--
-- Name: Class_Management_quizstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_quizstatus_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_quizstatus_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_quizstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_quizstatus_id_seq" OWNED BY public."Class_Management_quizstatus".id;


--
-- Name: Class_Management_quiztimer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_quiztimer" (
    id integer NOT NULL,
    timer integer,
    timer_stop timestamp with time zone,
    start boolean NOT NULL,
    classroom_id integer NOT NULL,
    "quizId_id" integer NOT NULL,
    "userId_id" character varying(255) NOT NULL
);


ALTER TABLE public."Class_Management_quiztimer" OWNER TO postgres;

--
-- Name: Class_Management_quiztimer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_quiztimer_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_quiztimer_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_quiztimer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_quiztimer_id_seq" OWNED BY public."Class_Management_quiztimer".id;


--
-- Name: Class_Management_quiztracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Class_Management_quiztracker" (
    id integer NOT NULL,
    "quizDoneCount" smallint NOT NULL,
    classroom_id integer NOT NULL,
    "userId_id" character varying(255) NOT NULL,
    CONSTRAINT "Class_Management_quiztracker_quizDoneCount_check" CHECK (("quizDoneCount" >= 0))
);


ALTER TABLE public."Class_Management_quiztracker" OWNER TO postgres;

--
-- Name: Class_Management_quiztracker_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Class_Management_quiztracker_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Class_Management_quiztracker_id_seq" OWNER TO postgres;

--
-- Name: Class_Management_quiztracker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Class_Management_quiztracker_id_seq" OWNED BY public."Class_Management_quiztracker".id;


--
-- Name: LogIn_Management_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."LogIn_Management_profile" (
    id integer NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public."LogIn_Management_profile" OWNER TO postgres;

--
-- Name: LogIn_Management_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."LogIn_Management_profile_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."LogIn_Management_profile_id_seq" OWNER TO postgres;

--
-- Name: LogIn_Management_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."LogIn_Management_profile_id_seq" OWNED BY public."LogIn_Management_profile".id;


--
-- Name: LogIn_Management_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."LogIn_Management_user" (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(255) NOT NULL,
    "userId" character varying(255) NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_admin boolean NOT NULL
);


ALTER TABLE public."LogIn_Management_user" OWNER TO postgres;

--
-- Name: LogIn_Management_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."LogIn_Management_user_groups" (
    id integer NOT NULL,
    user_id character varying(255) NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public."LogIn_Management_user_groups" OWNER TO postgres;

--
-- Name: LogIn_Management_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."LogIn_Management_user_groups_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."LogIn_Management_user_groups_id_seq" OWNER TO postgres;

--
-- Name: LogIn_Management_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."LogIn_Management_user_groups_id_seq" OWNED BY public."LogIn_Management_user_groups".id;


--
-- Name: LogIn_Management_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."LogIn_Management_user_user_permissions" (
    id integer NOT NULL,
    user_id character varying(255) NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public."LogIn_Management_user_user_permissions" OWNER TO postgres;

--
-- Name: LogIn_Management_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."LogIn_Management_user_user_permissions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."LogIn_Management_user_user_permissions_id_seq" OWNER TO postgres;

--
-- Name: LogIn_Management_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."LogIn_Management_user_user_permissions_id_seq" OWNED BY public."LogIn_Management_user_user_permissions".id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id character varying(255) NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: Assign_Management_category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_category" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_category_id_seq"'::regclass);


--
-- Name: Assign_Management_exam_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_data" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_exam_data_id_seq"'::regclass);


--
-- Name: Assign_Management_exam_quiz id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_quiz" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_exam_quiz_id_seq"'::regclass);


--
-- Name: Assign_Management_exam_score id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_exam_score_id_seq"'::regclass);


--
-- Name: Assign_Management_exam_tracker id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_tracker" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_exam_tracker_id_seq"'::regclass);


--
-- Name: Assign_Management_exam_upload id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_upload" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_exam_upload_id_seq"'::regclass);


--
-- Name: Assign_Management_upload id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_upload" ALTER COLUMN id SET DEFAULT nextval('public."Assign_Management_upload_id_seq"'::regclass);


--
-- Name: Class_Management_classroom id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_classroom_id_seq"'::regclass);


--
-- Name: Class_Management_classroom_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom_user" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_classroom_user_id_seq"'::regclass);


--
-- Name: Class_Management_quiz id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiz" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_quiz_id_seq"'::regclass);


--
-- Name: Class_Management_quizscore id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_quizscore_id_seq"'::regclass);


--
-- Name: Class_Management_quizstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizstatus" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_quizstatus_id_seq"'::regclass);


--
-- Name: Class_Management_quiztimer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztimer" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_quiztimer_id_seq"'::regclass);


--
-- Name: Class_Management_quiztracker id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztracker" ALTER COLUMN id SET DEFAULT nextval('public."Class_Management_quiztracker_id_seq"'::regclass);


--
-- Name: LogIn_Management_profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_profile" ALTER COLUMN id SET DEFAULT nextval('public."LogIn_Management_profile_id_seq"'::regclass);


--
-- Name: LogIn_Management_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_groups" ALTER COLUMN id SET DEFAULT nextval('public."LogIn_Management_user_groups_id_seq"'::regclass);


--
-- Name: LogIn_Management_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_user_permissions" ALTER COLUMN id SET DEFAULT nextval('public."LogIn_Management_user_user_permissions_id_seq"'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: Assign_Management_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_category" (id, name, slug) FROM stdin;
\.


--
-- Data for Name: Assign_Management_exam_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_exam_data" (id, name, detail, created, available, deadline, max_score, classroom_id) FROM stdin;
\.


--
-- Data for Name: Assign_Management_exam_quiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_exam_quiz" (id, title, detail, created, mode, text_template_content, text_testcode_content, text_testcase_content, category_id, classroom_id) FROM stdin;
\.


--
-- Data for Name: Assign_Management_exam_score; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_exam_score" (id, "passOrFail", total_score, max_score, code_id, exam_id, quiz_id, user_id) FROM stdin;
\.


--
-- Data for Name: Assign_Management_exam_tracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_exam_tracker" (id, picked, exam_id, user_id) FROM stdin;
\.


--
-- Data for Name: Assign_Management_exam_upload; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_exam_upload" (id, title, "Uploadfile", score, "uploadTime", exam_id, quiz_id, user_id) FROM stdin;
\.


--
-- Data for Name: Assign_Management_upload; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Assign_Management_upload" (id, title, "Uploadfile", score, "uploadTime", classroom_id, quiz_id, user_id) FROM stdin;
\.


--
-- Data for Name: Class_Management_classroom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_classroom" (id, "className", creator_id) FROM stdin;
1	FRA141	pengza79
\.


--
-- Data for Name: Class_Management_classroom_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_classroom_user" (id, classroom_id, user_id) FROM stdin;
1	1	pengza79
\.


--
-- Data for Name: Class_Management_quiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_quiz" (id, "quizTitle", "quizDetail", deadline, available, created, hint, mode, max_score, text_template_content, text_testcode_content, text_testcase_content, category_id, classroom_id) FROM stdin;
\.


--
-- Data for Name: Class_Management_quizscore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_quizscore" (id, "passOrFail", total_score, max_score, classroom_id, code_id, "quizId_id", "userId_id") FROM stdin;
\.


--
-- Data for Name: Class_Management_quizstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_quizstatus" (id, status, classroom_id, "quizId_id", "userId_id") FROM stdin;
\.


--
-- Data for Name: Class_Management_quiztimer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_quiztimer" (id, timer, timer_stop, start, classroom_id, "quizId_id", "userId_id") FROM stdin;
\.


--
-- Data for Name: Class_Management_quiztracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Class_Management_quiztracker" (id, "quizDoneCount", classroom_id, "userId_id") FROM stdin;
1	0	1	pengza79
\.


--
-- Data for Name: LogIn_Management_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."LogIn_Management_profile" (id, user_id) FROM stdin;
\.


--
-- Data for Name: LogIn_Management_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."LogIn_Management_user" (password, last_login, is_superuser, email, "userId", first_name, last_name, is_active, is_staff, is_admin) FROM stdin;
pbkdf2_sha256$100000$wPEqIkHFNXX4$0UL5vUCEDJTTqNKPNj3zcqL8YlFdAl0R0Y4QFCVctDY=	2018-09-29 11:11:53.775955+00	f	rsxs981@gmail.com	pengza79	Natworpong	Loyswai	t	t	t
\.


--
-- Data for Name: LogIn_Management_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."LogIn_Management_user_groups" (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: LogIn_Management_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."LogIn_Management_user_user_permissions" (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
1	FRA141_Teacher
2	FRA141_TA
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add profile	6	add_profile
17	Can change profile	6	change_profile
18	Can delete profile	6	delete_profile
19	Can add user	7	add_user
20	Can change user	7	change_user
21	Can delete user	7	delete_user
22	Can add class room	8	add_classroom
23	Can change class room	8	change_classroom
24	Can delete class room	8	delete_classroom
25	Can add quiz	9	add_quiz
26	Can change quiz	9	change_quiz
27	Can delete quiz	9	delete_quiz
28	Can add quiz score	10	add_quizscore
29	Can change quiz score	10	change_quizscore
30	Can delete quiz score	10	delete_quizscore
31	Can add quiz status	11	add_quizstatus
32	Can change quiz status	11	change_quizstatus
33	Can delete quiz status	11	delete_quizstatus
34	Can add quiz timer	12	add_quiztimer
35	Can change quiz timer	12	change_quiztimer
36	Can delete quiz timer	12	delete_quiztimer
37	Can add quiz tracker	13	add_quiztracker
38	Can change quiz tracker	13	change_quiztracker
39	Can delete quiz tracker	13	delete_quiztracker
40	Can add category	14	add_category
41	Can change category	14	change_category
42	Can delete category	14	delete_category
43	Can add exam_ data	15	add_exam_data
44	Can change exam_ data	15	change_exam_data
45	Can delete exam_ data	15	delete_exam_data
46	Can add exam_ quiz	16	add_exam_quiz
47	Can change exam_ quiz	16	change_exam_quiz
48	Can delete exam_ quiz	16	delete_exam_quiz
49	Can add exam_ score	17	add_exam_score
50	Can change exam_ score	17	change_exam_score
51	Can delete exam_ score	17	delete_exam_score
52	Can add exam_ tracker	18	add_exam_tracker
53	Can change exam_ tracker	18	change_exam_tracker
54	Can delete exam_ tracker	18	delete_exam_tracker
55	Can add exam_ upload	19	add_exam_upload
56	Can change exam_ upload	19	change_exam_upload
57	Can delete exam_ upload	19	delete_exam_upload
58	Can add upload	20	add_upload
59	Can change upload	20	change_upload
60	Can delete upload	20	delete_upload
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	LogIn_Management	profile
7	LogIn_Management	user
8	Class_Management	classroom
9	Class_Management	quiz
10	Class_Management	quizscore
11	Class_Management	quizstatus
12	Class_Management	quiztimer
13	Class_Management	quiztracker
14	Assign_Management	category
15	Assign_Management	exam_data
16	Assign_Management	exam_quiz
17	Assign_Management	exam_score
18	Assign_Management	exam_tracker
19	Assign_Management	exam_upload
20	Assign_Management	upload
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2018-09-29 11:07:43.106005+00
2	contenttypes	0002_remove_content_type_name	2018-09-29 11:07:43.116787+00
3	auth	0001_initial	2018-09-29 11:07:43.186898+00
4	auth	0002_alter_permission_name_max_length	2018-09-29 11:07:43.194608+00
5	auth	0003_alter_user_email_max_length	2018-09-29 11:07:43.201674+00
6	auth	0004_alter_user_username_opts	2018-09-29 11:07:43.20825+00
7	auth	0005_alter_user_last_login_null	2018-09-29 11:07:43.214619+00
8	auth	0006_require_contenttypes_0002	2018-09-29 11:07:43.217884+00
9	auth	0007_alter_validators_add_error_messages	2018-09-29 11:07:43.227168+00
10	auth	0008_alter_user_username_max_length	2018-09-29 11:07:43.234753+00
11	auth	0009_alter_user_last_name_max_length	2018-09-29 11:07:43.241498+00
12	LogIn_Management	0001_initial	2018-09-29 11:07:43.333941+00
13	Class_Management	0001_initial	2018-09-29 11:07:43.406038+00
14	Assign_Management	0001_initial	2018-09-29 11:07:43.489912+00
15	Assign_Management	0002_auto_20180925_1648	2018-09-29 11:07:43.515719+00
16	Assign_Management	0003_auto_20180925_1648	2018-09-29 11:07:43.815427+00
17	Class_Management	0002_auto_20180925_1648	2018-09-29 11:07:45.784639+00
18	admin	0001_initial	2018-09-29 11:07:45.875573+00
19	admin	0002_logentry_remove_auto_add	2018-09-29 11:07:45.897921+00
20	sessions	0001_initial	2018-09-29 11:07:45.927363+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
e1ysltxnaesfwo7bin46kzpvlz1ymst4	MmU1N2Q5ZmRjY2UzNDA3MWEyNzIxNzcwMmNiZGExMTgwNmRiNjMzOTp7Il9hdXRoX3VzZXJfaWQiOiJwZW5nemE3OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjRlZDUwMmM0NDhkYzI4NDEyNTg2ZmNmYWFkMmVmOTMzZjllMjFjYyIsImNsYXNzcm9vbSI6IkZSQTE0MSIsInF1aXoiOltdfQ==	2018-09-29 12:12:01.085111+00
\.


--
-- Name: Assign_Management_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_category_id_seq"', 1, false);


--
-- Name: Assign_Management_exam_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_exam_data_id_seq"', 1, true);


--
-- Name: Assign_Management_exam_quiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_exam_quiz_id_seq"', 1, false);


--
-- Name: Assign_Management_exam_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_exam_score_id_seq"', 1, false);


--
-- Name: Assign_Management_exam_tracker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_exam_tracker_id_seq"', 1, true);


--
-- Name: Assign_Management_exam_upload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_exam_upload_id_seq"', 1, false);


--
-- Name: Assign_Management_upload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Assign_Management_upload_id_seq"', 1, false);


--
-- Name: Class_Management_classroom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_classroom_id_seq"', 1, true);


--
-- Name: Class_Management_classroom_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_classroom_user_id_seq"', 1, true);


--
-- Name: Class_Management_quiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_quiz_id_seq"', 1, false);


--
-- Name: Class_Management_quizscore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_quizscore_id_seq"', 1, false);


--
-- Name: Class_Management_quizstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_quizstatus_id_seq"', 1, false);


--
-- Name: Class_Management_quiztimer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_quiztimer_id_seq"', 1, false);


--
-- Name: Class_Management_quiztracker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Class_Management_quiztracker_id_seq"', 1, true);


--
-- Name: LogIn_Management_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."LogIn_Management_profile_id_seq"', 1, false);


--
-- Name: LogIn_Management_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."LogIn_Management_user_groups_id_seq"', 1, false);


--
-- Name: LogIn_Management_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."LogIn_Management_user_user_permissions_id_seq"', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 2, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 20, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: Assign_Management_category Assign_Management_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_category"
    ADD CONSTRAINT "Assign_Management_category_name_key" UNIQUE (name);


--
-- Name: Assign_Management_category Assign_Management_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_category"
    ADD CONSTRAINT "Assign_Management_category_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_exam_data Assign_Management_exam_data_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_data"
    ADD CONSTRAINT "Assign_Management_exam_data_name_key" UNIQUE (name);


--
-- Name: Assign_Management_exam_data Assign_Management_exam_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_data"
    ADD CONSTRAINT "Assign_Management_exam_data_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_exam_quiz Assign_Management_exam_quiz_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_quiz"
    ADD CONSTRAINT "Assign_Management_exam_quiz_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_exam_quiz Assign_Management_exam_quiz_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_quiz"
    ADD CONSTRAINT "Assign_Management_exam_quiz_title_key" UNIQUE (title);


--
-- Name: Assign_Management_exam_score Assign_Management_exam_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score"
    ADD CONSTRAINT "Assign_Management_exam_score_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_exam_tracker Assign_Management_exam_tracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_tracker"
    ADD CONSTRAINT "Assign_Management_exam_tracker_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_exam_upload Assign_Management_exam_upload_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_upload"
    ADD CONSTRAINT "Assign_Management_exam_upload_pkey" PRIMARY KEY (id);


--
-- Name: Assign_Management_upload Assign_Management_upload_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_upload"
    ADD CONSTRAINT "Assign_Management_upload_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_classroom Class_Management_classroom_className_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom"
    ADD CONSTRAINT "Class_Management_classroom_className_key" UNIQUE ("className");


--
-- Name: Class_Management_classroom Class_Management_classroom_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom"
    ADD CONSTRAINT "Class_Management_classroom_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_classroom_user Class_Management_classroom_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom_user"
    ADD CONSTRAINT "Class_Management_classroom_user_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_quiz Class_Management_quiz_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiz"
    ADD CONSTRAINT "Class_Management_quiz_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_quiz Class_Management_quiz_quizTitle_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiz"
    ADD CONSTRAINT "Class_Management_quiz_quizTitle_key" UNIQUE ("quizTitle");


--
-- Name: Class_Management_quizscore Class_Management_quizscore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore"
    ADD CONSTRAINT "Class_Management_quizscore_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_quizstatus Class_Management_quizstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizstatus"
    ADD CONSTRAINT "Class_Management_quizstatus_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_quiztimer Class_Management_quiztimer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztimer"
    ADD CONSTRAINT "Class_Management_quiztimer_pkey" PRIMARY KEY (id);


--
-- Name: Class_Management_quiztracker Class_Management_quiztracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztracker"
    ADD CONSTRAINT "Class_Management_quiztracker_pkey" PRIMARY KEY (id);


--
-- Name: LogIn_Management_profile LogIn_Management_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_profile"
    ADD CONSTRAINT "LogIn_Management_profile_pkey" PRIMARY KEY (id);


--
-- Name: LogIn_Management_profile LogIn_Management_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_profile"
    ADD CONSTRAINT "LogIn_Management_profile_user_id_key" UNIQUE (user_id);


--
-- Name: LogIn_Management_user LogIn_Management_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user"
    ADD CONSTRAINT "LogIn_Management_user_email_key" UNIQUE (email);


--
-- Name: LogIn_Management_user_groups LogIn_Management_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_groups"
    ADD CONSTRAINT "LogIn_Management_user_groups_pkey" PRIMARY KEY (id);


--
-- Name: LogIn_Management_user LogIn_Management_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user"
    ADD CONSTRAINT "LogIn_Management_user_pkey" PRIMARY KEY ("userId");


--
-- Name: LogIn_Management_user_user_permissions LogIn_Management_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_user_permissions"
    ADD CONSTRAINT "LogIn_Management_user_user_permissions_pkey" PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: Class_Management_classroom_user class_management_classro_classroom_id_user_id_1bd666e7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom_user"
    ADD CONSTRAINT class_management_classro_classroom_id_user_id_1bd666e7_uniq UNIQUE (classroom_id, user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: LogIn_Management_user_groups login_management_user_groups_user_id_group_id_7aef063c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_groups"
    ADD CONSTRAINT login_management_user_groups_user_id_group_id_7aef063c_uniq UNIQUE (user_id, group_id);


--
-- Name: LogIn_Management_user_user_permissions login_management_user_us_user_id_permission_id_0b8ef45b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_user_permissions"
    ADD CONSTRAINT login_management_user_us_user_id_permission_id_0b8ef45b_uniq UNIQUE (user_id, permission_id);


--
-- Name: Assign_Management_category_name_689b6d4f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_category_name_689b6d4f_like" ON public."Assign_Management_category" USING btree (name varchar_pattern_ops);


--
-- Name: Assign_Management_category_slug_11c45a1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_category_slug_11c45a1c" ON public."Assign_Management_category" USING btree (slug);


--
-- Name: Assign_Management_category_slug_11c45a1c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_category_slug_11c45a1c_like" ON public."Assign_Management_category" USING btree (slug varchar_pattern_ops);


--
-- Name: Assign_Management_exam_data_classroom_id_6210e067; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_data_classroom_id_6210e067" ON public."Assign_Management_exam_data" USING btree (classroom_id);


--
-- Name: Assign_Management_exam_data_name_e1b3d6e1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_data_name_e1b3d6e1_like" ON public."Assign_Management_exam_data" USING btree (name varchar_pattern_ops);


--
-- Name: Assign_Management_exam_quiz_category_id_397f7051; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_quiz_category_id_397f7051" ON public."Assign_Management_exam_quiz" USING btree (category_id);


--
-- Name: Assign_Management_exam_quiz_classroom_id_f9849c51; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_quiz_classroom_id_f9849c51" ON public."Assign_Management_exam_quiz" USING btree (classroom_id);


--
-- Name: Assign_Management_exam_quiz_title_d1eabc33_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_quiz_title_d1eabc33_like" ON public."Assign_Management_exam_quiz" USING btree (title varchar_pattern_ops);


--
-- Name: Assign_Management_exam_score_code_id_74cab813; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_score_code_id_74cab813" ON public."Assign_Management_exam_score" USING btree (code_id);


--
-- Name: Assign_Management_exam_score_exam_id_60b75b4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_score_exam_id_60b75b4f" ON public."Assign_Management_exam_score" USING btree (exam_id);


--
-- Name: Assign_Management_exam_score_quiz_id_92b87429; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_score_quiz_id_92b87429" ON public."Assign_Management_exam_score" USING btree (quiz_id);


--
-- Name: Assign_Management_exam_score_user_id_0bc5be8f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_score_user_id_0bc5be8f" ON public."Assign_Management_exam_score" USING btree (user_id);


--
-- Name: Assign_Management_exam_score_user_id_0bc5be8f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_score_user_id_0bc5be8f_like" ON public."Assign_Management_exam_score" USING btree (user_id varchar_pattern_ops);


--
-- Name: Assign_Management_exam_tracker_exam_id_4fcc5756; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_tracker_exam_id_4fcc5756" ON public."Assign_Management_exam_tracker" USING btree (exam_id);


--
-- Name: Assign_Management_exam_tracker_user_id_80f22c59; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_tracker_user_id_80f22c59" ON public."Assign_Management_exam_tracker" USING btree (user_id);


--
-- Name: Assign_Management_exam_tracker_user_id_80f22c59_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_tracker_user_id_80f22c59_like" ON public."Assign_Management_exam_tracker" USING btree (user_id varchar_pattern_ops);


--
-- Name: Assign_Management_exam_upload_exam_id_fb709bca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_upload_exam_id_fb709bca" ON public."Assign_Management_exam_upload" USING btree (exam_id);


--
-- Name: Assign_Management_exam_upload_quiz_id_4ec79334; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_upload_quiz_id_4ec79334" ON public."Assign_Management_exam_upload" USING btree (quiz_id);


--
-- Name: Assign_Management_exam_upload_user_id_1ddfb625; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_upload_user_id_1ddfb625" ON public."Assign_Management_exam_upload" USING btree (user_id);


--
-- Name: Assign_Management_exam_upload_user_id_1ddfb625_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_exam_upload_user_id_1ddfb625_like" ON public."Assign_Management_exam_upload" USING btree (user_id varchar_pattern_ops);


--
-- Name: Assign_Management_upload_classroom_id_0557a92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_upload_classroom_id_0557a92e" ON public."Assign_Management_upload" USING btree (classroom_id);


--
-- Name: Assign_Management_upload_quiz_id_baaf6fdf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_upload_quiz_id_baaf6fdf" ON public."Assign_Management_upload" USING btree (quiz_id);


--
-- Name: Assign_Management_upload_user_id_da31c61f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_upload_user_id_da31c61f" ON public."Assign_Management_upload" USING btree (user_id);


--
-- Name: Assign_Management_upload_user_id_da31c61f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Assign_Management_upload_user_id_da31c61f_like" ON public."Assign_Management_upload" USING btree (user_id varchar_pattern_ops);


--
-- Name: Class_Management_classroom_className_36a9972e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_className_36a9972e_like" ON public."Class_Management_classroom" USING btree ("className" varchar_pattern_ops);


--
-- Name: Class_Management_classroom_creator_id_9361d351; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_creator_id_9361d351" ON public."Class_Management_classroom" USING btree (creator_id);


--
-- Name: Class_Management_classroom_creator_id_9361d351_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_creator_id_9361d351_like" ON public."Class_Management_classroom" USING btree (creator_id varchar_pattern_ops);


--
-- Name: Class_Management_classroom_user_classroom_id_d3bf0654; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_user_classroom_id_d3bf0654" ON public."Class_Management_classroom_user" USING btree (classroom_id);


--
-- Name: Class_Management_classroom_user_user_id_bbbf76f7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_user_user_id_bbbf76f7" ON public."Class_Management_classroom_user" USING btree (user_id);


--
-- Name: Class_Management_classroom_user_user_id_bbbf76f7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_classroom_user_user_id_bbbf76f7_like" ON public."Class_Management_classroom_user" USING btree (user_id varchar_pattern_ops);


--
-- Name: Class_Management_quiz_category_id_1fe0e92b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiz_category_id_1fe0e92b" ON public."Class_Management_quiz" USING btree (category_id);


--
-- Name: Class_Management_quiz_classroom_id_3dfc1262; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiz_classroom_id_3dfc1262" ON public."Class_Management_quiz" USING btree (classroom_id);


--
-- Name: Class_Management_quiz_quizTitle_3aacd799_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiz_quizTitle_3aacd799_like" ON public."Class_Management_quiz" USING btree ("quizTitle" varchar_pattern_ops);


--
-- Name: Class_Management_quizscore_classroom_id_059aa3a7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizscore_classroom_id_059aa3a7" ON public."Class_Management_quizscore" USING btree (classroom_id);


--
-- Name: Class_Management_quizscore_code_id_1c65dd40; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizscore_code_id_1c65dd40" ON public."Class_Management_quizscore" USING btree (code_id);


--
-- Name: Class_Management_quizscore_quizId_id_ed1c425f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizscore_quizId_id_ed1c425f" ON public."Class_Management_quizscore" USING btree ("quizId_id");


--
-- Name: Class_Management_quizscore_userId_id_9f1d0641; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizscore_userId_id_9f1d0641" ON public."Class_Management_quizscore" USING btree ("userId_id");


--
-- Name: Class_Management_quizscore_userId_id_9f1d0641_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizscore_userId_id_9f1d0641_like" ON public."Class_Management_quizscore" USING btree ("userId_id" varchar_pattern_ops);


--
-- Name: Class_Management_quizstatus_classroom_id_5bbf9c63; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizstatus_classroom_id_5bbf9c63" ON public."Class_Management_quizstatus" USING btree (classroom_id);


--
-- Name: Class_Management_quizstatus_quizId_id_8375504c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizstatus_quizId_id_8375504c" ON public."Class_Management_quizstatus" USING btree ("quizId_id");


--
-- Name: Class_Management_quizstatus_userId_id_00a1707d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizstatus_userId_id_00a1707d" ON public."Class_Management_quizstatus" USING btree ("userId_id");


--
-- Name: Class_Management_quizstatus_userId_id_00a1707d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quizstatus_userId_id_00a1707d_like" ON public."Class_Management_quizstatus" USING btree ("userId_id" varchar_pattern_ops);


--
-- Name: Class_Management_quiztimer_classroom_id_4baabc98; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztimer_classroom_id_4baabc98" ON public."Class_Management_quiztimer" USING btree (classroom_id);


--
-- Name: Class_Management_quiztimer_quizId_id_e7fb481d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztimer_quizId_id_e7fb481d" ON public."Class_Management_quiztimer" USING btree ("quizId_id");


--
-- Name: Class_Management_quiztimer_userId_id_3089c57e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztimer_userId_id_3089c57e" ON public."Class_Management_quiztimer" USING btree ("userId_id");


--
-- Name: Class_Management_quiztimer_userId_id_3089c57e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztimer_userId_id_3089c57e_like" ON public."Class_Management_quiztimer" USING btree ("userId_id" varchar_pattern_ops);


--
-- Name: Class_Management_quiztracker_classroom_id_83db111b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztracker_classroom_id_83db111b" ON public."Class_Management_quiztracker" USING btree (classroom_id);


--
-- Name: Class_Management_quiztracker_userId_id_95b7aa39; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztracker_userId_id_95b7aa39" ON public."Class_Management_quiztracker" USING btree ("userId_id");


--
-- Name: Class_Management_quiztracker_userId_id_95b7aa39_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Class_Management_quiztracker_userId_id_95b7aa39_like" ON public."Class_Management_quiztracker" USING btree ("userId_id" varchar_pattern_ops);


--
-- Name: LogIn_Management_profile_user_id_8450ccb2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_profile_user_id_8450ccb2_like" ON public."LogIn_Management_profile" USING btree (user_id varchar_pattern_ops);


--
-- Name: LogIn_Management_user_email_a9e4c25f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_email_a9e4c25f_like" ON public."LogIn_Management_user" USING btree (email varchar_pattern_ops);


--
-- Name: LogIn_Management_user_groups_group_id_84db3e0e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_groups_group_id_84db3e0e" ON public."LogIn_Management_user_groups" USING btree (group_id);


--
-- Name: LogIn_Management_user_groups_user_id_a7e13076; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_groups_user_id_a7e13076" ON public."LogIn_Management_user_groups" USING btree (user_id);


--
-- Name: LogIn_Management_user_groups_user_id_a7e13076_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_groups_user_id_a7e13076_like" ON public."LogIn_Management_user_groups" USING btree (user_id varchar_pattern_ops);


--
-- Name: LogIn_Management_user_userId_d1cecdac_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_userId_d1cecdac_like" ON public."LogIn_Management_user" USING btree ("userId" varchar_pattern_ops);


--
-- Name: LogIn_Management_user_user_permissions_permission_id_9b1826c8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_user_permissions_permission_id_9b1826c8" ON public."LogIn_Management_user_user_permissions" USING btree (permission_id);


--
-- Name: LogIn_Management_user_user_permissions_user_id_08db02bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_user_permissions_user_id_08db02bd" ON public."LogIn_Management_user_user_permissions" USING btree (user_id);


--
-- Name: LogIn_Management_user_user_permissions_user_id_08db02bd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "LogIn_Management_user_user_permissions_user_id_08db02bd_like" ON public."LogIn_Management_user_user_permissions" USING btree (user_id varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_admin_log_user_id_c564eba6_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6_like ON public.django_admin_log USING btree (user_id varchar_pattern_ops);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: Assign_Management_exam_quiz Assign_Management_ex_category_id_397f7051_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_quiz"
    ADD CONSTRAINT "Assign_Management_ex_category_id_397f7051_fk_Assign_Ma" FOREIGN KEY (category_id) REFERENCES public."Assign_Management_category"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_data Assign_Management_ex_classroom_id_6210e067_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_data"
    ADD CONSTRAINT "Assign_Management_ex_classroom_id_6210e067_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_quiz Assign_Management_ex_classroom_id_f9849c51_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_quiz"
    ADD CONSTRAINT "Assign_Management_ex_classroom_id_f9849c51_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_score Assign_Management_ex_code_id_74cab813_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score"
    ADD CONSTRAINT "Assign_Management_ex_code_id_74cab813_fk_Assign_Ma" FOREIGN KEY (code_id) REFERENCES public."Assign_Management_exam_upload"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_tracker Assign_Management_ex_exam_id_4fcc5756_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_tracker"
    ADD CONSTRAINT "Assign_Management_ex_exam_id_4fcc5756_fk_Assign_Ma" FOREIGN KEY (exam_id) REFERENCES public."Assign_Management_exam_data"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_score Assign_Management_ex_exam_id_60b75b4f_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score"
    ADD CONSTRAINT "Assign_Management_ex_exam_id_60b75b4f_fk_Assign_Ma" FOREIGN KEY (exam_id) REFERENCES public."Assign_Management_exam_data"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_upload Assign_Management_ex_exam_id_fb709bca_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_upload"
    ADD CONSTRAINT "Assign_Management_ex_exam_id_fb709bca_fk_Assign_Ma" FOREIGN KEY (exam_id) REFERENCES public."Assign_Management_exam_data"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_upload Assign_Management_ex_quiz_id_4ec79334_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_upload"
    ADD CONSTRAINT "Assign_Management_ex_quiz_id_4ec79334_fk_Assign_Ma" FOREIGN KEY (quiz_id) REFERENCES public."Assign_Management_exam_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_score Assign_Management_ex_quiz_id_92b87429_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score"
    ADD CONSTRAINT "Assign_Management_ex_quiz_id_92b87429_fk_Assign_Ma" FOREIGN KEY (quiz_id) REFERENCES public."Assign_Management_exam_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_score Assign_Management_ex_user_id_0bc5be8f_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_score"
    ADD CONSTRAINT "Assign_Management_ex_user_id_0bc5be8f_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_upload Assign_Management_ex_user_id_1ddfb625_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_upload"
    ADD CONSTRAINT "Assign_Management_ex_user_id_1ddfb625_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_exam_tracker Assign_Management_ex_user_id_80f22c59_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_exam_tracker"
    ADD CONSTRAINT "Assign_Management_ex_user_id_80f22c59_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_upload Assign_Management_up_classroom_id_0557a92e_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_upload"
    ADD CONSTRAINT "Assign_Management_up_classroom_id_0557a92e_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_upload Assign_Management_up_quiz_id_baaf6fdf_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_upload"
    ADD CONSTRAINT "Assign_Management_up_quiz_id_baaf6fdf_fk_Class_Man" FOREIGN KEY (quiz_id) REFERENCES public."Class_Management_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Assign_Management_upload Assign_Management_up_user_id_da31c61f_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Assign_Management_upload"
    ADD CONSTRAINT "Assign_Management_up_user_id_da31c61f_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_classroom_user Class_Management_cla_classroom_id_d3bf0654_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom_user"
    ADD CONSTRAINT "Class_Management_cla_classroom_id_d3bf0654_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_classroom Class_Management_cla_creator_id_9361d351_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom"
    ADD CONSTRAINT "Class_Management_cla_creator_id_9361d351_fk_LogIn_Man" FOREIGN KEY (creator_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_classroom_user Class_Management_cla_user_id_bbbf76f7_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_classroom_user"
    ADD CONSTRAINT "Class_Management_cla_user_id_bbbf76f7_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiz Class_Management_qui_category_id_1fe0e92b_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiz"
    ADD CONSTRAINT "Class_Management_qui_category_id_1fe0e92b_fk_Assign_Ma" FOREIGN KEY (category_id) REFERENCES public."Assign_Management_category"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizscore Class_Management_qui_classroom_id_059aa3a7_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore"
    ADD CONSTRAINT "Class_Management_qui_classroom_id_059aa3a7_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiz Class_Management_qui_classroom_id_3dfc1262_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiz"
    ADD CONSTRAINT "Class_Management_qui_classroom_id_3dfc1262_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiztimer Class_Management_qui_classroom_id_4baabc98_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztimer"
    ADD CONSTRAINT "Class_Management_qui_classroom_id_4baabc98_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizstatus Class_Management_qui_classroom_id_5bbf9c63_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizstatus"
    ADD CONSTRAINT "Class_Management_qui_classroom_id_5bbf9c63_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiztracker Class_Management_qui_classroom_id_83db111b_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztracker"
    ADD CONSTRAINT "Class_Management_qui_classroom_id_83db111b_fk_Class_Man" FOREIGN KEY (classroom_id) REFERENCES public."Class_Management_classroom"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizscore Class_Management_qui_code_id_1c65dd40_fk_Assign_Ma; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore"
    ADD CONSTRAINT "Class_Management_qui_code_id_1c65dd40_fk_Assign_Ma" FOREIGN KEY (code_id) REFERENCES public."Assign_Management_upload"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizstatus Class_Management_qui_quizId_id_8375504c_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizstatus"
    ADD CONSTRAINT "Class_Management_qui_quizId_id_8375504c_fk_Class_Man" FOREIGN KEY ("quizId_id") REFERENCES public."Class_Management_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiztimer Class_Management_qui_quizId_id_e7fb481d_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztimer"
    ADD CONSTRAINT "Class_Management_qui_quizId_id_e7fb481d_fk_Class_Man" FOREIGN KEY ("quizId_id") REFERENCES public."Class_Management_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizscore Class_Management_qui_quizId_id_ed1c425f_fk_Class_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore"
    ADD CONSTRAINT "Class_Management_qui_quizId_id_ed1c425f_fk_Class_Man" FOREIGN KEY ("quizId_id") REFERENCES public."Class_Management_quiz"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizstatus Class_Management_qui_userId_id_00a1707d_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizstatus"
    ADD CONSTRAINT "Class_Management_qui_userId_id_00a1707d_fk_LogIn_Man" FOREIGN KEY ("userId_id") REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiztimer Class_Management_qui_userId_id_3089c57e_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztimer"
    ADD CONSTRAINT "Class_Management_qui_userId_id_3089c57e_fk_LogIn_Man" FOREIGN KEY ("userId_id") REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quiztracker Class_Management_qui_userId_id_95b7aa39_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quiztracker"
    ADD CONSTRAINT "Class_Management_qui_userId_id_95b7aa39_fk_LogIn_Man" FOREIGN KEY ("userId_id") REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Class_Management_quizscore Class_Management_qui_userId_id_9f1d0641_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Class_Management_quizscore"
    ADD CONSTRAINT "Class_Management_qui_userId_id_9f1d0641_fk_LogIn_Man" FOREIGN KEY ("userId_id") REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: LogIn_Management_profile LogIn_Management_pro_user_id_8450ccb2_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_profile"
    ADD CONSTRAINT "LogIn_Management_pro_user_id_8450ccb2_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: LogIn_Management_user_user_permissions LogIn_Management_use_permission_id_9b1826c8_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_user_permissions"
    ADD CONSTRAINT "LogIn_Management_use_permission_id_9b1826c8_fk_auth_perm" FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: LogIn_Management_user_user_permissions LogIn_Management_use_user_id_08db02bd_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_user_permissions"
    ADD CONSTRAINT "LogIn_Management_use_user_id_08db02bd_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: LogIn_Management_user_groups LogIn_Management_use_user_id_a7e13076_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_groups"
    ADD CONSTRAINT "LogIn_Management_use_user_id_a7e13076_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: LogIn_Management_user_groups LogIn_Management_user_groups_group_id_84db3e0e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LogIn_Management_user_groups"
    ADD CONSTRAINT "LogIn_Management_user_groups_group_id_84db3e0e_fk_auth_group_id" FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_LogIn_Man; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT "django_admin_log_user_id_c564eba6_fk_LogIn_Man" FOREIGN KEY (user_id) REFERENCES public."LogIn_Management_user"("userId") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

