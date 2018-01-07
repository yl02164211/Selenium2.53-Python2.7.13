#!/usr/bin/env python
#coding=utf-8

import string,time,re,json,csv
import requests,urllib
import pandas as pd

# Filter Options
job_name = '测试'
job_city = '上海'
job_bizArea = '张江'
job_district = '浦东新区'
job_query = {
	'bizArea':job_bizArea,
	'city':job_city,
	'district':job_district,
	'isSchoolJob':0,
	'needAddtionalResult':'true',
	'px':'new'
}

# Create Valid URL
query_string= urllib.urlencode(job_query)
base_url = 'https://www.lagou.com/jobs/positionAjax.json?'
url = base_url+query_string
# Create Valid Referer in headers
job_name_quote = urllib.quote(job_name)
ref_base_url = 'https://www.lagou.com/jobs/list_%s?'%(job_name_quote)
refer_url = ref_base_url + query_string

header ={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Content-Length':'82',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Host':'www.lagou.com',
	'Origin':'https://www.lagou.com',
	'Pragma':'no-cache',
	# 'Referer':'https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95?px=default&city=%E4%B8%8A%E6%B5%B7&district=%E6%B5%A6%E4%B8%9C%E6%96%B0%E5%8C%BA&bizArea=%E5%BC%A0%E6%B1%9F',
	'Referer':refer_url,
	'X-Anit-Forge-Code':'0',
	'X-Anit-Forge-Token':None,
	'X-Requested-With':'XMLHttpRequest'
}

# Start to spider positions from page 1 to page 3
companies = []
positions=[]
positionLablesgroup = []
salaries=[]
workyears = []
educations = []
createdate = [] 

for i in range(1,4):
	data = {
		'first':'true',
		'pn':str(i),
		'kd':job_name
	}
	print "Request:", data
	response = requests.post(url, headers = header, data= data)
	if response.status_code ==200:
		html = response.content
		json_html = json.loads(html)
		# Current Page Positions Info
		jobsList= json_html['content']['positionResult']['result']
		for job in jobsList:
			company = job['companyShortName']
			companies.append(company)
			position = job['positionName']
			positions.append(position)
			positionLables = ';'.join(job['positionLables'])
			positionLablesgroup.append(positionLables)
			salary = job['salary']
			salaries.append(salary)
			workyear = job['workYear']
			workyears.append(workyear)
			education = job['education']
			educations.append(education)
			modified = job['formatCreateTime']
			createdate.append(modified)
	else:
		pass
	time.sleep(10)

# Save positions to excel
df = pd.DataFrame({
	'Company':companies,
	'Position':positions,
	'positionLables':positionLablesgroup,
	'Salary':salaries,
	'WorkYear':workyears,
	'Education':educations,
	'Published':createdate
	})
df.to_csv('lagou.csv',index=False)
df.to_excel('lagou.xlsx',sheet_name='Lagou_Positions')
