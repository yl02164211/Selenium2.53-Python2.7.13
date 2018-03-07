#coding=utf-8

import socket

server=socket.socket()
print('Start')
server.bind(('localhost',12345)) #绑定端口
server.listen(12345) # 监听

while True:
	conn, addr = server.accept() # 等消息
	while True:
		print("new conn", addr)
		data = conn.recv(1024) # recommend 8192 = 8K
		if not data:
			break
		conn.send('You are Welcome')

server.close()

# data = server.recv(1024)
# print("recv:",data)

# server.send(data.upper())

# server.close()
	