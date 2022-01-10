import requests
from bs4 import BeautifulSoup
from news_analyzer.database.models import Article
from news_analyzer.readers import Reader

feeds = [
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/startseite', 'Startseite'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/sport', 'Sport'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/tennis', 'Tennis'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/eishockey', 'Eishockey'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/fussball', 'Fussball'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/schweiz', 'Schweiz'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/wirtschaft', 'Wirtschaft'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kultur', 'Kultur'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/digital', 'Digital'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/natur', 'Natur'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/gesellschaft', 'Gesellschaft'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/geld-recht', 'Geld & Recht'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/wissen', 'Wissen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/panorama', 'Panorama'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/leben', 'Leben'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/motorsport', 'Motorsport'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/ski-alpin', 'Ski alpin'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/rad', 'Rad'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/weitere-sportarten',
        'Weitere Sportarten'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/vermischtes', 'Vermischtes'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/international', 'International'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/europa', 'Europa'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/amerika', 'Amerika'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/naher-osten-afrika',
        'Naher Osten & Afrika'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/asien-ozeanien',
        'Asien & Ozeanien'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/stadt', 'Stadt'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/reisen', 'Reisen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/mobilitat', 'Mobilität'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/leichtathletik', 'Leichtathletik'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/wahlen', 'Wahlen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/technik', 'Technik'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/medizin-psychologie',
        'Medizin & Psychologie'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/musik', 'Musik'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/fernsehen', 'Fernsehen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kino', 'Kino'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/region', 'Region'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/unternehmen-konjunktur',
        'Unternehmen & Konjunktur'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/bucher', 'Bücher'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/theater', 'Theater'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kunst', 'Kunst'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/klassik', 'Klassik'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/geschichte', 'Geschichte'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/essen-und-trinken',
        'Essen und Trinken'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/leute', 'Leute'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/zurich', 'Zürich'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/zuritipp', 'Züritipp'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/meinungen', 'Meinungen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kolumnen', 'Kolumnen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/us-wahlen', 'US-Wahlen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/wef-2020', 'WEF 2020'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/karriere', 'Karriere'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/cryptoleaks', 'Cryptoleaks'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/coronavirus', 'Coronavirus'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/essen-trinken-in-zurich',
        'Essen & Trinken in Zürich'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/neu-im-kino', 'Neu im Kino'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/coronavirus-service',
        'Coronavirus Service'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kulturstream', 'Kulturstream'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/bundeshaus', 'Bundeshaus'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/abstimmungen', 'Abstimmungen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/gastkommentare', 'Gastkommentare'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/formel-1', 'Formel 1'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/klimawandel', 'Klimawandel'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/fc-zurich', 'FC Zürich'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/gc', 'GC'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/ehc-kloten', 'EHC Kloten'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/zsc', 'ZSC'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/freizeitsport', 'Freizeitsport'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/das-magazin', 'Das Magazin'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/blogs', 'Blogs'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/fokusthema', 'Fokusthema'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/kolumnen', 'Kolumnen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/reportagen', 'Reportagen'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/rezepte', 'Rezepte'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/lockdown', 'Lockdown'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/schach', 'Schach'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/fussball-em', 'Fussball-EM'),
    ('https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/olympia-2021', 'Olympia 2021'),
]

# The following dict defines the tags and classes which represent
# the needed data in the HTML source of tagesanzeiger.ch, for example in which
# tag and with what class we can get the author The data is stored as:
# key: (tag, class)
# This information is taken from the HTML-source of tagesanzeiger.ch
HTML_INFO = {
    'author': ('span', 'ContentMetaInfo_author__HbYvO'),
    'article_text': ('p', 'ArticleParagraph_root__3J10I'),
    'comments': ('span', 'commentcount'),
}


class Tagesanzeiger(Reader):
    def process_entry(self, entry, args):
        category = args[0]
        article = Article(site_name='Tagesanzeiger')

        article.title = entry.title
        article.published_at = entry.published_parsed
        article.external_id = entry.link.split("-")[-1]

        article.category = category

        author_items = self.get_elements_from_html(
            entry.link, HTML_INFO['author'])

        r = requests.get(entry.link)
        soup = BeautifulSoup(r.text, 'html.parser')
        spans = soup.find_all(
            HTML_INFO['author'][0], {"class": HTML_INFO['author'][1]})

        if len(spans) > 0:
            author_splits = spans[0].text.split()
            if len(author_splits) > 1:
                article.author_first_name = author_splits[0]
                article.author_last_name = author_splits[1]
            else:
                article.author_first_name = author_splits[0]
                article.author_last_name = author_splits[0]

        if not article.author_first_name:
            article.author_first_name = "N/A"

        if not article.author_last_name:
            article.author_last_name = "N/A"

        comments = self.get_elements_from_html(
            entry.link, HTML_INFO['comments'])
        if comments and len(comments) > 0:
            article.comment_count = str(comments[0]).split('>')[1].split()[0]

        paragraphs = soup.find_all(
            HTML_INFO['article_text'][0], {"class": HTML_INFO['article_text'][1]})
        for paragraph in paragraphs:
            for s in paragraph.find_all('span'):
                article.length += len(s.text)

        if article.length == 0:
            article.length = len(article.title)

        # Start transaction
        # We only want to persist the new data if all inserts (author, article, etc.)
        # are successful
        self.db.begin_transaction()

        self.db.save_article(article)

        # Commit transaction as all database operations were OK
        self.db.commit_transaction()

    def process_feed(self):
        for (url, category) in feeds:
            self.process_rss_feed(url, self.process_entry, category)


if __name__ == '__main__':
    Tagesanzeiger().process_feed()
