#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import random
from pprint import pprint

PORT_NUMBER = 8080
HOST_NAME = 'localhost'

wordlist = json.load(open('../scripts/assets/datasets/names.json'))

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

	#Handler for the POST requests
	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("<html><head><title>Title goes here.</title></head>")
		# self.wfile.write("<body><p>This is a test.</p>")
		# self.wfile.write("<body><form action='.' method='POST'><input type='text' name='xxxxxxxxxxxx' value='0000000000000000000000' /><input type='submit' /></form><p>This is a test.</p>")
		# If someone went to "http://something.somewhere.net/foo/bar/",
		# then s.path equals "/foo/bar/".
		# self.wfile.write("<p>POST: You accessed path: %s</p>" % self.path)
		# self.wfile.write("</body></html>")
		pprint (vars(self))
		# pprint (vars(self.connection))
		# pprint (vars(self.headers))
		# pprint (vars(self.request))
		# pprint (vars(self.rfile))
		# pprint (vars(self.server))
		# pprint (vars(self.wfile))
		# pprint (vars(self.fp))

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
