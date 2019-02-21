# -*- coding: utf-8 -*-
import scrapy
from imdb.items import ImdbItem

class ImdbbotSpider(scrapy.Spider):
    name = 'imdbbot1'
    allowed_domains = ['www.imdb.com']

    #start_urls = ['https://www.imdb.com/search/name?gender=male,female&ref_=rlm']

    def start_requests(self):
        for rank_start in range(1, 10001, 50):
            yield scrapy.Request("https://www.imdb.com/search/name?gender=male,female&start={}&ref_=rlm".format(rank_start))

    def parse(self, response):

        # Actor Links
        for sel in response.css('.lister-item-header a::attr(href)'):
            yield response.follow(sel, self.parse_item)

        # Pagination
        # for href in response.css('.lister-page-next.next-page::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_item(self, response):

        # Copy URL for turn-in
        with open('/Users/user/Desktop/lectureMaterials/infoRetrieval/imdb/imdb/spiders/imdbUrls.txt', 'a') as f:
            f.write(response.url+'\n')

        # Set basic actor info
        actor = ImdbItem()
        actor['name'] = response.xpath('//h1/span[@class="itemprop"]/text()').extract()[0]
        actor['img_url'] = response.xpath('//td[@id="img_primary"]/div/a/img/@src').get()
        actor['url'] = response.url
        actor['filmography'] = response.xpath('//div[@class="filmo-category-section"]/div/b/a/text()').extract()


        # Go to biography page
        bio_link = response.xpath('//span/a[text()="See full bio"]/@href').get()
        next_page = response.urljoin(bio_link)
        request = scrapy.Request(next_page, callback=self.get_bio)
        request.meta['actor'] = actor

        yield request



    def get_bio(self, response):

        # Get bio stuff here
        bio = response.xpath("//div[@class='soda odd']/p//text()").extract()
        bio = [item.strip() for item in bio]
        bio = ' '.join(bio)

        # Set bio
        actor = response.meta['actor']
        actor['bio'] = bio

        yield actor
