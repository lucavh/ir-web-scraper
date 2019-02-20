import scrapy
from web_scrapers.items import NewsItem

class TMZSpider(scrapy.Spider):
    name = "tmzbot"
    allowed_domains = ["tmz.com"]

    start_urls = ["https://www.tmz.com/?adid=TMZ_Web_Nav_News"]

    def start_requests(self):
        for page_start in range(800, 1500):
            yield scrapy.Request("https://www.tmz.com/page/{}/".format(page_start))


    def parse(self, response):
        hxs = scrapy.Selector(response)

        article_urls = hxs.select('//*[@id="main-content"]/descendant::article/a[@class="headline"]/@href').extract()

        for url in article_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_newsarticle)


    def parse_newsarticle(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['timestamp'] = response.xpath('//h5[@class="article-posted-date"]/text()').extract()[1].replace("\n","").strip()
        item['title'] = response.xpath('//h2/descendant::span/text()').extract()[0]
        content_body = ' '.join(response.xpath('//div[@class="all-post-body group article-content"]/descendant::p/text()').extract()).replace("\n", "").replace("\t", "")
        item['content'] = content_body
        yield item

