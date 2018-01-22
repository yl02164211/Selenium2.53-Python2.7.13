#!/usr/bin/env python
#coding=utf-8

import time
from selenium import webdriver

url = 'http://sahitest.com/demo/index.htm'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
# driver.maximize_window()
time.sleep(5)

title = driver.title
print "L1 - current page title is:",driver.title

links = driver.find_elements_by_tag_name('a')
try:
    classlinks = driver.find_elements_by_class_name("a")
except Exception as e:
    print e
    classlinks=None

if classlinks:    
    classlinks[0].click()
    driver.implicitly_wait(10)
    print "L2 - current page title is:",driver.title
    driver.find_element_by_id('linkById').click()
    driver.implicitly_wait(10)
    print "L3 - current page title is:",driver.title
    driver.find_element_by_tag_name('a').click()
    driver.implicitly_wait(10)
    print "L2 - current page title is:",driver.title    
else:
    print "Not found target elements"

print "L2 - current page title is:", driver.title
driver.back()
print "L3 - current page title is:", driver.title
driver.close()