#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""
from app import app
from flask import request, redirect
from CandidateManagement.CandidateModel import CandidateModel
from TwilioMessageManager import TwilioMessageManager
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *

@app.route("/vote")
def sendVote():
	xml = "<CandidateList>"
	print xml
	conn = sqlite3.connect("app/static/data/machines.db")
	machine_model = SMSMachineModel("+442033229681", conn)
	twilio = TwilioMessageManager()
	clients = machine_model.getAllClients()
	conn.close()
	for client in clients:
		machine = SMSVoteMachine("+442033229681",client , "app/static/data/machines.db")
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

@app.route("/", methods=["POST"])
def receiveMessage():
	machine = SMSVoteMachine("+442033229681", request.form["From"], "app/static/data/machines.db")
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
		processXML(response["message"])
	return "200"

#@app.route("/addCandidate", methods=["POST"])
# Internal method use only
def processXML(xml):
	# get candidates
	# clear candidates db
	# add new candidtes
	
def addCandidate(candidate):
	first_name = candidate["first_name"]
	last_name =  candidate["last_name"]
	party = candidate["party"]
	con = sqlite3.connect('./app/static/data/candidates.db')
	candidate_model  = CandidateModel(con)
	try:
		candidate_model.addCandidate(first_name, last_name, party)
	except:
		pass
	return redirect("/candidates")




