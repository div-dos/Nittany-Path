-- SQLite
CREATE TABLE Students(
    email   VARCHAR(100),
    password    VARCHAR(100),
    name    VARCHAR(30),
    age     INTEGER,
    gender  VARCHAR(1),
    major   VARCHAR(5),
    street  VARCHAR(100),
    zipcode INTEGER
);

CREATE TABLE Zipcodes(
  zipcode   INTEGER,
  city      VARCHAR(20),
  state     VARCHAR(20)
);

CREATE TABLE Professors(
    email   VARCHAR(100),
    password    VARCHAR(100),
    name    VARCHAR(30),
    age     INTEGER,
    gender  VARCHAR(6),
    office_address  VARCHAR(100),
    department  VARCHAR(20),
    title   VARCHAR(20)
);

CREATE TABLE Departments (
    dept_id     INTEGER,
    dept_name   VARCHAR(20),
    dept_head   VARCHAR(20)
);

CREATE TABLE Courses (
    course_id   INTEGER,
    course_name VARCHAR(30),
    course_description  VARCHAR(30),
    late_drop_deadline  DATE
);

CREATE TABLE Sections (
    course_id   INTEGER,
    sec_no      FLOAT,
    MAX_limit       INTEGER,
    teaching_team_id    INTEGER
);

CREATE TABLE Enrolls (
    student_email   VARCHAR(100),
    course_id       INTEGER,
    section_no      FLOAT
);

CREATE TABLE Prof_teaching_teams (
    prof_email      VARCHAR(100),
    teaching_team_id    INTEGER
);

CREATE TABLE TA_teaching_teams (
    student_email   VARCHAR(100),
    teaching_team_id    INTEGER
);

CREATE TABLE Homeworks (
    course_id       INTEGER,
    sec_no          FLOAT,
    hw_no           FLOAT,
    hw_detail       VARCHAR(100)
);

CREATE TABLE Homework_grades (
    student_email   VARCHAR(100),
    course_id       INTEGER,
    sec_no          FLOAT,
    hw_no           FLOAT,
    grade           FLOAT
);

CREATE TABLE Exams (
    course_id       INTEGER,
    sec_no          FLOAT,
    exam_no         FLOAT,
    exam_details    VARCHAR(100)
);

CREATE TABLE Exams_grades (
    student_email   VARCHAR(100),
    course_id       INTEGER,
    sec_no          FLOAT,
    exam_no         FLOAT,
    grades          FLOAT
);

CREATE TABLE Posts (
    course_id       INTEGER,
    post_no         INTEGER,
    student_email   VARCHAR(100),
    post_info       VARCHAR(100)
);

CREATE TABLE Comments (
    course_id       INTEGER,
    post_no         INTEGER,
    comment_no      INTEGER,
    student_email   VARCHAR(100),
    comment_info       VARCHAR(100)
);