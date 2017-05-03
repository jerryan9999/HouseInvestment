import requests
import json
import csv
from selenium import webdriver


#config web browser
driver=webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
driver.set_window_size(1024, 768)


def get_ids(url):
  content = requests.get(url).text
  ids = json.loads(content)
  ids = [_id['id'] for _id in ids['content']['results']]
  return ids


def get_info(ids):
  url = 'https://www.mashvisor.com/api/v1.1/neighborhood/{}/marker?_t=QcG6kP3yDnUHD67hWAAQyqrDdFm4gBPW&state=TX'
  items = []
  for _id in ids:
    urls = url.format(_id)
    content = requests.get(urls).text
    result = json.loads(content)
    item = dict()
    item['Neiborghood'] = result['content']['name']
    item['Median_price'] = result['content']['median_price']
    item['cash_on_cash_Airbnb'] = convert(result['content']['airbnb_rental']['roi'])
    item['cash_on_cash_Traditional'] = convert(result['content']['traditional_rental']['roi'])
    item['cap_rate_Airbnb'] = convert(result['content']['airbnb_rental']['cap_rate'])
    item['cap_rete_Traditional'] = convert(result['content']['traditional_rental']['cap_rate'])
    item['optimial_strategy'] = optimial_strategy(result)
    items.append(item)
  return items

def convert(cont):
  if cont == 0:
    return 'N/A'
  elif cont == None:
    return None
  else:
    return str(round(cont, 2)) + '%'

def optimial_strategy(result):
  content = result['content']
  _id = content['id']
  name_city_state= content['name'] + '-' + content['city'] + '-' + content['state']
  # name_city_state: city-center-district-dallas-tx
  name_city_state = name_city_state.lower().replace(' ', '-')
  url = 'https://www.mashvisor.com/explore/#!/neighborhood/{}/{}/demographics'.format(name_city_state, _id)
  driver.get(url)
  optimial_strategy = driver.find_element_by_css_selector('.text-orange-dark').text
  return optimial_strategy

def wirte_csv(items):
  with open('item.csv', 'w') as csvfile:
    fieldnames = ['Neiborghood', 'Median_price', 'cash_on_cash_Airbnb', 'cash_on_cash_Traditional', 'cap_rate_Airbnb', 'cap_rete_Traditional', 'optimial_strategy']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in items:
      writer.writerow(item)

if __name__ == '__main__':
#  url = 'https://www.mashvisor.com/api/v1.1/search/location/pins?state=TX&city=Dallas&minPrice=50000&maxPrice=5000000&payment=CASH&loanType=30&lat=32.7766642&lng=-96.79698789999998&listings=Investment&_t=QcG6kP3yDnUHD67hWAAQyqrDdFm4gBPW'
  url = 'https://www.mashvisor.com/api/v1.1/search/location/pins?state=MA&city=Boston&minPrice=50000&maxPrice=5000000&payment=CASH&loanType=30&lat=42.3600825&lng=-71.05888010000001&listings=Investment&_t=QcG6kP3yDnUHD67hWAAQyqrDdFm4gBPW'
  ids = get_ids(url)  
  items = get_info(ids)
  wirte_csv(items)
