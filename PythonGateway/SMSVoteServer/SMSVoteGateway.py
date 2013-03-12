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
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *
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
	machine = SMSVoteMachine("+442033229681", request.form["From"])
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
		print response["message"]

@app.route("/setup")
def setup():	
	servkey = RSA.importKey(open("serverKey.txt","r").read())
	clientPub = open("clientPub.txt","r").read()
	obj = SMSVoteMachine("+442033229681",servkey, "gfedcba", [{"telephone":"+441252236305","password":"abcdefg","PK":clientPub}])
	return "Setup Complete"

@app.route("/send")
def sendBallots():
	xml = "<person A>"
	machine = SMSVoteMachine("+442033229681", request.form["From"])
	machine_model = SMSMachineModel("+442033229681")
	twilio = TwilioMessageManager()
	
	for client in machine_model.getAllClients():
		response = machine.sendMessage(client, xml)
		if response["status"]<2:
			print response["message"].message
			twilio.sendMessage(response["message"])
		elif response["status"]==2:
			for message in response["messages"]:
				twilio.sendMessage(message)
		elif response["status"]==5:
			print response["message"]
	return "Ballots sent"

	
if __name__ == "__main__":
	app.run(debug=True, port=8000, host='0.0.0.0')

