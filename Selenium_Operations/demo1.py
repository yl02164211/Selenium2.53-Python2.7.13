#coding=utf-8

import math

def add(x, y, f):
    return f(x) + f(y)

def f(x):
    return float(x)**0.5

a = None

if a:
	print "True"
else:
	print "False"

a = '1234567890-wertyui'
print a.endswith('i')