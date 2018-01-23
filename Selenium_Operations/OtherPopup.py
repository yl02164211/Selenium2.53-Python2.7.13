#!/usr/bin/env python
#coding=utf-8

import time
from selenium import webdriver

url = 'http://sahitest.com/demo/index.htm' 
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/a[4]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('/html/body/button').click()
print driver.switch_to.alert.text
driver.switch_to.alert.accept()
time.sleep(2)
print driver.switch_to.alert.text
driver.switch_to.alert.dismiss()
time.sleep(2)
print driver.switch_to.alert.text
popup = driver.switch_to_alert()
popup.send_keys("Hello")
driver.switch_to.alert.accept()
time.sleep(10)
driver.close()
# 测试用
# url = 'file:///C:/Github_Python/Python2.7-Selenium2.53/Selenium_Operations/popup.html'
# driver = webdriver.Chrome()
# driver.get(url)
# time.sleep(5)
# driver.find_element_by_xpath('//input[@id="prompt"]').click()
# time.sleep(3)
# popup = driver.switch_to.alert
# print popup.text
# popup.send_keys("hello world")
# driver.switch_to.alert.accept()
# time.sleep(3)
# print driver.find_element_by_xpath('/html/body').text
