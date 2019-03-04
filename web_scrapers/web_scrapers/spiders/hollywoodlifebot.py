import scrapy
from web_scrapers.items import HollywoodlifeItem

class HollywoodlifeSpider(scrapy.Spider):
    name = "hollywoodlifeBot"
    allowed_domains = ["hollywoodlife.com"]

    start_urls = ["https://hollywoodlife.com/topics/news/"]

    def start_requests(self):
        for page_start in range(1, 700):
            yield scrapy.Request("https://hollywoodlife.com/topics/news/page/{}/".format(page_start))

    def parse(self, response):
        hxs = scrapy.Selector(response)

        article_urls = hxs.select('//*[@id="archive-river"]/article/div[2]/div/header/h3[@class="article-feed__article-title"]/a/@href').extract()

        for url in article_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_newsarticle)

    def parse_newsarticle(self, response):
        with open('../data/urls_hollywoodlife.txt', 'a') as f:
            f.write(response.url+'\n')

        item = HollywoodlifeItem()

        item['url'] = response.url
        item['timestamp'] = response.xpath('//time/span/text()').extract()[0]
        item['title'] = response.xpath('//h1/descendant::*/text()').extract()[0]
        content_top = ' '.join(response.xpath('//*[@id="site-content"]/main/article/div/div[3]/descendant::h3/text()').extract()).replace("\n", "").replace("\t", "")
        content_body = ' '.join(response.xpath('//*[@id="site-content"]/main/article/div/div[3]/descendant::p/text()').extract()).replace("\n", "").replace("\t", "")
        item['content'] = content_top + ' ' + content_body

        yield item

