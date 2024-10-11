DROP DATABASE IF EXISTS bookstore;

CREATE DATABASE bookstore;

USE bookstore;

CREATE TABLE `bookstore`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(30) NOT NULL,
  `password` CHAR(72) NOT NULL,
  `address` TEXT NOT NULL,
  `role` ENUM('user', 'admin') NULL DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE);