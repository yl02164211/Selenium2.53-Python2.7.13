#!/usr/bin/env python
#coding=utf-8

from bs4 import BeautifulSoup

soup =BeautifulSoup(open('laws.html'),'lxml')
# print soup.prettify()

# 找到所有的tbody标签
tbodys = soup.find_all('tbody')
# 法规的内容在最后一个tbody
tbody = tbodys[-1]
# print tbody
# 开始找所有的tr
titles = []
publishs_date=[]
refers_num = []
docs_link =[]
trs = tbody.find_all('tr')
for tr in trs:
	tds = tr.find_all('td')
	print len(tds)
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
