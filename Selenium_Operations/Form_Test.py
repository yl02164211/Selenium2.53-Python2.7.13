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
Form_Test=driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/a[2]')
# print Form_Test.get_attribute('class')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 处理Alert
# try:
# 	Form_Test.click()
# 	time.sleep(2)
# 	driver.implicitly_wait(10)
# 	print driver.title
# 	t1_input = 't1_input'
# 	driver.find_element_by_name('t1').send_keys(t1_input)
# except Exception as e:
# 	print e
# 	alert = driver.switch_to_alert()
# 	print alert.text
# 	alert.accept()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 引入EC方法
Form_Test.click()
time.sleep(2)
driver.implicitly_wait(10)
# 等待页面出现alert窗口，超时时间是60秒
WebDriverWait(driver, 60).until(EC.alert_is_present())
# 找到Alert，点击“确定”按钮
# 老版本的语法
# print driver.switch_to_alert().text
# driver.switch_to_alert().accept()
# 新的方法
print driver.switch_to.alert.text
driver.switch_to.alert.accept()
print driver.title
# 操作所有元素对象属性是text的对象
form = driver.find_element_by_name('f1')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Table
# textTable = form.find_elements_by_xpath('//table/tbody/tr')
# for row in textTable:
# 	cols = row.find_elements_by_xpath('td')
# 	row_Text = cols[0].text
# 	print row_Text
# 	try:
# 		cols[1].find_element_by_tag_name('input').send_keys(row_Text)
# 	except Exception as e:
# 		print "Current Row - <%s> is disabled."%(row_Text)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # TextArea
# txtAreas=form.find_elements_by_tag_name('textarea')
# for txtArea in txtAreas:
# 	txtArea.send_keys(random.randint(1,100))
# time.sleep(50)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Checkbox
# checkboxs = form.find_elements_by_xpath('//input[@type="checkbox"]')
# i = 0
# for chbox in checkboxs:
# 	if chbox.get_attribute('name'):
# 		print chbox.get_attribute('value'), chbox.get_attribute('name')
# 		chbox.click()
# 		print chbox.is_selected()
# 	else:
# 		print chbox.get_attribute('value')
# 		chbox.is_selected()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Radio Box
# radioboxs = form.find_elements_by_xpath('//input[@type="radio"]')
# for radio in radioboxs:
# 	print radio.get_attribute('value'), radio.get_attribute('name')
# 	radio.click()
# 	print radio.is_selected()
# 	print "第一个Radio status is： ",radioboxs[0].is_selected()
# 	print "第二个Radio status is： ",radioboxs[1].is_selected()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Password
# pwdboxs= form.find_elements_by_xpath('//input[@type="password"]')
# for pwd in pwdboxs:
# 	print "输入数据前的pwd：",pwd.get_attribute('value')
# 	pwd.send_keys(random.randint(0,100000))
# 	print "输入数据后的pwd：",pwd.get_attribute('value')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Selector 下拉列表, 伴有多种属性，可唯一定位
# selector = Select(form.find_element_by_xpath('//select[@id="s1Id" and @name="s1"]'))
# # Select_by_index()
# sindex = selector.select_by_index(2)
# time.sleep(1)
# driver.switch_to.alert.accept()
# time.sleep(1)
# print 'Current Selected Item is: ',selector.first_selected_option.text
# # Select_by_value()
# sindex = selector.select_by_value('o2')
# time.sleep(1)
# driver.switch_to.alert.accept()
# time.sleep(1)
# print 'Current Selected Item is: ',selector.first_selected_option.text
# # Select_by_visible_text()
# sindex = selector.select_by_visible_text('o1')
# time.sleep(1)
# driver.switch_to.alert.accept()
# time.sleep(1)
# print 'Current Selected Item is: ',selector.first_selected_option.text
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Selector 下拉列表, 有属性，不可唯一定位
# selector = Select(form.find_elements_by_xpath('//select[@id="s1Id"]')[-1])
# sindex = selector.select_by_index(2)
# print 'Current Selected Item is: ',selector.first_selected_option.text
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Selector 下拉列表, 没属性，不可唯一定位
# selector = Select(form.find_elements_by_xpath('//select[not(@multiple)]')[-1])
# sindex = selector.select_by_index(1)
# print 'Current Selected Item is: ',selector.first_selected_option.text
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # Selector 下拉列表, 可多选, 利用反选
# selector = Select(form.find_element_by_xpath('//select[@multiple="multiple"]'))
# # 选一个，
# opts = selector.options
# for opt in opts:
# 	selector.select_by_value(opt.text)
# 	time.sleep(1)
# 	driver.switch_to.alert.accept()
# 	time.sleep(1)
# selected_opts = selector.all_selected_options
# for idx in selected_opts:
# 	print idx.text
# # 取消其中的一个
# selector.deselect_by_index(1)
# time.sleep(1)
# driver.switch_to.alert.accept()
# time.sleep(1)
# # 显示所有选择的item
# selected_opts = selector.all_selected_options
# for idx in selected_opts:
# 	print idx.text
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

time.sleep(20)
driver.close()
