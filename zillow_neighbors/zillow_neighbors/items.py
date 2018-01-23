# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowNeighborsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    regionID = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    history = scrapy.Field()
    
    forecast_pct = scrapy.Field()
    past_pct = scrapy.Field()
    zestimate = scrapy.Field()
    median_rent_price = scrapy.Field()

    crawled_date = scrapy.Field()

    home_value_sale_price = scrapy.Field()
    home_value_rent_price = scrapy.Field()

    rent_final_point = scrapy.Field()        # 最新的租金
    forecast_rent_pct = scrapy.Field()       # 未来一年的预测的租金收益百分率

    past_rent_pct = scrapy.Field()           # 过去一年的租金收益百分率
    sale_rent_ratio = scrapy.Field()         # 售租比
