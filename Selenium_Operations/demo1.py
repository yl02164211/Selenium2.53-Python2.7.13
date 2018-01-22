#coding=utf-8

import math

def add(x, y, f):
    return f(x) + f(y)

def f(x):
    return float(x)**0.5

print add(25, 9, f)