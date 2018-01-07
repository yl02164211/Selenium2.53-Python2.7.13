#!/usr/bin/env python
#coding=utf-8

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

def goto_nextpage(browser):
	# 检查下是否是最后一页
	if browser.find_element_by_link_text(u"末页").is_displayed():
		links=browser.find_element_by_link_text(u"下一页")
		links.click()
		res = "Continue"
	else:
		res = "Completed"
	time.sleep(5)
	return res

def get_laws_summary(soup,titles,publishs_date,refers_num,docs_link):	
	# 找到所有的tbody标签
	tbodys = soup.find_all('tbody')
	# 法规的内容在最后一个tbody
	tbody = tbodys[-1]
	# print tbody
	# 开始找所有的tr
	trs = tbody.find_all('tr')
	for tr in trs:
		tds = tr.find_all('td')
		if tds[0].attrs['bgcolor']=='#dddddd':
			# 这个是标题栏，所以不需要
			# print "This is title row, ignore it."
			pass
		elif tds[0].attrs['bgcolor']=='#F0F0F0':
			# print 'This row is needed'
			titles.append(tds[0].string)
			publishs_date.append(tds[1].string)
			refers_num.append(tds[2].string)
			docs_link.append(tds[0].a.attrs['href'])
		else:
			# 这个就等有了其他的逻辑之后再添加
			pass
	return (titles,publishs_date,refers_num,docs_link)

def save_toexcel(records):
	titles,publishs_date,refers_num,docs_link = records
	df = pd.DataFrame({
		u'标题':titles,
		u'发布时间':publishs_date,
		u'公文号':refers_num,
		u'文章链接':docs_link
	})
	df.to_excel(u'法规网.xlsx',sheet_name='LawsList')

browser = webdriver.Chrome()
base_url = 'http://hd.chinatax.gov.cn/guoshui/main.jsp'
# 打开法规网 http://hd.chinatax.gov.cn/guoshui/main.jsp
browser.get(base_url)
browser.maximize_window()
browser.implicitly_wait(10)

browser.switch_to.frame("rightList")
print("10秒之后开始抓取数据")
time.sleep(10)
titles = []
publishs_date=[]
refers_num = []
docs_link =[]
# 循环抓取一个系列的数据
while browser.find_element_by_link_text(u"末页").is_displayed():
	# 开始抓取第一页的内容
	iframepage = browser.page_source
	soup =BeautifulSoup(iframepage,'lxml')
	res = get_laws_summary(soup,titles,publishs_date,refers_num,docs_link)
	# 开始抓下一页的内容
	save_toexcel(res)
	try:
		flag = goto_nextpage(browser)
	except Exception,e:
		print "Exception is:",e
		break
	else:
		time.sleep(5)
print "Current page is last one, so the current laws spider is completed."
save_toexcel(res)