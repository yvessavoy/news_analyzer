from news_analyzer.readers import Reader
from news_analyzer.database.models import Article, User, Category


# The following dict defines the tags and classes which represent
# the needed data in the HTML source of 20min.ch, for example in which
# tag and with what class we can get the author The data is stored as:
# key: (tag, class)
# This information is taken from the HTML-source of 20min.ch
HTML_INFO = {
    'author': ('dd', 'e6kyyn-5 jqTZID'),
    'category': ('a', 'wfomuy-2 wfomuy-4 fTjhJh eOUWaL'),
    'article_text': ('section', 'Article_body__19ylX')
}


class TwentyMinutes(Reader):
    def get_comment_count(self, url):
        div = self.get_elements_from_html(
            url, ('div', 'CommentArea_commentCounter__2eY2Y'))

        # If no elements are found, comments are probably disabled
        if div:
            if len(div) == 0:
                return None
        else:
            return None

        return int(div[0].span.text.split()[0])

    def process_entry(self, entry, *args):
        article = Article(site_id=1)
        article.title = entry.title
        article.published_at = entry.published_parsed
        article.external_id = entry.link.split("/")[-1]
        article.comment_count = self.get_comment_count(entry.link)

        parts = self.get_elements_from_html(
            entry.link, HTML_INFO['article_text'])
        if parts:
            article.length = len(
                ''.join(w.text for w in parts[0].find_all("p")))
        else:
            article.length = len(article.title)

        # Start transaction
        # We only want to persist the new data if all inserts (author, article, etc.)
        # are successful
        self.db.begin_transaction()

        parts = self.get_elements_from_html(entry.link, HTML_INFO['author'])
        if parts:
            author = User(type=1)
            s = str(parts[0]).split()
            if len(s) > 1:
                author.last_name = s[0]
                author.first_name = s[1]
            else:
                author.last_name = author.first_name = s[0]

            article.author_id = self.db.save_user(author)

        parts = self.get_elements_from_html(entry.link, HTML_INFO['category'])
        if parts:
            article.category_id = self.db.save_category(
                Category(name=parts[-1].text))

        self.db.save_article(article)

        # Commit transaction as all database operations were OK
        self.db.commit_transaction()

    def process_feed(self):
        self.process_rss_feed(
            "https://partner-feeds.20min.ch/rss/20minuten", self.process_entry)


if __name__ == '__main__':
    TwentyMinutes().process_feed()
