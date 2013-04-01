#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""
from app import app
from flask import request, redirect, Response
from TwilioMessageManager import TwilioMessageManager
import time
import json
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *
from ElectionMgt.ElectionMgt import *
from ElectionMgt.PersonMgt import *


@app.route("/sendBallots")
def sendBallots():
	# Get candidates list as JSON string
	cands = candidates()
	plain_message = {"election_id":1,"candidate_list":cands}
	message = json.dumps(plain_message)
	# Connect to DB containing client data
	conn = sqlite3.connect("app/static/data/machines.db")
	machine_model = SMSMachineModel("+442033229681", conn)
	
	# Get client tel numbers
	clients = machine_model.getAllClients()
	conn.close()
	print message
	# For each client send the candidate list
	for client in clients:
		# send message to client
		sendSMS(message, client)
	
	return redirect("/candidates")

def sendSMS(message, client):
	# Init message sender
	twilio = TwilioMessageManager()
	# Create a voting machine object for sending/receiveing messages
	machine = SMSVoteMachine("+442033229681",client , "app/static/data/machines.db")
	# Create the message instance
	response = machine.sendMessage(message)
	# Send the message
	twilio.sendMessage(response["message"])
	

@app.route("/clear")
def clearCandidates():
	import initCandidates
	initCandidates.main()
	import views
	return views.candidates()

@app.route("/", methods=["POST"])
def receiveMessage():
	# Create a voting machine instance to decrypt/encrypt messages messages
	machine = SMSVoteMachine("+442033229681", request.form["From"], "app/static/data/machines.db")
	# Init message sender
	twilio = TwilioMessageManager()
	# Create message object
	response = machine.receiveMessage(request.form["Body"])
	machine.conn.close()
	# Depending on stage of message exchange do one of the following
	if response["status"]==-1:
		print "first part of init received"
	elif response["status"]<2:
		twilio.sendMessage(response["message"])
	elif response["status"]==2:
		for message in response["messages"]:
			time.sleep(5)
			twilio.sendMessage(message)
	elif response['status']==4:
		print "receiving messages"
	elif response["status"]==5:
		confirmation = processVote(response["message"])
		if confirmation is None:
			sendSMS(json.dumps({"error":"INVALID CANDIDATE"}), request.form["From"])
		else:
			sendSMS(json.dumps(confirmation), request.form["From"])
	return "200"
	

def countVotes(election_id):
	con = sqlite3.connect('./app/static/data/election.db')
	election_mgt = ElectionMgt(con)
	results = election_mgt.countVotes(election_id)
	return results

def processVote(message):
	con = sqlite3.connect('./app/static/data/election.db')
	vote = json.loads(message)
	election_mgt = ElectionMgt(con)
	return election_mgt.addVote(vote["candidate_id"], vote["election_id"])

@app.route("/addCandidate", methods=["POST"])
def addCandidate():
	first_name = request.form["first_name"]
	last_name =  request.form["last_name"]
	party = request.form["party"]
	if len(first_name) is not 0 and len(last_name) is not 0:
		if len(party) is 0:
			party = None
		
		con = sqlite3.connect('./app/static/data/election.db')
		person_model  = PersonMgt(con)
		try:
			person_id = person_model.addPerson(first_name, last_name)
			candidate_id = person_model.makeCandidate(person_id, 1, party=party)
		except:
			pass
	return redirect("/candidates")

@app.route("/saveCandidates", methods=["GET"])
def saveCandidates():
	f = open("app/static/data/candidates.txt","w")
	f.write(json.dumps(candidates()))
	f.close()
	return redirect("/candidates")
	
def candidates(election_id=1):
	"""Display a table of candidates retrieved from the database"""
	con = sqlite3.connect('./app/static/data/election.db')
	people  = PersonMgt(con)
	candidates = people.getCandidates(election_id)
	for candidate in candidates:
		del(candidate["person_id"])
		del(candidate["election_id"])
	con.close()
	return candidates
	
	



