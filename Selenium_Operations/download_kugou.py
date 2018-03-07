#coding=utf-8

import requests
import re
from urllib import urlencode
import json

baseurl = 'http://www.kugou.com/yy/singer/home/3520.html'
url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash=3C3D93A5615FB42486CAB22024945264&album_id=1645030&_=1520248223241'

req = requests.get(baseurl)
content = req.text

songsinfo = re.findall(r'<script type="text/javascript">(.*?)</script>',content, re.S)
# print len(songsinfo)
i = 0

# for script in songsinfo:
# 	print i+1
# 	print script
# 	i +=1

songslist = songsinfo[0]
# print songslist

songsTotalCount = re.findall(r'songsTotal = (.*?),', songslist,re.S|re.I)
print songsTotalCount[0].replace("'",'')
# songsCount = songsTotalCount[0].replace("'",'')

songsDataNode = re.findall(r'songsdata = (.*?);',songslist,re.S|re.I )

songs_loads= json.loads(songsDataNode[0])
for song in songs_loads:
	# print song
	# print song['album_id']
	albumid = song['album_id']
	break

data = {
	'r':'play/getdata',
	'hash':'E18C99D768BA77F9F2D35E0E0FEF2E42',
	'album_id':555888,
	'_':1520253513692
}

# 试听音乐的实际请求页面URL
# http://www.kugou.com/yy/index.php?r=play/getdata&hash=E18C99D768BA77F9F2D35E0E0FEF2E42&album_id=555888&_=1520253513692

# http://www.kugou.com/yy/index.php?r=play%2Fgetdata&hash=E18C99D768BA77F9F2D35E0E0FEF2E42&_=1520253513692&album_id=555888

baseurl = 'http://www.kugou.com/yy/index.php?'

target_url = baseurl + urlencode(data)
# print target_url

ting_req = requests.get(target_url)
# print ting_req.text

ting_json = json.loads(ting_req.text)
# print ting_json['data']['play_url']
# print ting_json['data']['audio_name']

music_url = ting_json['data']['play_url']
music_name = ting_json['data']['audio_name'] + '.mp3'
print music_name
req = requests.get(music_url)
with open(music_name,'wb') as f:
	f.write(req.content)







# music_url = 'http://fs.w.kugou.com/201803051912/d929740a9a3c9ddd40e852edb5ce0656/G013/M06/18/09/rYYBAFUBVceAQsKQADn6ct4sfQo314.mp3'




# baseurl = 'http://www.kugou.com/yy/singer/home/3520.html'
# 周杰伦 - 告白气球|3C3D93A5615FB42486CAB22024945264|216000

# 试听页面
# http://www.kugou.com/song/#hash=3C3D93A5615FB42486CAB22024945264&album_id=1645030


# http://www.kugou.com/song/#hash=3C3D93A5615FB42486CAB22024945264&album_id=1645030
