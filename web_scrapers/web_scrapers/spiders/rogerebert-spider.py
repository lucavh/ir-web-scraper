import scrapy
from web_scrapers.items import RRItem

class RogeRebertSpider(scrapy.Spider):
    name = "rrbot"
    allowed_domains = ["rogerebert.com"]

    start_urls = ["https://www.rogerebert.com/reviews"]

    def start_requests(self):
        for page_start in range(1, 850):
            yield scrapy.Request("https://www.rogerebert.com/reviews?filters%5Bgreat_movies%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=1&filters%5Btitle%5D=&filters%5Breviewers%5D=&filters%5Bgenres%5D=&page={}&sort%5Border%5D=newest".format(page_start))

    def parse(self, response):
        hxs = scrapy.Selector(response)

        review_urls = hxs.select("//*[@id='review-list']/figure/a[@class='poster']/@href").extract()

        for url in review_urls:
            yield scrapy.Request(response.urljoin('https://www.rogerebert.com' + url), callback=self.parse_review)


    def parse_review(self, response):
        item = RRItem()
        item['url'] = response.url
        item['timestamp'] = response.xpath('//time/text()').extract()[0]
        item['title'] = response.xpath('//h1/text()').extract()[0]

        rating = response.xpath('//meta[@itemprop="ratingValue"]/@content').extract()[0]
        max_rating = response.xpath('//meta[@itemprop="bestRating"]/@content').extract()[0]
        item['rating_10'] = round((float(rating)/float(max_rating))*10,2)

        content = ' '.join(response.xpath('//div[@itemprop="reviewBody"]/descendant::p/text()').extract()).replace("\n", "").replace("\t", "")
        item['content'] = content

        item['poster_img_url'] = response.xpath('//div[@class="movie-poster"]/img/@src').extract()[0]

        cast = response.xpath('//section[@class="details"]/ul/descendant::li[@itemprop="actor"]/a/span/text()').extract()
        item['cast'] = cast
        yield item
