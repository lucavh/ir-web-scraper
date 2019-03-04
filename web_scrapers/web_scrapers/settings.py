# -*- coding: utf-8 -*-

# Scrapy settings for web_scrapers project
#

BOT_NAME = 'web_scrapers'

SPIDER_MODULES = ['web_scrapers.spiders']
NEWSPIDER_MODULE = 'web_scrapers.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'UvaIrBot (+http://www.lucaverhees.nl)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY = 3

# Configure item pipelines
ITEM_PIPELINES = {
    'web_scrapers.pipelines.ActorPipeline': 300
}