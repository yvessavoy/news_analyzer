import pymysql


class Database:
    def __init__(self, host, user, password):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database='news_analyzer',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def save_author(self, lastname, firstname):
        with self.connection.cursor() as c:
            c.execute(
                'SELECT ID FROM AUTHOR WHERE LAST_NAME = %s AND FIRST_NAME = %s', (lastname, firstname))
            result = c.fetchone()
            if result:
                return result['ID']

            c.execute(
                'INSERT INTO AUTHOR(LAST_NAME, FIRST_NAME) VALUES(%s, %s)', (lastname, firstname))
            self.connection.commit()
            return c.lastrowid

    def save_article(self, article_id, author_id, site_id, title, article_length, comment_count, published_at, category_id):
        with self.connection.cursor() as c:
            c.execute(
                'SELECT ID FROM article WHERE ARTICLE_ID = %s', (article_id,))
            result = c.fetchone()
            if result:
                return result['ID']

            c.execute(
                """
                INSERT INTO article(
                    ARTICLE_ID
                    , AUTHOR_ID
                    , SITE_ID
                    , TITLE
                    , ARTICLE_LENGTH
                    , COMMENT_COUNT
                    , PUBLISHED_AT
                    , CATEGORY_ID
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (article_id, author_id, site_id, title, article_length, comment_count, published_at, category_id))
            self.connection.commit()
            return c.lastrowid

    def save_category(self, name):
        with self.connection.cursor() as c:
            c.execute(
                'SELECT ID FROM CATEGORY WHERE NAME = %s', (name,))
            result = c.fetchone()
            if result:
                return result['ID']

            c.execute(
                'INSERT INTO CATEGORY(NAME) VALUES(%s)', (name,))
            self.connection.commit()
            return c.lastrowid
