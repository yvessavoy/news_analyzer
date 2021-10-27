import ssl
import os
import re
from bs4 import BeautifulSoup
import feedparser
import requests

from news_analyzer.database import Database

feeds = [
    ('https://www.blick.ch/rss.xml', 'News'),
    ('https://www.blick.ch/news/rss.xml', 'News'),
    ('https://www.blick.ch/schweiz/rss.xml', 'Schweiz'),
    ('https://www.blick.ch/ausland/rss.xml', 'Ausland'),
    ('https://www.blick.ch/wirtschaft/rss.xml', 'Wirtschaft'),
    ('https://www.blick.ch/sport/rss.xml', 'Sport'),
    ('https://www.blick.ch/sport/fussball/rss.xml', 'Fussball'),
    ('https://www.blick.ch/sport/eishockey/rss.xml', 'Eishockey'),
    ('https://www.blick.ch/sport/ski/rss.xml', 'Ski'),
    ('https://www.blick.ch/sport/tennis/rss.xml', 'Tennis'),
    ('https://www.blick.ch/sport/formel1/rss.xml', 'Formel 1'),
    ('https://www.blick.ch/sport/rad/rss.xml', 'Rad'),
    ('https://www.blick.ch/people-tv/rss.xml', 'Menschen'),
    ('https://www.blick.ch/life/rss.xml', 'Leben'),
    ('https://www.blick.ch/digital/rss.xml', 'Digital'),
]


def get_detail_html(url):
    return requests.get(url).text


def get_comment_count(article_id):
    r = requests.get(
        f'https://community.ws.blick.ch/community/comment?page=1&discussion_type_id={article_id}')
    return r.json()['number_of_comments']


def get_article_length(html):
    matches = re.findall('"articleLength":([0-9]+),', html)
    if len(matches) > 0:
        return int(matches[0])
    else:
        return 0


def main():
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db = Database('localhost', db_user, db_password)

    for (url, category) in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            published_at = entry.published_parsed
            article_id_splits = entry.id.split("-")
            article_id = article_id_splits[-1].split(".")[0][2:]

            html = get_detail_html(entry.link)
            comment_count = get_comment_count(article_id)
            article_length = get_article_length(html)

            author_id = None
            if 'author' in entry:
                author_splits = entry.author.split()
                if len(author_splits) > 1:
                    author_id = db.save_author(
                        author_splits[0], author_splits[1])
                if len(author_splits) == 1:
                    author_id = db.save_author(
                        author_splits[0], author_splits[0])

            category_id = db.save_category(category)

            db.save_article(article_id, author_id, 2, title,
                            article_length, comment_count, published_at, category_id)


if __name__ == '__main__':
    # Configure SSL to not validate certificates
    ssl._create_default_https_context = ssl._create_unverified_context
    main()
