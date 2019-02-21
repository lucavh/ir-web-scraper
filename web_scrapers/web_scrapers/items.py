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

class RottenItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    filmography = scrapy.Field()
    bio = scrapy.Field() 
    roles = scrapy.Field()
    offscreen_role = scrapy.Field()
    birthplace = scrapy.Field()
    birthday = scrapy.Field()
    pass
