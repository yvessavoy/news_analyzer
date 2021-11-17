-- Note:
-- No user should have any privileges to Insert, Delete
-- or Update the Site-Table as it will be loaded through
-- a script and will not change after that.

-- Create a user for the data aggregation scripts
-- that has the right to SELECT and INSERT on all
-- tables
CREATE USER 'data_retrieval'@'localhost';
GRANT SELECT ON news_analyzer.article TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.article TO 'data_retrieval'@'localhost';

GRANT SELECT ON news_analyzer.author TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.author TO 'data_retrieval'@'localhost';

GRANT SELECT ON news_analyzer.category TO 'data_retrieval'@'localhost';
GRANT INSERT ON news_analyzer.category TO 'data_retrieval'@'localhost';

-- Create a user for the data analysis / report generation script
-- which only has the right to SELECT on all views and tables
CREATE USER 'report'@'localhost';
GRANT SELECT ON news_analyzer.article TO 'report'@'localhost';
GRANT SELECT ON news_analyzer.author TO 'report'@'localhost';
GRANT SELECT ON news_analyzer.category TO 'report'@'localhost';

-- Flush privileges to make them active immediately
FLUSH PRIVILEGES;