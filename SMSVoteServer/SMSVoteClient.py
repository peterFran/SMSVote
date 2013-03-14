#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteClient.py

Created by Peter Meckiffe on 2013-03-06.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from flask import Flask, request
from TwilioMessageManager import TwilioMessageManager
from SMSVoteState.SMSVoteMachine import SMSVoteMachine
from Crypto.PublicKey import RSA
import InitialiseClient
app = Flask(__name__)

@app.route("/", methods=["POST"])
def receiveMessage():
	print request.form["From"]
	print request.form["Body"]
	machine = SMSVoteMachine("+441252236305", request.form["From"], "client.db")
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
		receiveCandidates(response["message"])
	return "200"

def setup():
	InitialiseClient.main()

def receiveCandidates(xml):
	print xml

@app.route("/send")
def send():
	pass

if __name__ == "__main__":
	setup()
	app.run(debug=True, port=7999, host='0.0.0.0')
	
	