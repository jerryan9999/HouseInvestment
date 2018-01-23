# -*- utf-8 -*-

from selenium import webdriver
import json
import re
import csv
import time


#config web browser
driver=webdriver.PhantomJS(executable_path='./phantomjs/bin/phantomjs')
driver.set_window_size(1024, 768)

def get_agent_info(agent_url):
  driver.get(agent_url)
  lastHeight = driver.execute_script("return document.body.scrollHeight")
  print('lastHeight:{}'.format(lastHeight))
  #while True:
  for i in range(6):
    driver.execute_script("window.scrollTo(0, {});".format(lastHeight/6))
    time.sleep(3)

  driver.save_screenshot('screen.png')
  item = {}
  item['name'] = driver.find_element_by_css_selector('.chart').text
  item['url'] = agent_url

  return item


if __name__ == '__main__':
  
  urls = ['https://www.zillow.com/seattle-wa/home-values/']

  # prepare item list
  items = []

  for index,url in enumerate(urls):
    #if index<1000:
    try:
      item = get_agent_info(url)
      print(item)
    except Exception as e:
      print(e)
      item = None
      print("Problem for {}".format(url))
    if item:
      print("Finishing #{} for {}".format(index+1,item['name']))
      items.append(item)

  ## writing to file
  #with open("items_{}.csv".format(city),'w') as csvfile:
  #  fieldnames = ['name','url','company','personal_website','addr','experiences','transactions','visitors','comment_num','description']
  #  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  #  writer.writeheader()
  #  for item in items:
  #    writer.writerow(item)




