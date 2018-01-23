# -*- coding: utf-8 -*-

# Scrapy settings for zillow_neighbors project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zillow_neighbors'

SPIDER_MODULES = ['zillow_neighbors.spiders']
NEWSPIDER_MODULE = 'zillow_neighbors.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

#ITEM_PIPELINES = {
#    'zillow_neighbors.pipelines.ZillowNeighborsPipeline' : 400
#}

# Logging 
import time
LOG_LEVEL = 'DEBUG'   # default: 'DEBUG'
#LOG_FILE = "logs/scrapy_%s_%s.log"%(BOT_NAME, int(time.time()))

import yaml
with open("config.yml") as f:
  CONFIG = yaml.load(f)

CONCURRENT_REQUESTS = 1#

DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES ={
  #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
  #'zillow_neighbors.useragent.RotateUserAgentMiddleware':530,
  'scrapy.downloadermiddleware.redirect.RedirectMiddleware':None,
  'zillow_neighbors.redirect.RedirectMiddleware': 600,
}

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en',
    'Authority': 'www.zillow.com'

}

COOKIES_ENABLED = True

#COOKIES_DEBUG = True

ROBOTSTXT_OBEY = False
