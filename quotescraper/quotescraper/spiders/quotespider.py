import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css('div.quote')
        
        for quote in quotes:
            yield {
                'quote': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
                'about': quote.css('div.quote span a::attr(href)').get()
            }
            
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = 'https://quotes.toscrape.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_about(self, response, author):
        yield {
            'author': author,
            'about': response.css('.author-description::text').get()
        }