# -*- coding: utf-8 -*-

# Define your item pipelines here
#
import json
from web_scrapers.items import ActorItem, MovieItem, TmzItem, MoviewebItem, HollywoodlifeItem

class ActorPipeline(object):
    def __init__(self):
      self.movie_urls = []

    def open_spider(self, spider):
      self.file_actors = open('../data/actors.jl', 'a')
      self.file_movies = open('../data/movies.jl', 'a')
      self.file_tmz = open('../data/news_tmz.jl', 'a')
      self.file_movieweb = open('../data/news_movieweb.jl', 'a')
      self.file_hollywoodlife = open('../data/news_hollywoodlife.jl', 'a')

    def process_item(self, item, spider):
      line = json.dumps(dict(item)) + "\n"

      if isinstance(item, ActorItem):
        self.file_actors.write(line)
        self.movie_urls += item['movie_urls']
      elif isinstance(item, MovieItem):
        self.file_movies.write(line)
      elif isinstance(item, TmzItem):
        self.file_tmz.write(line)
      elif isinstance(item, MoviewebItem):
        self.file_movieweb.write(line)
      elif isinstance(item, HollywoodlifeItem):
        self.file_hollywoodlife.write(line)

      return

    def close_spider(self, spider):
      self.file_actors.close()
      self.file_movies.close()
      self.file_tmz.close()
      self.file_movieweb.close()
      self.file_hollywoodlife.close()

      if self.movie_urls != []:
        self.file_urls = open('../data/movie_urls.txt', 'w')
        self.file_urls.write(str(list(set(self.movie_urls))))
        self.file_urls.close()
