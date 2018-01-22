#!/usr/bin/env python
#coding=utf-8

import threading
import time

def thread_main(a):
	global count,mutex
	global count,mutex

	threadname = threading.currentThread().getName()

	for x in xrange(0,int(a)):
		mutex.acquire() #lock
		count = count +1
		mutex.release() #unlock
		print threadname,x,count

def main(num):
	global count,mutex
	threads=[]
	count=1
	mutex=threading.Lock()

	for x in xrange(0,num):
		threads.append(threading.Thread(target=thread_main,args=(5,)))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

if __name__=='__main__':
	num=4
	main(num)

