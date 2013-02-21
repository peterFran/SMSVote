#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""


import SimpleHTTPServer
import SocketServer


import SimpleHTTPServer, SocketServer
class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		# self.wfile.write("<html><body>")             
		# 		self.wfile.write("Hello World!")             
		# 		self.wfile.write("</body></html>")
		
		#print self.request.data
		print self.path
		#print dir(self)
		#print self.address_string
		#print self.parse_request()
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	def do_POST(self):
		print dir(self)
		print "success"
			 

Handler = MyHandler
PORT = 8000

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

