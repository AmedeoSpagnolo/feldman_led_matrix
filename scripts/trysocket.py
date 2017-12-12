
import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8000
ip = socket.gethostbyname("0.0.0.0")
client.connect((ip,port))

# client.send()
# print client.recv(1024)

def communicate(data):
	client.send(data)
	print client.recv(1024)
	return

communicate("GET /favicon.ico HTTP/1.1")

# communicate("disconnect")
