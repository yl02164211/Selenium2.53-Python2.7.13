#!/usr/bin/env python
#coding=utf-8

import yaml,os,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def get_YMLInfo(yamlfile): 
	if os.path.exists(yamlfile):
		with open(yamlfile,'rb') as f:
			config_info = yaml.load(f)
	else:
		print "文件找不到。"
		config_info = None
	return config_info

def find_element_By_displayed(driver, element_xpath,wait_seconds=60):
	# Check the target element by xpath, if found, return object, else return None
	webObj = None
	seconds_wait = 0
	while seconds_wait<wait_seconds:
		if driver.find_element_by_xpath(element_xpath).is_displayed():
			webObj = driver.find_element_by_xpath(element_xpath)
			break
		else:
			time.sleep(1)
			seconds_wait +=1	
	
	print "等待目标元素出现用时：%ds; 默认等待时间60s"%seconds_wait	
	return webObj

def action_Security_Verfication(driver):
	'''
	淘宝的算法太复杂，决定人工干预
	ActionChains(driver).drag_and_drop_by_offset(sliceObj, 400, 0).perform()
	'''
	print "等待人为操作， 持续30秒"
	time.sleep(30)
	sliceObj = driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
	if sliceObj.get_attribute('class') =='nc_iconfont btn_ok':
		flag=0
	else:
		flag = 1
	return flag

def check_NextPage_Status(element_pagebar):
	childpages = element_pagebar.find_elements_by_tag_name('li')				
	# 检查下一页的class属性
	if childpages[-1].get_attribute('title') == '下一页':
		if childpages[-1].get_attribute('class') == 'pagination-next':
			flag = True	
		elif childpages[-1].get_attribute('class') == 'pagination-disabled pagination-next':
			flag = False
		else:
			pass
	return flag

def goto_NextPage(driver,element_pagebar):
	childpages = element_pagebar.find_elements_by_tag_name('li')				
	if childpages[-1].get_attribute('title') == '下一页':
		if childpages[-1].get_attribute('class') == 'pagination-next':
			childpages[-1].click()
			time.sleep(30)

def get_ActivePageNo(element_pagebar):
	pageNO = None
	childpages = element_pagebar.find_elements_by_tag_name('li')
	for childpage in childpages:
		if childpage.get_attribute('class').endswith('pagination-item-active'):
			pageNo = childpage.get_attribute('title')
			break
	return pageNO

def get_OrdersList_In_ActivePage(driver, element_OrderList, element_pagebar):
	activePageNo = get_ActivePageNo(element_pagebar)
	print "Current Page No is: %s"%activePageNo
	time.sleep(5)


# Get Taobao Login Acct
yamlfile = 'config.yml'
AcctInfo = get_YMLInfo(yamlfile)
user = AcctInfo['Taobao_ACCT']
pwd = AcctInfo['Taobao_PWD']

url = 'http://login.taobao.com'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(30)
driver.maximize_window()

# 打开登入页面，查找登入的DIV是否出现
rootNode_Login= find_element_By_displayed(driver, '//div[@id="J_LoginBox"]', 30)
if rootNode_Login:
	# 默认登入页面是手机扫码登入，	
	# 检查-密码登入并切换到密码登入页面
	xpath = '//div[@id="J_QRCodeLogin"]/div[5]/a[1]'
	if driver.find_element_by_xpath(xpath).is_displayed():
		driver.find_element_by_xpath(xpath).click()
		time.sleep(2)
	
	print driver.find_element_by_xpath('//div[@id="J_StaticForm"]/div').text
	# 检查验证框是否存在，默认返回None
	authnode_Login = find_element_By_displayed(driver,'//div[@id="nocaptcha"]',10)
	if not authnode_Login: 
		# 激活验证码框		
		driver.find_element_by_xpath('//input[@id="TPL_username_1"]').send_keys(user)
		driver.find_element_by_xpath('//input[@id="TPL_password_1"]').send_keys(pwd)
		driver.find_element_by_xpath('//button[@id="J_SubmitStatic"]').click()
		driver.implicitly_wait(5)
	# 默认验证码元素应该出现在页面上
	authnode_Login = find_element_By_displayed(driver,'//div[@id="nocaptcha"]',10)	
	auth_result = action_Security_Verfication(driver)			
	if auth_result == 0:
		driver.find_element_by_xpath('//input[@id="TPL_username_1"]').clear()
		driver.find_element_by_xpath('//input[@id="TPL_username_1"]').send_keys(user)
		driver.find_element_by_xpath('//input[@id="TPL_password_1"]').clear()
		driver.find_element_by_xpath('//input[@id="TPL_password_1"]').send_keys(pwd)
		driver.find_element_by_xpath('//button[@id="J_SubmitStatic"]').click()
		driver.implicitly_wait(10)
		# 打开我的淘宝的主页
		xpath = '/html/body/header/article/div/a' # 我的淘宝		
		myTaobao_Home = find_element_By_displayed(driver, xpath, 60)
		if myTaobao_Home:
			xpath = '//a[@id="bought"]'
			myOrders_Home = find_element_By_displayed(driver, xpath, 30)
			myOrders_Home.click()
			# 订单页面的同步
			driver.implicitly_wait(30)
			# 判断所有订单的页面数
			xpath = '//div[@id="tp-bought-root"]/div[19]/div[2]/ul'
			pageBar = find_element_By_displayed(driver, xpath, 30)
			# 通过点击下一页来循环所有的订单页面
			while check_NextPage_Status(pageBar):
				print "Current Page No is:", get_ActivePageNo(pageBar)
				# get_OrdersList_In_ActivePage(driver, '/html', pageBar)
				i = 1
				while i < 7:
					js = "var q=document.body.scrollTop=300000"
					driver.execute_script(js)
					time.sleep(1)
					i +=1
				goto_NextPage(driver,pageBar)
driver.quit()