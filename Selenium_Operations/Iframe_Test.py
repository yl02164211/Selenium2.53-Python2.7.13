#!/usr/bin/env python
#coding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

url = 'http://sahitest.com/demo/index.htm'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)

Iframe_Test = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[6]')
Iframe_Test.click()
time.sleep(5)
driver.implicitly_wait(10)
print driver.current_url
# 进入左边的一个页面
iframes = driver.find_elements_by_xpath('//iframe')
print len(iframes)
driver.switch_to.frame(iframes[0])
Iframe1_link = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[6]')
Iframe1_link.click()
time.sleep(5)
driver.implicitly_wait(10)
print "左边的Iframe count:",driver.find_elements_by_xpath('//iframe')
driver.switch_to.frame(driver.find_elements_by_xpath('//iframe')[0])
# 开始操作第二个Iframe
# 返回上一层Iframe
driver.switch_to.parent_frame()
#切换到第二层的右边的Iframe
driver.switch_to.frame(driver.find_elements_by_xpath('//iframe')[1])
driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[1]').click()
time.sleep(5)
driver.implicitly_wait(10)
time.sleep(5)
# 返回最外层页面
driver.switch_to.default_content()
# 操作右边的frame
driver.switch_to.frame(driver.find_elements_by_xpath('//iframe')[1])
driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[1]').click()
driver.switch_to.parent_frame()
driver.close()
driver.quit()