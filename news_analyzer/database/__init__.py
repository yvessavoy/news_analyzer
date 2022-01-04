import pymysql


class Database:
    def __init__(self, host, user, password):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database='news_analyzer',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def save_user(self, author):
        with self.connection.cursor() as c:
            c.execute(
                'SELECT ID FROM USER WHERE LAST_NAME = %s AND FIRST_NAME = %s', (author.last_name, author.first_name))
            result = c.fetchone()
            if result:
                return result['ID']

            c.execute(
                'INSERT INTO USER(LAST_NAME, FIRST_NAME, TYPE) VALUES(%s, %s, %s)', (author.last_name, author.first_name, author.type))
            self.connection.commit()

            return c.lastrowid

    def save_article(self, article):
        with self.connection.cursor() as c:
            c.execute(
                'SELECT ID FROM ARTICLE WHERE EXTERNAL_ID = %s', (article.external_id,))
            result = c.fetchone()
            if result:
                return result['ID']

            c.execute(
                """
                INSERT INTO ARTICLE(
                      EXTERNAL_ID
                    , AUTHOR_ID
                    , SITE_ID
                    , TITLE
                    , ARTICLE_LENGTH
                    , PUBLISHED_AT
                    , CATEGORY_ID
                ) VALUES(%s, %s, %s, %s, %s, %s, %s)""", (
                    article.external_id, article.author_id,
                    article.site_id,
                    article.title,
                    article.length,
                    article.published_at,
                    article.category_id
                ))
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
