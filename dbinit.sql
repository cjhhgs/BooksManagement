-- source E:/git-demo/bookmanage/dbinit.sql
DROP DATABASE IF EXISTS bookmanage;
CREATE DATABASE IF NOT exists bookmanage
default character set utf8
default collate utf8_general_ci;

use bookmanage

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
    if_manager enum('Y','N') not null default 'N',
    user_id int auto_increment,
    name varchar(80),
    password varchar(128) not null,
    primary key(user_id),
    unique key(name)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建函数，判断book_id是否存在于某分表中，若不存在则返回-1
delimiter $$
drop function if exists ifexist$$
create function ifexist (id int) 
returns int
begin
    if (id in (select book_id from book_list)) then
        return(id);
    end if;
    return(-1);
end$$
delimiter ;