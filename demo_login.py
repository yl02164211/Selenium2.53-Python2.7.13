#coding=utf-8

from selenium import webdriver
import time
import unittest


class DemoUnit(unittest.TestCase):

	url = 'https://mall.imeihao.shop/my'

	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get(self.url)
		self.driver.implicitly_wait(30)

	def tearDown(self):
		self.driver.close()
		self.driver.quit()

	def test_Login(self):
		# 查找登入的按钮并点击登入
		btn_prelogin = self.driver.find_element_by_xpath('//*[@id="mh-scroll-load"]/div/div/div[1]/h2')
		print(btn_prelogin.text)
		btn_prelogin.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)
		login_frame = self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div[1]/h1')
		print(login_frame.is_displayed())
		#检查界面是否显示
		if login_frame.is_displayed():
			print('登入框能正常显示，其标题是：%s'%login_frame.text)
			# 开始定位用户名密码跟登入按钮
			txt_Mobile = self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div[2]/div[1]/input')
			txt_Mobile.send_keys('13713572468')
			txt_Pwd = self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div[2]/div[2]/input')
			txt_Pwd.send_keys('123456789')
			btn_login = self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/button')
			btn_login.click()
			self.driver.implicitly_wait(30)
		else:
			print('登入框没有正确激活。。。。。')

if __name__ == '__main__':
	unittest.main(verbosity=2)
	# suite = unittest.TestSuite()
	# suite.addTest(DemoUnit('test_Login'))
	# runner = unittest.TextTestRunner()
	# runner.run(suite)