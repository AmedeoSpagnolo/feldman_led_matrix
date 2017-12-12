
import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 80
ip = socket.gethostbyname("www.google.com")
client.connect((ip,port))
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
print client.recv(1024)

def comminicate(data):
	client.send(data)
	print client.recv(1024)
	return

communicate("Hello server")
communicate("disconnect")
