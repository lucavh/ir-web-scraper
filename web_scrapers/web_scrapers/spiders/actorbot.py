import scrapy
import requests
from bs4 import BeautifulSoup
from web_scrapers.items import ActorItem

class ImdbbotSpider(scrapy.Spider):
    name = 'actorBot'
    allowed_domains = ['www.imdb.com', 'www.rottentomatoes.com', 'www.brainyquote.com']

    def start_requests(self):
        for rank_start in range(1, 15001, 50):
            yield scrapy.Request("https://www.imdb.com/search/name?gender=male,female&start={}&ref_=rlm".format(rank_start))

    def parse(self, response):
        for sel in response.css('.lister-item-header a::attr(href)'):
            yield response.follow(sel, self.parse_item)

    def parse_item(self, response):
        with open('../data/urls_imdb.txt', 'a') as f:
            f.write(response.url+'\n')

        actor = ActorItem()
        name = response.xpath('//h1/span[@class="itemprop"]/text()').extract()[0]
        actor['name'] = name
        actor['url_imdb'] = response.url
        actor['url_img'] = response.xpath('//td[@id="img_primary"]/div/a/img/@src').get()
        actor['filmography'] = response.xpath('//div[@id="filmography"]/div[@class="filmo-category-section"][1]/div').extract()
        actor['movie_urls'] = response.xpath('//div[@id="filmography"]/div[@class="filmo-category-section"][1]/div/b/a/@href').extract()

        imdb_bio_link = response.xpath('//span/a[text()="See full bio"]/@href').get()
        imdb_bio_page = response.urljoin(imdb_bio_link)

        yield scrapy.Request(imdb_bio_page, callback=self.get_imdb_bio, meta={'actor': actor, 'name':name})

    def get_imdb_bio(self, response):
        with open('../data/urls_imdb_2.txt', 'a') as f:
            f.write(response.url+'\n')

        actor = response.meta['actor']
        name = response.meta['name']

        bio = response.xpath("//div[@class='soda odd']/p//text()").extract()
        bio = ' '.join([item.strip() for item in bio])

        quotes = response.xpath("//*[@id='bio_content']/a[@name='quotes']/following-sibling::div").extract()
        quotes_clean = [BeautifulSoup(quote, "lxml").text.strip() for quote in quotes]

        actor['bio_imdb'] = bio
        actor['quotes_imdb'] = quotes_clean

        rottom_name_link = '_'.join(name.lower().replace('.','').replace('-','').split(' '))
        rottom_link = 'https://www.rottentomatoes.com/celebrity/' + rottom_name_link
        request = requests.get(rottom_link)
        if request.status_code == 404:
            rottom_link = rottom_link.replace('_','-')

        actor['url_rottom'] = rottom_link
        rottom_page = response.urljoin(rottom_link)

        yield scrapy.Request(rottom_page, callback=self.get_rottom, meta={'actor': actor, 'name':name})

    def get_rottom(self, response):
        with open('../data/urls_rottom.txt', 'a') as f:
            f.write(response.url+'\n')

        actor = response.meta['actor']
        name = response.meta['name']

        quotes = response.xpath("//*[@id='main_container']/section/div[1]/section[3]/div/table").extract()
        quotes_clean = [BeautifulSoup(quote, "lxml").text.strip().replace('\n', ' ') for quote in quotes]

        actor['bio_rottom'] = ' '.join(response.xpath("//*[@id='main_container']/section/div[1]/div[1]/section/div/div[3]/div[5]/text()").extract()).strip()
        actor['birthday'] = ' '.join(response.xpath("//*[@id='main_container']/section/div[1]/div[1]/section/div/div[3]/div[3]/text()").extract()).strip()
        actor['birthplace'] = ' '.join(response.xpath("//*[@id='main_container']/section/div[1]/div[1]/section/div/div[3]/div[4]/text()").extract()).strip()
        actor['quotes_rottom'] = quotes_clean

        brainyquotes_name_link = '_'.join(name.lower().replace('.','').replace('-','').split(' '))
        brainyquotes_link = 'https://www.brainyquote.com/authors/' + brainyquotes_name_link
        brainyquotes_page = response.urljoin(brainyquotes_link)

        yield scrapy.Request(brainyquotes_page, callback=self.get_brainyquotes, meta={'actor': actor})

    def get_brainyquotes(self, response):
        with open('../data/urls_brquotes.txt', 'a') as f:
            f.write(response.url+'\n')

        actor = response.meta['actor']
        actor['quotes_brainyquotes'] = response.xpath("//div[@id='quotesList']/div[@class='m-brick grid-item boxy bqQt']/div/div[1]/div/a/text()").extract()

        yield actor
