#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import random

PORT_NUMBER = 8080

wordlist = json.load(open('names.json'))

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		rr = random.randint(0,len(wordlist)-1)
		out = wordlist[rr]
		self.wfile.write(json.dumps(out))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	print '[*] serving random name on http://localhost:8080/'
	print '[*] form command line:'
	print '    curl http://localhost:8080/'


	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
