from scrapy.spiders import Spider
from scrapy.shell import inspect_response
from collections import defaultdict
from ..items import ZillowNeighborsItem
from scrapy.http import Request
import datetime
import json
import csv
import re

class NbSpider(Spider):
  name = "NbSpider"

  def start_requests(self):
    #with open("neigh.csv") as f:
    #with open("neigh_seattle.csv") as f:
    with open('test.csv') as f:
      for line in f:
        item  = ZillowNeighborsItem()
        nb = json.loads(line.strip("\n"))
        name = nb['properties']['Name'].strip().replace(' ','-').lower()
        item['name'] = name
        item['state'] = nb['properties']['State']
        item['city'] = nb['properties']['City']
        item['regionID'] = nb['properties']['RegionID']
        city_state = item['city'].strip().replace(' ','-').lower() +"-"+nb['properties']['State']
        #self.logger.info("{},{}".format(city_state,name))
        yield Request(url='https://www.zillow.com/' + name + '-' + city_state + '/home-values/',callback=self.parse_nb,meta={'item':item})

  def parse_nb(self,response):
    item = response.meta['item']
    item['forecast_pct'] = response.xpath('//section[@class="zm-forecast-chart"]/header/ul/li[2]/text()').extract_first()
    item['past_pct'] = response.xpath('//section[@class="zm-forecast-chart"]/header/ul/li[1]/text()').extract_first()
    item['zestimate'] = response.xpath('//div[@class="region-info-item"][1]/h2/text()').extract_first()
    r = Request(url="https://www.zillow.com/ajax/homevalues/data/timeseries.json?r={}&m=zhvi_plus_forecast&dt=1".format(item['regionID']),meta={'item':item},callback=self.parse_graph)
    #print(r.headers,r.cookies,"anzhi")
    return r

    #item['median_rent_price'] = None
    #search_str = ' '.join(response.xpath('//div[@class="region-info-item"][3]/p/text()').extract()).replace('\n','')
    #if search_str:
    #  rent_price_dirty = re.search(r'The median rent price in.+?(\$[0-9,]+)',search_str)  # 当该值取到和城市平均值相等的值时需要特别关注一下
    #  if rent_price_dirty:
    #    item['median_rent_price'] = rent_price_dirty.group(1).rstrip(',')


  def parse_graph(self,response):
    item = response.meta['item']
    a = json.loads(response.body.decode())
    datas_list = a['{};zhvi_plus_forecast;1'.format(item['regionID'])]
    if datas_list:
      data_list = datas_list['data']
    else:
      return item
    for d in data_list:
      d['x'] = datetime.datetime.fromtimestamp(int(str(d['x'])[:-3])).strftime('%Y-%m-%d')
    item['home_value_sale_price'] = data_list
    return Request(url="https://www.zillow.com/ajax/homevalues/data/timeseries.json?r={}&m={}&dt=1".format(item['regionID'],50),meta={'item':item},callback=self.parse_rent)


  def parse_rent(self,response):
    item = response.meta['item']
    #inspect_response(response,self)
    a = json.loads(response.body.decode())
    data_list = a['{};{};1'.format(item['regionID'],50)]['data']
    for d in data_list:
      d['x'] = datetime.datetime.fromtimestamp(int(str(d['x'])[:-3])).strftime('%Y-%m-%d')
    item['home_value_rent_price'] = data_list
    item['crawled_date'] = datetime.datetime.now()

    #inspect_response(response,self)
    item['rent_final_point'] = item['home_value_rent_price'][-1]['y']
    item['forecast_rent_pct'] = "{:.2%}".format(int(item['rent_final_point'])*12/int(item['home_value_sale_price'][-12]['y']))
    sale_point_of_the_past_year = int(item['home_value_sale_price'][-24]['y'])
    rents_within_12_months = [i['y'] for i in item['home_value_rent_price'][-12:]]
    item['past_rent_pct'] = "{:.2%}".format(sum(rents_within_12_months)/sale_point_of_the_past_year)
    item['sale_rent_ratio'] = int(item['home_value_sale_price'][-12]['y'])/(item['rent_final_point']*12)/12



    return item
