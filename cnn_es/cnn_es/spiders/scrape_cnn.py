import scrapy
import os

class CnnSpider(scrapy.Spider):
    name = 'cnn_spider'
    allowed_domains = ['cnnespanol.cnn.com']
    start_urls = ['https://cnnespanol.cnn.com/']

    file_counter = 1

    def parse(self, response):
        for article in response.css('article'):
            link = article.css('a::attr(href)').get()
            if link:
                full_link = response.urljoin(link)
                yield scrapy.Request(full_link, callback=self.parse_article)

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        
        # Extract article content
        content_blocks = response.css('p.paragraph.inline-placeholder.vossi-paragraph-primary-core-light::text').getall()
        content = ' '.join(content_blocks).strip()

        if not title:
            title = response.css('h1 span::text').get()

        os.makedirs('articles', exist_ok=True)

        file_name = f"articles/article_{self.file_counter}.txt"
        self.file_counter += 1

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            # f.write(f"URL: {response.url}\n\n")
            f.write(content)

        self.log(f'Saved file {file_name}')
