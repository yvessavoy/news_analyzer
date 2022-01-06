import os
import ssl
from bs4 import BeautifulSoup
import requests
import feedparser

from news_analyzer.database import Database

"""
Parent Reader class for all site-specific readers.
This class is responsible for common setup like the
SSL context, logging and providing one implementation
for common problems applicable to all readers
"""


class Reader:
    def __init__(self):
        # To avoid problems with missing certificates, we setup the
        # SSL-Context in such a way that no certificate validation
        # happens. It is not necessary for this context, so there is
        # no harm in disabling it
        ssl._create_default_https_context = ssl._create_unverified_context

        self.soup = None
        self.db = self.init_db_connection()

    def process_rss_feed(self, link, handler_func, *args):
        """Process all item in a given RSS-feed
        """
        feed = feedparser.parse(link)
        for entry in feed.entries:
            self.soup = None
            handler_func(entry, args)

    def get_elements_from_html(self, url, html_info):
        if not self.soup:
            r = requests.get(url)
            self.soup = BeautifulSoup(r.text, 'html.parser')

        html_tag = html_info[0]
        html_class = html_info[1]

        items = self.soup.find_all(html_tag, {'class': html_class})

        return items if len(items) > 0 else None

    def init_db_connection(self):
        """Connect to the database

        Uses the environment variables DB_USER
        and DB_PASSWORD to get the credentials
        """
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')

        return Database('localhost', user, password)

    def get_html(self, url):
        """Return a string

        HTML-Content of the URL if the request was
        successful (HTTP 200), otherwhise an empty string
        """
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            return ""
