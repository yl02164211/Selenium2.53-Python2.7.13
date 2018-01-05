#coding=utf-8

import requests
import re
import urllib

def get_NovelTypeList():
	# Open Home Page
	url = 'http://www.quanshuwang.com/'
	response = urllib.urlopen(url)
	html = response.read().decode('gbk').encode('utf-8')
	# Get One Novel Linkage
	reg = r'<a href="(.*?)" title="(.*?)" class="clearfix">'
	NovelSummaryList = re.findall(reg, html)
	return NovelSummaryList

def get_NovelDetail(url):
	response = urllib.urlopen(url)
	html = response.read().decode('gbk').encode('utf-8')
	response.close()
	reg = r'<a href="(.*?)" class="reader"'
	novelDetail = re.findall(reg, html)
	novel_ChapterUrl= novelDetail[0]
	print novel_ChapterUrl
	response = requests.get(novel_ChapterUrl)
	html_Chapter = response.content.decode('gbk').encode('utf-8')
	response.close()
	reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
	ChaptersList = re.findall(reg, html_Chapter)
	return ChaptersList

def get_ChapterDetail(url):
	response = urllib.urlopen(url)
	html = response.read().decode('gbk').encode('utf-8')
	response.close()
	# print html
	reg = r'>style5\(\);</script>(.*?)<script type="text/javascript">style6'
	chapter = re.findall(reg,html,re.S)
	return chapter[0]

if __name__ == "__main__":
	url = 'http://www.quanshuwang.com/'
	NovelSummaryList= get_NovelTypeList()
	for novel_url,novel_name in NovelSummaryList:
		print novel_url,novel_name
		for chapter_url, chapter_title in get_NovelDetail(novel_url):
			print chapter_url
			print chapter_title
			print get_ChapterDetail(chapter_url)
		break