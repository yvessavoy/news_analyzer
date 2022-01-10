-- Check if that author already exists and if not, add it with USERTYPE = 1
DROP PROCEDURE IF EXISTS sp_add_author;
DELIMITER $$
CREATE PROCEDURE sp_add_author(IN last_name VARCHAR(255), IN first_name VARCHAR(255), OUT A_ID INT)
BEGIN
    SELECT ID INTO A_ID FROM USER A WHERE A.LAST_NAME = last_name AND A.FIRST_NAME = first_name;
    IF A_ID IS NULL THEN
        INSERT INTO USER (LAST_NAME, FIRST_NAME, TYPE) VALUES (last_name, first_name, 1);
		SELECT ID INTO A_ID FROM USER A WHERE A.LAST_NAME = last_name AND A.FIRST_NAME = first_name;
    END IF;
END$$
DELIMITER ;

-- Check if that category already exists and if not, create it
DROP PROCEDURE IF EXISTS sp_add_category;
DELIMITER $$
CREATE PROCEDURE sp_add_category(IN c_name VARCHAR(255), OUT C_ID INT)
BEGIN
    SELECT ID INTO C_ID FROM CATEGORY WHERE NAME = c_name;
    IF C_ID IS NULL THEN
        INSERT INTO CATEGORY (NAME) VALUES (c_name);
        SELECT ID INTO C_ID FROM CATEGORY WHERE NAME = c_name;
    END IF;
END$$
DELIMITER ;

-- Insert a new article with adding a category and author if they don't exist yet. Also checks whether the external id already exists
-- to avoid double storing of the same article
DROP PROCEDURE IF EXISTS sp_add_article;
DELIMITER $$
CREATE PROCEDURE sp_add_article(IN ext_id VARCHAR(255), IN site_name VARCHAR(255), IN title VARCHAR(255), IN a_last_name VARCHAR(255), IN a_first_name VARCHAR(255), IN article_length INT, IN category VARCHAR(255), IN pub_at DATETIME, IN comment_count INT)
BEGIN
    DECLARE S_ID INT;
    DECLARE A_ID INT;
    DECLARE C_ID INT;
    DECLARE ARTICLE_ID INT;
    
    CALL sp_add_author(a_last_name, a_first_name, A_ID);
    CALL sp_add_category(category, C_ID);
    SELECT ID INTO S_ID FROM SITE WHERE NAME = site_name;

    IF S_ID IS NOT NULL AND A_ID IS NOT NULL AND C_ID IS NOT NULL THEN
        SELECT ID INTO ARTICLE_ID FROM ARTICLE WHERE EXTERNAL_ID = ext_id;
        IF ARTICLE_ID IS NULL THEN
            INSERT INTO ARTICLE (EXTERNAL_ID, AUTHOR_ID, SITE_ID, TITLE, LENGTH, PUBLISHED_AT, CATEGORY_ID, COMMENT_COUNT)
            VALUES (ext_id, A_ID, S_ID, title, article_length, pub_at, C_ID, comment_count);
        END IF;
    END IF;
END$$
DELIMITER ;