create database if not exists ece140;

use ece140;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
-- drop table if exists users;

create table if not exists users (
  id         integer auto_increment primary key,
  first_name varchar(30) not null,
  last_name  varchar(30) not null,
  created_at timestamp
);

insert into users (first_name, last_name, created_at) values
  ("Zendaya", "", current_timestamp),
  ("Tom", "Holland", current_timestamp),
  ("Tobey", "Maguire", current_timestamp),
  ("Andrew", "Garfield", current_timestamp)
;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
drop table if exists members;

create table if not exists members (
  id          integer auto_increment primary key,
  first_name  varchar(30) not null,
  last_name   varchar(30) not null,
  username    varchar(254) not null,
  pass        varchar(128) not null,
  db_role     varchar(20) not null,
  created_at  timestamp
);

-- 2. Insert initial seed records into the table
-- [INSERT CODE HERE]
insert into members (first_name, last_name, username, pass, db_role, created_at) values
  ("Sialoi", "Taa", "SialoiTaa", "12345", "ADMIN", current_timestamp),
  ("Yuyang", "Wu", "YuyangWu", "12345", "USER", current_timestamp)
;