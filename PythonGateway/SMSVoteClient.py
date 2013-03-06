#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteClient.py

Created by Peter Meckiffe on 2013-03-06.
Copyright (c) 2013 UWE. All rights reserved.
"""

from flask import Flask, request
from TwilioMessageManager import TwilioMessageManager
from SMSVoteMachine import SMSVoteMachine
from Crypto.PublicKey import RSA
app = Flask(__name__)

@app.route("/", methods=["POST"])
def receiveMessage():
	print request.form["From"]
	print request.form["Body"]
	response = app.jinja_env.globals["machine"].receiveMessage(request.form["From"], request.form["Body"])
	if response["status"]<2:
		app.jinja_env.globals["twilio"].sendMessage(response["message"])
	elif response["status"]==2:
		for message in response["messages"]:
			app.jinja_env.globals["twilio"].sendMessage(message)
	elif response["status"]==5:
		receiveCandidates(response["message"])

@app.route("/setup")
def setup():
	clientKey = RSA.importKey(open("clientKey.txt","r").read())
	servPub = open("clientPub.txt","r").read()
	obj = SMSVoteMachine("+441252236305",clientKey, "abcdefg", [{"telephone":"+442033229681","password":"gfedcba","PK":servPub}])
	app.jinja_env.globals["machine"] = obj
	return "Setup complete"

@app.route("/print")
def yeha():
	for i in app.jinja_env.globals["machine"].data_store.sessions_dictionary:
		print i
	return "yipee"

def receiveCandidates(xml):
	print xml

@app.route("/send")
def send():
	pass

if __name__ == "__main__":
	app.run(debug=True, port=7999, host='0.0.0.0')