#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteClient.py

Created by Peter Meckiffe on 2013-03-06.
Copyright (c) 2013 UWE. All rights reserved.
"""

from flask import Flask, request
from TwilioMessageManager import TwilioMessageManager
from SMSVoteState.SMSVoteMachine import SMSVoteMachine
from Crypto.PublicKey import RSA
app = Flask(__name__)

@app.route("/", methods=["POST"])
def receiveMessage():
	print request.form["From"]
	print request.form["Body"]
	machine = SMSVoteMachine("+441252236305", request.form["From"])
	twilio = TwilioMessageManager()
	response = machine.receiveMessage(request.form["Body"])
	if response["status"]==-1:
		print "first part of init received"
	if response["status"]<2:
		twilio.sendMessage(response["message"])
	elif response["status"]==2:
		for message in response["messages"]:
			twilio.sendMessage(message)
	elif response['status']==4:
		print "receiving messages"
	elif response["status"]==5:
		receiveCandidates response["message"]

@app.route("/setup")
def setup():
	clientKey = RSA.importKey(open("clientKey.txt","r").read())
	servPub = open("clientPub.txt","r").read()
	obj = SMSVoteMachine("+441252236305",clientKey, "abcdefg", [{"telephone":"+442033229681","password":"gfedcba","PK":servPub}])
	return "Setup complete"

def receiveCandidates(xml):
	print xml

@app.route("/send")
def send():
	pass

if __name__ == "__main__":
	app.run(debug=True, port=7999, host='0.0.0.0')