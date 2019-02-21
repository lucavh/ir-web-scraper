import scrapy
import json
from web_scrapers.items import RottenItem

class RottenTomatoesSpider(scrapy.Spider):
    name = "rtbot"
    allowed_domains = ["rottentomatoes.com"]

    start_urls = ["https://rottentomatoes.com"]

    def start_requests(self):
        for page_start in range(0,15000,30):
            yield scrapy.Request(
                "https://www.rottentomatoes.com/api/private/v2.0/search?q=\%3F&t=celeb&offset={0}&limit={1}".format(page_start, 30))

    def parse(self, response):
        data = json.loads(response.text)
        article_urls = [actor['url'] for actor in data['actors']]

        for url in article_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_review)


    def parse_review(self, response):
        item = RottenItem()
        item['url'] = response.url
        item['name'] = response.xpath('//html/head/meta[7]/@content').extract()[0]
        item['birthplace'] = response.xpath('//*[@id="main_container"]/section/div[1]/div[1]/section/div/div[3]/div[4]/text()').extract()[1].replace("\n", "").strip()
        item['birthday'] = response.xpath('//*[@id="main_container"]/section/div[1]/div[1]/section/div/div[3]/div[3]/text()').extract()[1].replace("\n", "").strip()
        try:
            item['bio'] = response.xpath('//*[@id="main_container"]/section/div[1]/div[1]/section/div/div[3]/div[5]/text()').extract()[0].replace("\n", "").strip()
        except:
            item['bio'] = ''
        item['filmography'] = response.xpath('//*[@id="filmography"]//tbody//tr//@data-title').extract()
        item['roles'] = list(filter(None, [role.strip() for role in response.xpath('//*[@id="filmography"]/section/div/div/table/tbody//tr/td[3]/text()').extract()]))
        item['offscreen_role'] = set(response.xpath('//*[@id="filmography"]/section/div/div/table/tbody//tr/td[3]//em/text()').extract())

        yield item

#