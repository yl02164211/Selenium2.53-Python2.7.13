#!/usr/bin/env python
#coding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = 'http://sahitest.com/demo/index.htm'
driver=webdriver.Chrome()
driver.get(url)
time.sleep(5)
driver.implicitly_wait(10)

Visible_Test = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/a[4]')
Visible_Test.click()
driver.implicitly_wait(10)
print driver.current_url

time.sleep(2)
obj_ud = driver.find_element_by_xpath('/html/body/div[@id="ud"]')
print "Before Click, the value is: <",obj_ud.text, "> and the style is: <",obj_ud.get_attribute('style') , ">"

time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[1]').click()
print "Click <Display None> button, the value is: <",obj_ud.text, "> and the style is: <",obj_ud.get_attribute('style'), ">"

time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[2]').click()
print "Click <Display Block> button, the value is: <",obj_ud.text, "> and the style is: <",obj_ud.get_attribute('style'), ">"

time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[3]').click()
print "Click <Display inline> button, the value is: <",obj_ud.text, "> and the style is: <",obj_ud.get_attribute('style'), ">"

time.sleep(2)
obj_uv = driver.find_element_by_xpath('/html/body/div[@id="uv"]')
print "Before Click, the value is: <",obj_uv.text, "> and the style is: <",obj_uv.get_attribute('style') , ">"

time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[4]').click()
print "Click <Visibilty hidden> button, the value is:<",obj_uv.text, "> and the style is: <",obj_uv.get_attribute('style') , ">"

time.sleep(2)
driver.find_element_by_xpath('/html/body/form/input[5]').click()
print "Click <Visibilty visible> button, the value is: <",obj_uv.text, "> and the style is: <",obj_uv.get_attribute('style') , ">"

time.sleep(10)
driver.close()

