#coding=utf-8

def singlestar(*args):
	print "accept args length is:", len(args)
	for p in args:
		print p

def doublestars(**kwargs):
	print type(kwargs)
	for key in kwargs:
		print '%s=%s'%(key, kwargs[key])

arr1 = [1,'234',3,'asdfasd']
print '第一次调用'
singlestar(arr1)
print '第二次调用'
arr2 = [1,'234',3,'asdfasd','asygdf923']
singlestar(arr1,arr2)

print '传入词典数据一'
doublestars(a=1,b=2)
dict1={'a':1,'b':2}
print '传入词典数据二'
doublestars(**dict1)
