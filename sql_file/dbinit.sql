-- source E:/git-demo/bookmanage/dbinit.sql
DROP DATABASE IF EXISTS bookmanage;
CREATE DATABASE IF NOT exists bookmanage;
default character set utf8;
default collate utf8_general_ci;

use bookmanage;

-- 创建 book_list 总表
create table if not exists book_list(
    book_id int auto_increment,
    name varchar(80) not null,
    auther varchar(80) not null,
    price int not null,
    date varchar(80) not null,
    number int not null,
    primary key (book_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建用户表
create table if not exists user(
    id int auto_increment,
    name varchar(80),
    password varchar(128) not null,
    if_manager enum('Y','N') not null default 'N',
    primary key(id),
    unique key(name)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建出借记录表
create table if not exists record(
    id int auto_increment,
    username varchar(80),
    book_id int,
    primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
