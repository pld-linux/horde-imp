// IMP database creation script for postgreSQL
// Author: barce@lines.edu
// Date:   Aug-29-1998
// Notes: replace "nobody" with yours httpd username
// Run using:  psql template1 < pgsql_create.sql

CREATE DATABASE imp;

\connect imp

CREATE TABLE imp_pref (
username	text,
sig		text,
fullname	text,
replyto		text,
lang            varchar(30)
);

CREATE TABLE imp_addr (
username	text,
address		text,
nickname	text,
fullname	text
);

GRANT SELECT, INSERT, UPDATE ON imp_pref, imp_addr TO www-data
