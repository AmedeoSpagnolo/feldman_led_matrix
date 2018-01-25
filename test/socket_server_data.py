#!/usr/bin/python
import socket

s = socket.socket()
host = socket.gethostname() # Get local machine name
port = 12345

s.bind((host, port))
s.listen(5)                 # Now wait for client connection.

while True:

   # Establish connection with client.
   c, addr = s.accept()
   print('Got connection from', addr)

   data = c.recv(1024)
   if not data: break
   print "data: %s" % data

   c.send("Thank you for connecting: %s" % data)
   # c.close()
