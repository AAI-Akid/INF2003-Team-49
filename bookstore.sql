DROP DATABASE IF EXISTS bookstore;
CREATE DATABASE bookstore;
USE bookstore;
  
  -- Create Books Table
  CREATE TABLE bookstore.books (
  `book_id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `author` VARCHAR(50) NOT NULL,
  `rating` DECIMAL(2,1) NULL DEFAULT 0,
  `price` DECIMAL(5,2) NOT NULL DEFAULT 0,
  `currency` CHAR(3) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `page_count` INT NULL,
  `genres` VARCHAR(100) NULL,
  `ISBN` VARCHAR(17) NULL,
  `language` VARCHAR(50) NULL,
  `published_date` VARCHAR(45) NULL,
  `cover_image` VARCHAR(45) NULL,
  PRIMARY KEY (`book_id`));
  
-- Create Users Table
CREATE TABLE `bookstore`.`users` (
    user_id TINYINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password CHAR(72) NOT NULL,
    address TEXT NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user'
);
  
-- Create Orders Table
CREATE TABLE `bookstore`.`orders` (
    order_id TINYINT AUTO_INCREMENT PRIMARY KEY,
    user_id TINYINT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,	
    status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') NOT NULL DEFAULT 'Pending',
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES `bookstore`.`users`(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Create Order_Items Table
CREATE TABLE `bookstore`.`order_Items` (
    order_item_id TINYINT AUTO_INCREMENT PRIMARY KEY,
    order_id TINYINT,
    book_id TINYINT UNSIGNED,
    quantity INT UNSIGNED NOT NULL,
    price_per_unit DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `bookstore`.`orders`(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES `bookstore`.`books`(book_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create Inventory Table with book_id as Primary Key
CREATE TABLE `bookstore`.`inventory` (
    book_id TINYINT UNSIGNED NOT NULL,
    quantity_in_stock INT UNSIGNED NOT NULL DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id),
    FOREIGN KEY (book_id) REFERENCES `bookstore`.`books`(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Run the following after importing dataset (don't import with book_id)
UPDATE bookstore.books
SET published_date = STR_TO_DATE(published_date, '%b %d, %Y');
ALTER TABLE bookstore.books
MODIFY published_date DATE;

update books set cover_image = "attack_on_titan_volume_13.jpg" where book_id = 1;
update books set cover_image = "mario.jpg" where book_id = 2;
update books set cover_image = "The_Painted_Man_The_Demon_Cycle_Book_1.jpg" where book_id = 3;
update books set cover_image = "A_Feast_for_Crows.jpg" where book_id = 4;
update books set cover_image = "God_Of_War.jpg" where book_id = 5;
update books set cover_image = "Edgedancer.jpg" where book_id = 6;
update books set cover_image = "BSAP.jpg" where book_id = 7;
update books set cover_image = "TWAS.jpg" where book_id = 8;
update books set cover_image = "witcher.jpg" where book_id = 9;
update books set cover_image = "affair.jpg" where book_id = 10;
update books set cover_image = "OGOT.jpg" where book_id = 11;
update books set cover_image = "deadpool.jpg" where book_id = 12;

-- Generate data for inventory table
INSERT INTO `bookstore`.`inventory` (book_id, quantity_in_stock)
SELECT book_id, 5
FROM `bookstore`.`books`;