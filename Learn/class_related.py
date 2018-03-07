#coding=utf-8

from selenium import webdriver

class DemoClass(object):

	url = 'http://www.jd.com'

	def __init__(self, browser_type = 'Chrome'):
		if browser_type.lower().strip() =='chrome':
			self._driver = webdriver.Chrome
		
		self.driver = None
		self.url = 'http://www.baidu.com'

	def open(self):
		self.driver = self._driver()

	@classmethod # 类方法只能调用类变量
	def get(self, url=url):
		print url
		self.driver.get(url)

a = DemoClass()
a.open()
DemoClass.get()
