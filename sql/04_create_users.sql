-- Note:
-- No user should have any privileges to Insert, Delete
-- or Update the Site- and User_Type-Table as it will be
-- loaded through a script and will not change after that.

-- Create a user for the data aggregation scripts
-- that has the right to SELECT and INSERT on all
-- tables
DROP USER IF EXISTS 'data_retrieval'@'localhost';
CREATE USER 'data_retrieval'@'localhost';
GRANT SELECT ON news_analyzer.ARTICLE TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.ARTICLE TO 'data_retrieval'@'localhost';

GRANT SELECT ON news_analyzer.USER TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.USER TO 'data_retrieval'@'localhost';

GRANT SELECT ON news_analyzer.CATEGORY TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.CATEGORY TO 'data_retrieval'@'localhost';

-- Create a user for the data analysis / report generation script
-- which only has the right to SELECT on all views
DROP USER IF EXISTS 'report'@'localhost';
CREATE USER 'report'@'localhost';
GRANT SELECT ON news_analyzer.WEEKDAY_STATISTIC TO 'report'@'localhost';
GRANT SELECT ON news_analyzer.PUB_STATISTIC TO 'report'@'localhost';
GRANT SELECT ON news_analyzer.CATEGORY_SUMMARY TO 'report'@'localhost';

-- Flush privileges to make them active immediately
FLUSH PRIVILEGES;