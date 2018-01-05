#coding=utf-8

import requests
import re
import urllib
import time

request = requests.Session()

proxies={
'http':'http://proxy.houston.hpecorp.net:8080',
'https':'https://proxy.houston.hpecorp.net:8080'
} 
mp3_data =[]

for page_index in range(2):
	url = 'http://www.htqyy.com/genre/musicList/3?pageIndex='+str(page_index)+'&pageSize=20&order=hot'
	print url
	response = request.get(url,proxies = '')
	content = response.content
	# print response.content
	reg = r'value=\"(.*?)\"><span'	
	sids = re.findall(reg,content,re.S)
	mp3_data.extend(sids)
# print mp3_data
all_song_url = list(map(lambda sid:'http://f1.htqyy.com/play6/'+sid+'/mp3/12', mp3_data))
# print all_song_url
idx = 0 
for idx_url in all_song_url:
	print idx_url, mp3_data[idx]
	# # Method 1: using urllib.urlretrieve
	# try:
	# 	urllib.urlretrieve(idx_url,'./Songs/'+mp3_data[idx]+'.mp3')
	# 	idx = idx +1
	# except Exception,e:
	# 	print e

	# Method 2: using request to save to file
	music_response= request.get(idx_url,proxies='')
	content = music_response.content
	print music_response.status_code
	if music_response.status_code ==200:
		with open('./Songs/%s.mp3'%(mp3_data[idx]),'wb') as f:
				f.write(content)
				f.close()
		idx = idx+1
		music_response.close()