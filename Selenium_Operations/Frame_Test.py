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

Frame_Test = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[5]')
Frame_Test.click()
time.sleep(5)
driver.implicitly_wait(10)
frames = driver.find_elements_by_xpath("//frame")
topframe_name = ''
for subframe in frames:
	if subframe.get_attribute('name'):
		topframe_name = subframe.get_attribute('name')
		print "这个是第一个frame"
	else:
		print "这个是第二个frame"

print "进入第一个Frame:",topframe_name
driver.switch_to.frame(topframe_name)
print "返回最外层frame"
driver.switch_to.default_content();
print "转换到第二个frame"
driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame[2]'))

# 找到Frame_Test Link
Frame_Test2= driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[5]')
Frame_Test2.click()
time.sleep(5)
driver.implicitly_wait(10)
frame2s=driver.find_elements_by_xpath('//frame')
top2frame_name = ''
# 查找在第二个frame下有几个frame返回
for sub2frame in frame2s:
	if sub2frame.get_attribute('name'):
		top2frame_name = sub2frame.get_attribute('name')
		print "这个在Frame2下面的第一个frame"
	else:
		print "这个在Frame2下面的第二个frame"
print "进入Frame2下面的第一个frame:",top2frame_name
driver.switch_to.frame(top2frame_name)
print "返回上一层frame"
driver.switch_to.parent_frame();
print "进入Frame2下面的第二个frame"
driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame[2]'))
print "返回最上层Frame"
driver.switch_to.default_content()


time.sleep(5)
driver.close()

