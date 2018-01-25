#!/usr/bin/python

import socket
import sys

msg = sys.argv[1]

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
s.sendall(msg)
data = s.recv(1024)
print repr(data)
s.close()
