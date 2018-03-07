#!/usr/bin/env python
#coding=utf-8

import MySQLdb

host = 'localhost'
user = 'root'
pwd = '!QAZ2wsx'
dbschema = 'demo'
connect = MySQLdb.connect(host,user, pwd, dbschema, charset='utf8')
cursor = connect.cursor()
sql = 'select * from order_jd_d;'
print sql
cursor.execute(sql)
print "Total Count =%d"%cursor.rowcount
dataset = cursor.fetchall()
for record in dataset:
	for item in record:
		print item
cursor.close()
connect.close()