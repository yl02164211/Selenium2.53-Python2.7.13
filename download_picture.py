#coding=utf-8

import re
import requests
import urllib2,urllib
import chardet

proxies={
'http':'http://proxy.houston.hpecorp.net:8080',
'https':'https://proxy.houston.hpecorp.net:8080'
}

url = 'http://www.xiaohuar.com/list-1-%s.html'
for i in range(1,3):
	new_url = url % i
	print new_url
	response = requests.get(new_url,proxies='')
	html = response.content.decode('gbk').encode('utf-8')
	new_reg = r'<div class="item_t">.*?<a href="http://www.xiaohuar.com/p-\d+-(\d+).*?src="(.*?)" /></a>.*?class="price">(.*?)</span>.*?class="img_album_btn">(.*?)</a>'
	img_urls = re.findall(new_reg,html,re.S|re.M)
	for img_id, img_jpg, img_name, img_school in img_urls:
		hot_reg = r'<em class="bold" id="digg%s">(\d+)</em>'%(img_id)
		img_score=re.findall(hot_reg,html)[0]
		print img_jpg, img_name, img_school, img_score
		img_url = 'http://www.xiaohuar.com'+ img_jpg
		img_response = requests.get(img_url,proxies = '')
		img_data = img_response.content
		filename = img_school + '_' + img_name + "_" + img_score + '.jpg'
		with open('./TuPian/%s'%(filename.decode('utf-8')),'wb+') as f:
			f.write(img_data)
			f.close()
