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

def search_PageElement(browser, xpathValue):
	# Check the target element by xpath, if found, return object, else return None
	flag = 0 # Element is found 
	locator = (By.XPATH,xpathValue)
	try:
		# Check If the element can be found in 60s 
		webObj = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))	
	except:
		print "Target Element is not found in page after wait 60s."
		flag = 1 # Emelment is not found
		webObj = None

	return (flag,webObj)

def get_ActivePageElement(rootElement, related_path):
	flag = 0
	try:
		webObj = rootElement.find_element_by_xpath(xpath)
	except Exception as e:
		print e
		flag = 1
		webObj = None
	return (flag, webObj)

def get_TotalPageCount(rootElement,related_path):
	flag = 0
	try:
		pagesList = rootElement.find_elements_by_xpath(xpath)
		page_index = 0	# 0代表上一页
		for page in pagesList:
			print page.get_attribute("title"), page.get_attribute('class')
			if page.get_attribute('title') == "下一页":
				page_index = page_index - 1
				totalcount_page = page_index
				break
			else:
				page_index = page_index+1
	except Exception as e:
		print e
		flag = 1

	totalcount = int(pagesList[totalcount_page].get_attribute('title'))
	print "My Orders Page count is :",totalcount
	return totalcount

def action_Security_Verfication(driver):
	'''
	# 淘宝的算法太无语，放弃，人工干预
	times= 1
	while times <10:
		print "Loop %d"%times
		webObj = driver.find_element_by_xpath('//div[@id="nocaptcha"]')
		sliceObj = driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
		ActionChains(driver).drag_and_drop_by_offset(sliceObj, 400, 0).perform()
		time.sleep(5)
		webObj = driver.find_element_by_xpath('//div[@id="nocaptcha"]')
		if webObj.text  == '验证通过':
			flag = 0
			break
		else:
			flag = 1
			times +=1
			driver.refresh()
			driver.implicitly_wait(20)
	return flag
	'''
	print driver.find_element_by_xpath('//*[@id="nc_1_n1t"]').text
	print "等待人为操作"
	time.sleep(30)
	print driver.find_element_by_xpath('//*[@id="nc_1_n1t"]').text
	sliceObj = driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
	if sliceObj.get_attribute('class') =='nc_iconfont btn_ok':
		flag=0
	else:
		flag = 1
	return flag

# Get Taobao Login Acct
yamlfile = 'config.yml'
AcctInfo = get_YMLInfo(yamlfile)
user = AcctInfo['Taobao_ACCT']
pwd = AcctInfo['Taobao_PWD']

# Login Taobao Home Page
url = 'http://login.taobao.com/'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
driver.maximize_window()	
# Login My Taobao
status, mylogin= search_PageElement(driver, '//div[@id="J_QRCodeLogin"]/div[2]')
if status == 0:
	# check the default login type
	default_login = "手机扫码，安全登录"
	normal_login = "密码登录"
	if mylogin.text == default_login:
		# 切换成密码登入
		driver.find_element_by_xpath('//i[@id="J_Quick2Static"]').click()
		driver.implicitly_wait(2)
	# 第一次登入前检查验证码元素是否出现
	status, element_Security = search_PageElement(driver,'//div[@id="nocaptcha"]')
	if status == 1:
		# 激活验证码框		
		driver.find_element_by_xpath('//input[@id="TPL_username_1"]').send_keys(user)
		driver.find_element_by_xpath('//input[@id="TPL_password_1"]').send_keys(pwd)
		time.sleep(1)
		driver.find_element_by_xpath('//button[@id="J_SubmitStatic"]').click()
		driver.implicitly_wait(5)
	# 第二次登入并通过验证码验证，及登入我的淘宝页面
	status, element_Security = search_PageElement(driver,'//div[@id="nocaptcha"]')
	if status == 0:
		move_result = action_Security_Verfication(driver)			
		if move_result ==0:
			print "Auth Passed!"
		else:
			print "Auto Failed!"
	driver.close()			