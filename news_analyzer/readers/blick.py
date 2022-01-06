import ssl
import os
import re
from bs4 import BeautifulSoup
import feedparser
import requests

from news_analyzer.database import Database
from news_analyzer.database.models import Article, User
from news_analyzer.readers import Reader

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


class Blick(Reader):
    def get_comment_count(self, article_id):
        r = requests.get(
            f'https://community.ws.blick.ch/community/comment?page=1&discussion_type_id={article_id}')
        return r.json()['number_of_comments']

    def get_article_length(self, html):
        matches = re.findall('"articleLength":([0-9]+),', html)
        if len(matches) > 0:
            return int(matches[0])
        else:
            return 0

    def process_entry(self, entry, *args):
        category = args[0]
        article = Article(site_id=2)
        article.category_id = self.db.save_category(category)
        article.title = entry.title
        article.published_at = entry.published_parsed
        article.external_id = entry.link.split('-id')[1].split('.')[0]
        article.comment_count = self.get_comment_count(article.external_id)
        article.length = self.get_article_length(requests.get(entry.link).text)
        if article.length == 0:
            article.length = len(article.title)

        if 'author' in entry:
            author = User(type=1)
            author_splits = entry.author.split()
            if len(author_splits) > 1:
                author.first_name = author_splits[1]
                author.last_name = author_splits[0]
            if len(author_splits) == 1:
                author.first_name = author_splits[0]
                author.last_name = author_splits[0]

            article.author_id = self.db.save_user(author)

        self.db.save_article(article)

    def process_feed(self):
        for (url, category) in feeds:
            self.process_rss_feed(url, self.process_entry, category)


if __name__ == '__main__':
    Blick().process_feed()
