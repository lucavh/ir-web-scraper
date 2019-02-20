import scrapy

class NewsItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass

class RRItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    rating_10 = scrapy.Field()
    content = scrapy.Field()
    poster_img_url = scrapy.Field()
    cast = scrapy.Field()
    pass
