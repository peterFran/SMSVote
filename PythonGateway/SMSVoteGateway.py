#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""

from flask import Flask, request
app = Flask(__name__)
 
@app.route("/", methods=["POST"])
def hello():
	print request.form["From"]
	print request.form["Body"]
	#print request.data
	# for i in dir(request):
	# 	print i
	return "Hello World!"
 
if __name__ == "__main__":
	app.run(debug=True, port=8000, host='0.0.0.0')

