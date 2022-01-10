import pymysql


class Database:
    def __init__(self, host, user, password):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database='news_analyzer',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def begin_transaction(self):
        self.connection.begin()

    def commit_transaction(self):
        self.connection.commit()

    def save_article(self, article):
        with self.connection.cursor() as c:
            c.execute(
                "CALL sp_add_article(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    article.external_id,
                    article.site_name,
                    article.title,
                    article.author_last_name,
                    article.author_first_name,
                    article.length,
                    article.category,
                    article.published_at,
                    article.comment_count
                ))
            return c.lastrowid
