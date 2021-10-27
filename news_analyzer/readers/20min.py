import ssl
import os
import feedparser
import requests
from bs4 import BeautifulSoup
from news_analyzer.database import Database


def get_comment_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all("div", {"class": "CommentArea_commentCounter__2eY2Y"})

    # If no elements are found, comments are probably disabled
    if len(div) == 0:
        return None

    return int(div[0].span.text.split()[0])


def get_category(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all("a", {"class": "wfomuy-2 wfomuy-4 fTjhJh eOUWaL"})

    # If no elements are found, then there is probably no category
    if len(div) == 0:
        return None

    # As there could be subcategories with the same HTML-Class, we
    # will use the last one (deepest level)
    return div[len(div) - 1].text


def get_article_length(html):
    soup = BeautifulSoup(html, 'html.parser')
    wrapper = soup.find_all("section", {"class": "Article_body__19ylX"})

    # If there is no article section then there is also no content
    if len(wrapper) == 0:
        return 0

    return len(''.join(w.text for w in wrapper[0].find_all("p")))


def get_author(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all("dd", {"class": "e6kyyn-5 jqTZID"})

    # If there is no element, then there is probably no author
    if len(div) == 0:
        return None

    return div[0].text


def get_detail_html(url):
    return requests.get(url).text


def main():
    # Configure SSL to not validate certificates
    ssl._create_default_https_context = ssl._create_unverified_context

    # Parse the whole feed
    feed = feedparser.parse("https://partner-feeds.20min.ch/rss/20minuten")

    # Setup database
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db = Database('localhost', db_user, db_password)

    for entry in feed.entries:
        title = entry.title
        published_at = entry.published_parsed
        url_splits = entry.link.split("/")
        article_id = url_splits[len(url_splits) - 1]

        html = get_detail_html(entry.link)
        author = get_author(html)
        comments = get_comment_count(html)
        category = get_category(html)
        article_length = get_article_length(html)

        author_id = None
        if author:
            author_splits = author.split()
            if len(author_splits) > 1:
                author_id = db.save_author(author_splits[1], author_splits[0])
            else:
                author_id = db.save_author(author_splits[0], author_splits[0])

        category_id = None
        if category:
            category_id = db.save_category(category)

        db.save_article(article_id, author_id, 1, title,
                        article_length, comments, published_at, category_id)


if __name__ == '__main__':
    main()
