-- Note:
-- No user should have any privileges to Insert, Delete
-- or Update the Site-Table as it will be loaded through
-- a script and will not change after that.

-- Create a user for the data aggregation scripts
-- that has the right to SELECT and INSERT on all
-- tables
DROP USER 'data_retrieval'@'localhost';
CREATE USER 'data_retrieval'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.ARTICLE TO 'data_retrieval'@'localhost';
GRANT INSERT ON NEWS_ANALYZER.ARTICLE TO 'data_retrieval'@'localhost';

GRANT SELECT ON NEWS_ANALYZER.USER TO 'data_retrieval'@'localhost';
GRANT INSERT ON NEWS_ANALYZER.USER TO 'data_retrieval'@'localhost';

GRANT SELECT ON NEWS_ANALYZER.CATEGORY TO 'data_retrieval'@'localhost';
GRANT INSERT ON NEWS_ANALYZER.CATEGORY TO 'data_retrieval'@'localhost';

-- Create a user for the data analysis / report generation script
-- which only has the right to SELECT on all views and tables
DROP USER 'report'@'localhost';
CREATE USER 'report'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.ARTICLE TO 'report'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.USER TO 'report'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.CATEGORY TO 'report'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.SITE TO 'report'@'localhost';
GRANT SELECT ON NEWS_ANALYZER.COMMENT TO 'report'@'localhost';

-- Flush privileges to make them active immediately
FLUSH PRIVILEGES;