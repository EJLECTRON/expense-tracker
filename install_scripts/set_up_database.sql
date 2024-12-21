CREATE DATABASE IF NOT EXISTS EXPENSE_TRACKER;
USE EXPENSE_TRACKER;

CREATE USER 'mykola'@'localhost' IDENTIFIED BY '#linux_password';

GRANT ALL PRIVILEGES ON EXPENSE_TRACKER.* TO 'mykola'@'localhost';

#create category table and populate it
CREATE TABLE IF NOT EXISTS CATEGORIES (
    ID INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL UNIQUE DEFAULT "MISCELLANEOUS"
);
INSERT IGNORE INTO CATEGORIES (NAME) VALUES 
('GROCERIES'), ('UTILITIES'), ('ENTERTAINMENT'), ('TAXES'), ('DEBT_PAYMENT'),
('INSURANCE'), ('TRANSPORATION'), ('RENT'), ('HOUSING'), ('SAVINGS'),
('INVESTMENTS'), ('SUBSCRIPTIONS'), ('GIFTS'), ('PERSONAL_CARE'),
('DINING_OUT'), ('HEALTH_CARE'), ('PERSONAL_EXPENSES'),
('EDUCATION'), ('PETS'), ('CHILD_CARE'), ('TRAVEL'), ('TECHNOLOGY'),
('LUXURY'), ('BUSINESS EXPENSES'), ('EVENTS'), ('FURNITURE'),
('REPAIRS');

#create expence table
CREATE TABLE IF NOT EXISTS EXPENSES (
    ID INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    AMOUNT INT(6) NOT NULL,
    TIME_OF_TRANSACTION DATETIME NOT NULL,
    CATEGORY_NAME VARCHAR(50) NOT NULL,
    DESCRIPTION VARCHAR(511),
    FOREIGN KEY (CATEGORY_NAME) REFERENCES CATEGORIES(NAME) ON UPDATE CASCADE
);

DELIMITER //

CREATE TRIGGER IF NOT EXISTS before_category_delete
BEFORE DELETE ON CATEGORIES
FOR EACH ROW
BEGIN
    UPDATE EXPENSES
    SET CATEGORY_NAME = 'MISCELLANEOUS'
    WHERE CATEGORY_NAME = OLD.NAME;
END //

DELIMITER ;

FLUSH PRIVILEGES;
