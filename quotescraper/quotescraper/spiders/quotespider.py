import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    start_urls = ["https://quotes.toscrape.com/", ]

    def parse(self, response):
        
        for quote in response.css('div.quote'):
            # Extraer la info de cada cita
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            about_url = response.urljoin(quote.css('span > a::attr(href)').get())
            tags = quote.css('div.tags a.tag::text').getall()
            
            # Extraer info de la cita y seguir el enlace del autor
            yield response.follow(about_url, self.parse_author, meta={
                'text': text, 
                'author': author, 
                'about': about_url,
                'tags' : tags
                })
            
        # Seguir a la siguiente página
        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, self.parse)
        
    def parse_author(self, response):
        text = response.meta['text']
        author = response.meta['author']
        about_url = response.meta['about']
        tags = response.meta['tags']
        
        bio = response.css('div.author-description::text').get()
        
        yield {
            'text': text,
            'author': author,
            'about': about_url,
            'tags': tags,
            'bio': bio,
        }