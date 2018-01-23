# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from datetime import datetime


class ZillowNeighborsPipeline(object):

  def open_spider(self, spider):
    config = spider.settings.get('CONFIG')
    self.client = pymongo.MongoClient(config['mongo_db_neigh']['hosts'])
    self.db = self.client[config['mongo_db_neigh']['database']]
    self.collection = self.db[config['mongo_db_neigh']['collection']]

  def process_item(self, item, spider):
    item['crawled_date'] = datetime.utcnow()
    history = {
              'crawled_date':item['crawled_date'],
              'forecast_pct':item['forecast_pct'],
              'past_pct':item['past_pct'],
              'zestimate':item['zestimate'],
              'median_rent_price':item['median_rent_price']}
    update = {k:v for k,v in item.items() if not k in ['forecast_pct','past_pct','zestimate','median_rent_price']}
    self.collection.update_one({'regionID':item['regionID']},{'$set': update, '$push':{'history':history}},upsert=True)
    return item

  def close_spider(self, spider):
    self.client.close()
