#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""

from flask import Flask, request
from TwilioMessageManager import TwilioMessageManager
from SMSVoteMachine import SMSVoteMachine
from Crypto.PublicKey import RSA
app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SECRET_KEY='gateway'
)


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
		print response["message"]

@app.route("/setup")
def setup():
	
	app.jinja_env.globals["twilio"] = TwilioMessageManager()
	servkey = RSA.importKey(open("serverKey.txt","r").read())
	clientPub = open("clientPub.txt","r").read()
	obj = SMSVoteMachine("+442033229681",servkey, "gfedcba", [{"telephone":"+441252236305","password":"abcdefg","PK":clientPub}])
	app.jinja_env.globals["machine"] = obj
	for i in app.jinja_env.globals["machine"].data_store.sessions_dictionary:
		print i
	return "hello"

@app.route("/print")
def yeha():
	for i in app.jinja_env.globals["machine"].data_store.sessions_dictionary:
		print i
	return "yipee"

@app.route("/send")
def sendBallots():
	xml = "<person A>"
	for client in app.jinja_env.globals["machine"].data_store.sessions_dictionary:
		response = app.jinja_env.globals["machine"].sendMessage(client, xml)
		if response["status"]<2:
			print response["message"].message
			app.jinja_env.globals["twilio"].sendMessage(response["message"])
		elif response["status"]==2:
			for message in response["messages"]:
				app.jinja_env.globals["twilio"].sendMessage(message)
		elif response["status"]==5:
			print response["message"]
	return "Ballots sent"

	
if __name__ == "__main__":
	app.run(debug=True, port=8000, host='0.0.0.0')

