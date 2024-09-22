import scrapy
import os

class SpanishWikipediaSpider(scrapy.Spider):
    name = 'spanish_wikipedia'
    allowed_domains = ['es.wikipedia.org']
    start_urls = ['https://es.wikipedia.org/wiki/Procesamiento_de_lenguajes_naturales']

    def __init__(self, *args, **kwargs):
        super(SpanishWikipediaSpider, self).__init__(*args, **kwargs)
        self.max_pages = 10000000000000000
        self.page_count = 0
        self.file_counter = 1

    def parse(self, response):
        if self.page_count >= self.max_pages:
            self.crawler.engine.close_spider(self, 'Page limit reached')
            return

        self.page_count += 1

        paragraphs = response.css('div.mw-parser-output > p::text').getall()
        article_text = ' '.join(paragraphs).strip()

        os.makedirs('articles', exist_ok=True)

        # Saving each article to individual text file
        file_name = f"articles/wiki_{self.file_counter}.txt"
        self.file_counter += 1
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(article_text)

        # Follow links to other pages and parse them
        for href in response.css('div.mw-parser-output a::attr(href)').getall():
            if href.startswith('/wiki/') and not ':' in href:
                yield response.follow(response.urljoin(href), self.parse)
