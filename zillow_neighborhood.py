# /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from parsel import Selector
import re
import csv

def get_html(url):
  response = requests.get(url).text
  return response

def parse(response,neighbor):
  ''' parse html and get dict-like item
  '''
  item = {}
  sel = Selector(text=response)
  item['neighbor'] = neighbor
  item['Zestamate_change_pct_past'] = sel.xpath('//section[@class="zm-forecast-chart"]/header/ul/li[1]/text()').extract_first()
  item['Zestamate_change_pct_future'] = sel.xpath('//section[@class="zm-forecast-chart"]/header/ul/li[2]/text()').extract_first()
  item['Zestamate'] = sel.xpath('//div[@class="region-info-item"][1]/h2/text()').extract_first()
  item['median_rent_price'] = None
  search_str = ' '.join(sel.xpath('//div[@class="region-info-item"][3]/p/text()').extract()).replace('\n','')
  if search_str:
    rent_price_dirty = re.search(r'The median rent price in.+?(\$[0-9,]+)',search_str)  # 当该值取到和城市平均值相等的值时需要特别关注一下
    if rent_price_dirty:
      item['median_rent_price'] = rent_price_dirty.group(1).rstrip(',')
  return item

if __name__ == '__main__':
  file = open('items.csv','w',newline='')
  filewriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
  filewriter.writerow(['neighbor','median_rent_price','Zestamate','Zestamate_change_pct_past','Zestamate_change_pct_future'])
  #city_states = 'dallas-tx'
  city_states = 'boston-ma'

  #neighbors = [ 'Eagle Ford', 'Oak Cliff', 'North Dallas', 'South Dallas', 'M Streets', 'Bluffview', 'Cedar Crest', 'City Center District', 'Far North', 'Farmers Market District', 'Government District', 'Lake Caroline', 'Lake Highlands', 'Love Field Area', 'Main Street District', 'Northeast Dallas', 'Oak Lawn', 'Preston Hollow', 'South Boulevard-Park Row Historic', 'Southeast Dallas', 'Southwest Dallas', 'Urbandale-Parkdale', 'West End Historic District', 'Winnetka Heights', 'Wolf Creek', 'Arts District', 'Five Mile Creek', 'Near East', 'Dells District']

  neighbors = ["Haymarket","Mission Hill","Brighton","Kenmore","Roxbury","Bay Village","Beacon Hill","Charlestown","Downtown Crossing","East Boston","Hyde Park","Jamaica Plain","North End","Roslindale","South Boston","West Roxbury","Leather District","Allston","Back Bay","West End","North Dorchester","South Dorchester","South End","Fenway","Government Center","Chinatown",]
  for neighbor in neighbors:
    neighbor_format = neighbor.strip().replace(' ','-').lower()
    url = 'https://www.zillow.com/' + neighbor_format + '-' + city_states + '/home-values/'
    print(url)
#    if url=='https://www.zillow.com/far-north-dallas-tx/home-values/' or url=='https://www.zillow.com/m-streets-dallas-tx/home-values/':
    response = get_html(url)
    item = parse(response,neighbor=neighbor)
    print(item)
    filewriter.writerow([item['neighbor'],item['median_rent_price'],item['Zestamate'],item['Zestamate_change_pct_past'],item['Zestamate_change_pct_future']])
