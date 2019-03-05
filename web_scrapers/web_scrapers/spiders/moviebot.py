import scrapy
import requests
from bs4 import BeautifulSoup
from web_scrapers.items import MovieItem
import ast

class ImdbbotSpider(scrapy.Spider):
    name = 'movieBot'
    allowed_domains = ['www.imdb.com', 'www.rottentomatoes.com', 'www.metacritic.com']

    with open('../data/movie_urls.txt') as f:
        urls = ast.literal_eval(f.readlines()[0])

    start_urls = ['https://www.imdb.com' + url.strip() for url in urls]

    def parse(self, response):
        with open('../data/urls_imdb_2.txt', 'a') as f:
            f.write(response.url+'\n')

        movie = MovieItem()

        title = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().strip()

        movie['url_imdb'] = response.url
        movie['url_img'] = response.xpath('//div[@class="poster"]/a/img/@src').extract_first()
        movie['title'] = title
        movie['year'] = response.xpath('//div[@class="title_wrapper"]/h1/span[@id="titleYear"]/a/text()').extract_first()
        movie['genres'] = []
        movie['genres'] += [genre for genre in response.xpath('//*/div[@class="subtext"]/a/text()').extract() if not genre.startswith(('1','2','3','4','5','6','7','8','9','0'))]

        rottom_title_for_link = '_'.join(title.lower().replace('.','').replace('-','').replace(':','').replace(',','').split(' '))
        rottom_movie_link = 'https://www.rottentomatoes.com/m/' + rottom_title_for_link

        # Check if URL exists, otherwise adjust link
        request = requests.get(rottom_movie_link)
        if request.status_code == 404:
            year = response.xpath('//*[@id="titleYear"]/a/text()').extract_first()
            try:
                rottom_movie_link = rottom_movie_link + '_' + year
            except:
                print('Could not find rottentomatoes link.')

        rottom_movie_page = response.urljoin(rottom_movie_link)

        yield scrapy.Request(rottom_movie_page, callback=self.get_rottom_movie, meta={'movie':movie, 'title':title})

    def get_rottom_movie(self, response):
        with open('../data/urls_rottom.txt', 'a') as f:
            f.write(response.url+'\n')

        movie = response.meta['movie']
        title = response.meta['title']

        movie['url_rottom'] = response.url
        movie['reviews'] = [' '.join(response.xpath('//p[@class="mop-ratings-wrap__text mop-ratings-wrap__text--concensus"]/descendant-or-self::*/text()').extract())]

        metacritic_title_for_link = '-'.join(title.lower().replace('.','').replace('-','').split(' '))
        metacritic_movie_link = 'https://www.metacritic.com/movie/' + metacritic_title_for_link
        metacritic_movie_page = response.urljoin(metacritic_movie_link)

        yield scrapy.Request(metacritic_movie_page, callback=self.get_metacritic_movie, meta={'movie':movie})

    def get_metacritic_movie(self, response):
        with open('../data/urls_metacritic.txt', 'a') as f:
            f.write(response.url+'\n')

        movie = response.meta['movie']

        movie['url_metacritic'] = response.url
        movie['genres'] += response.xpath('//div[@class="genres"]/span/span/text()').extract()

        metacr_reviews_link = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[5]/a/@href').get()
        metacr_reviews_page = response.urljoin(metacr_reviews_link)

        yield scrapy.Request(metacr_reviews_page, callback=self.get_metacritic_reviews, meta={'movie': movie})

    def get_metacritic_reviews(self, response):
        with open('../data/urls_metacritic.txt', 'a') as f:
            f.write(response.url+'\n')

        movie = response.meta['movie']
        movie['reviews'] += response.xpath('//div[@class="critic_reviews"]/div/div[2]/div[@class="summary"]/a[1]/text()').extract()

        yield movie
