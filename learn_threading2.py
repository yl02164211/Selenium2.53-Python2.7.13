#!/usr/bin/env python
#coding=utf-8

import threading
import time

class TestThread(threading.Thread):
	def __init__(self,num):
		threading.Thread.__init__(self)
		self._run_nmu=num

	def run(self):
		global count,mutex
		threadname = threading.currentThread().getName()

		for x in xrange(0,int(self._run_nmu)):
			mutex.acquire() #lock
			count = count +1
			mutex.release() #unlock
			print threadname,x,count

if __name__=='__main__':
	global count,mutex
	threads=[]
	num,count=4,1
	
	mutex=threading.Lock()

	for x in xrange(0,num):
		threads.append(TestThread(8))
	for t in threads:
		t.start()
	for t in threads:
		t.join()