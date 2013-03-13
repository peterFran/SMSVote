#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""

from flask import Flask, request
import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from TwilioMessageManager import TwilioMessageManager
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *
from Crypto.PublicKey import RSA
import InitialiseServer
app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SECRET_KEY='gateway'
)


@app.route("/", methods=["POST"])
def receiveMessage():
	print request.form["From"]
	print request.form["Body"]
	machine = SMSVoteMachine("+442033229681", request.form["From"], "gateway.db")
	twilio = TwilioMessageManager()
	response = machine.receiveMessage(request.form["Body"])
	machine.conn.close()
	if response["status"]==-1:
		print "first part of init received"
	elif response["status"]<2:
		twilio.sendMessage(response["message"])
	elif response["status"]==2:
		for message in response["messages"]:
			twilio.sendMessage(message)
	elif response['status']==4:
		print "receiving messages"
	elif response["status"]==5:
		print response["message"]
	return "200"

def setup():	
	InitialiseServer.main()
	return "Setup Complete"

@app.route("/send")
def sendBallots():
	xml = "<CandidateList>"
	for i in CandidateList:
		
	print xml
	conn = sqlite3.connect("gateway.db")
	machine_model = SMSMachineModel("+442033229681", conn)
	twilio = TwilioMessageManager()
	clients = machine_model.getAllClients()
	conn.close()
	for client in clients:
		machine = SMSVoteMachine("+442033229681",client , "gateway.db")
		response = machine.sendMessage(xml)
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
	setup()
	app.run(debug=True, port=8000, host='0.0.0.0')
	

