import scrapy

class ActorItem(scrapy.Item):
    name = scrapy.Field()
    url_imdb = scrapy.Field()
    url_rottom = scrapy.Field()
    url_img = scrapy.Field()
    bio_imdb = scrapy.Field()
    bio_rottom = scrapy.Field()
    birthday = scrapy.Field()
    birthplace = scrapy.Field()
    filmography = scrapy.Field()
    quotes_imdb = scrapy.Field()
    quotes_rottom = scrapy.Field()
    quotes_brainyquotes = scrapy.Field()
    movie_urls = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
    url_imdb = scrapy.Field()
    url_rottom = scrapy.Field()
    url_metacritic = scrapy.Field()
    url_img = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    genres = scrapy.Field()
    reviews = scrapy.Field()
    pass

class TmzItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass

class MoviewebItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass

class HollywoodlifeItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass