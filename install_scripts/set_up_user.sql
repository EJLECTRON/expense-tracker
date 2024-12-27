DELIMITER $$
CREATE PROCEDURE CreateUserIfNotExists(IN username VARCHAR(255))
BEGIN
    DECLARE user_count INT;

    SELECT COUNT(*) INTO user_count
    FROM mysql.user
    WHERE user = username AND host = 'localhost';

    IF user_count = 0 THEN CREATE USER username@'localhost' IDENTIFIED BY password;
END$$
DELIMITER;

CALL CreateUserIfNotExists('mykola', '#linux_password')

GRANT ALL PRIVILEGES ON EXPENSE_TRACKER.* TO 'mykola'@'localhost';

FLUSH PRIVILEGES;
