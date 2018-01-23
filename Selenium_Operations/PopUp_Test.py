#!/usr/bin/env python
#coding=utf-8

import time
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

url = 'http://sahitest.com/demo/index.htm'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
# 尝试Alert类型的弹出框
Alert_Test=driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/a[1]')
Alert_Test.click()
driver.implicitly_wait(10)
print driver.current_url
driver.find_element_by_xpath('/html/body/form/input[1]').clear()
driver.find_element_by_xpath('/html/body/form/input[1]').send_keys('test alert')
driver.find_element_by_xpath('/html/body/form/input[2]').click()
time.sleep(2)
# 弹出框出现了
print driver.switch_to.alert.text
driver.switch_to.alert.accept()
time.sleep(2)
# 单击Multiline Alert
driver.find_element_by_xpath('/html/body/form/input[3]').click()
time.sleep(2)
print driver.switch_to.alert.text
driver.switch_to.alert.accept()
time.sleep(2)
# 单击Multiline Unicode
driver.find_element_by_xpath('/html/body/form/input[4]').click()
time.sleep(2)
print driver.switch_to.alert.text
driver.switch_to.alert.accept()
time.sleep(2)
driver.implicitly_wait(10)
# 尝试Confirm类型的弹出框
driver.get(url)
driver.implicitly_wait(10)
Confirm_Test=driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/a[2]')
Confirm_Test.click()
driver.implicitly_wait(10)
# 单击确定
driver.find_element_by_xpath('/html/body/form/input[1]').click()
time.sleep(2)
driver.switch_to.alert.accept()
print driver.find_element_by_xpath('/html/body/form/input[2]').get_attribute('value')
# 单击取消
time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[1]').click()
time.sleep(2)
driver.switch_to.alert.dismiss()
print driver.find_element_by_xpath('/html/body/form/input[2]').get_attribute('value')
driver.back()
# 尝试Prompt类型的弹出框
driver.get(url)
driver.implicitly_wait(10)
driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/a[3]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('/html/body/form/input[1]').click()
popup = driver.switch_to.alert
popup.send_keys('test')
popup.accept()
time.sleep(10)
driver.close()