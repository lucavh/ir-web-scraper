import scrapy
from web_scrapers.items import MoviewebItem

class MoviewebSpider(scrapy.Spider):
    name = "moviewebBot"
    allowed_domains = ["movieweb.com"]

    start_urls = ["https://movieweb.com/movie-news/"]

    def start_requests(self):
        for page_start in range(1, 600):
            yield scrapy.Request("https://movieweb.com/movie-news/?page={}".format(page_start))

    def parse(self, response):
        hxs = scrapy.Selector(response)

        article_urls = hxs.select('//article/a/@href').extract()

        for url in article_urls:
            yield scrapy.Request(response.urljoin('https://movieweb.com'+url), callback=self.parse_newsarticle)

    def parse_newsarticle(self, response):
        with open('../data/urls_movieweb.txt', 'a') as f:
            f.write(response.url+'\n')

        item = MoviewebItem()

        item['url'] = response.url
        item['timestamp'] = response.xpath('//time/text()').extract()[0]
        item['title'] = response.xpath('//h1/text()').extract()[0]
        content_body = ' '.join(response.xpath('//html/body/main/div/div/article/section/div/descendant::p/text()').extract()).replace("\n", "").replace("\t", "")
        item['content'] = content_body

        yield item


