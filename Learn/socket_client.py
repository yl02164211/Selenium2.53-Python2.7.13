#coding=utf-8

import socket

client = socket.socket()	# 声明socket类型，同时生成socket链接对象
client.connect(('127.0.0.1',12345))

client.send('Hello World!')
client.send('Hello World!')
data = client.recv(1024)
print("recv:",data)

client.close()