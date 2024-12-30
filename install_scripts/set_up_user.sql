USE EXPENSE_TRACKER;

DELIMITER &&
CREATE PROCEDURE create_user(IN user_name VARCHAR(255), IN user_password VARCHAR(255))
BEGIN
    DECLARE user_count INT;

    SELECT COUNT(*) INTO user_count
    FROM mysql.user
    WHERE user=user_name AND host="localhost";

    IF user_count = 0 THEN
        SET @query = CONCAT('CREATE USER \'', user_name, '\'@\'localhost\' IDENTIFIED BY \'', user_password, '\';');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END&&

DELIMITER;

CALL create_user('mykola', 'linuxpassword');

GRANT ALL PRIVILEGES ON EXPENSE_TRACKER.* TO 'mykola'@'localhost';

FLUSH PRIVILEGES;
