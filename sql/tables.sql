-- file: tables.sql
-- date: 22 SEP 2011
-- author: John P Clements
-- 
-- table creation script for mebook database. used for PostreSQL 8.4

CREATE TABLE books (
   book_id int,
   title varchar(256),
   pub_year int,
   PRIMARY KEY (book_id)
);

CREATE TABLE authors (
   author_id int,
   name varchar(256),
   PRIMARY KEY (author_id)
);

CREATE TABLE series (
   series_id int,
   name varchar(256),
   PRIMARY KEY (series_id)
);

CREATE TABLE book_series (
   book_id int REFERENCES books(book_id),
   series_id int REFERENCES series(series_id),
   book_in_series int,
   PRIMARY KEY (book_id, series_id)
);

CREATE TABLE books_authors (
   book_id int REFERENCES books(book_id),
   author_id int REFERENCES authors(author_id),
   PRIMARY KEY(book_id, author_id)
);

CREATE TABLE isbns (
   book_id int references books(book_id),
   isbn varchar(20),
   is_main boolean
);

CREATE TABLE books_read (
   book_id int references books(book_id),
   was_read boolean,
   date_read date
);
