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
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *
from ElectionMgt.PersonMgt import *
import json

@app.route("/vote", methods=["POST"])
def vote():
	import views
	if authenticate(int(request.form["voter_id"]), 1) is None:
		voted = checkVoted(int(request.form["voter_id"]), 1)
		if voted is None:
			return views.error("Voter ID is not registered")
		else:
			return views.error("%s %s has already voted" % (voted["first_name"], voted["last_name"]))
	message = {"candidate_id":int(request.form["candidate_id"]), "election_id":1}
	message = json.dumps(message)
	print message
	sendSMS(message)
	voter = castVote(int(request.form["voter_id"]), 1)
	return views.success(voter)

def sendSMS(message):
	twilio = TwilioMessageManager()
	machine = SMSVoteMachine("+441252236305","+442033229681" , "app/static/data/machines.db")
	response = machine.sendMessage(message)
	twilio.sendMessage(response["message"])
	
def authenticate(voter_id, election_id):
	conn = sqlite3.connect("app/static/data/election.db")
	person_mgt = PersonMgt(conn)
	voter = person_mgt.getVoter(int(request.form["voter_id"]), election_id)
	return voter

def checkVoted(voter_id, election_id):
	conn = sqlite3.connect("app/static/data/election.db")
	person_mgt = PersonMgt(conn)
	voter = person_mgt.getVoter(int(request.form["voter_id"]), election_id, voted=1)
	return voter

def castVote(voter_id, election_id):
	conn = sqlite3.connect("app/static/data/election.db")
	person_mgt = PersonMgt(conn)
	person_mgt.vote(int(request.form["voter_id"]), election_id)
	voter = person_mgt.getVoter(int(request.form["voter_id"]),election_id,voted=1)
	return voter

@app.route("/", methods=["POST"])
def receiveMessage():
	machine = SMSVoteMachine("+441252236305", request.form["From"], "app/static/data/machines.db")
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
		print response["message"]
	elif response["status"]==5:
		processMessage(response["message"])
	return "200"

def processMessage(message):
	plain_message = json.loads(message)
	if "error" in plain_message or "vote_id" in plain_message:
		printConfirmation(plain_message)
	elif "candidate_list" in plain_message:
		processCandidates(plain_message)
	else:
		print "INVALID MESSAGE"

def processCandidates(plain_message):
	# clear candidates db
	con = sqlite3.connect('./app/static/data/election.db')
	# add new candidtes
	candidates = plain_message["candidate_list"]
	election_id = plain_message["election_id"]
	person_mgt = PersonMgt(con)
	person_mgt.clearCandidates(election_id)
	for candidate in candidates:
		
		print candidate['candidate_id'],"\t",candidate['first_name'],"\t",candidate['last_name'],"\t", candidate['party']
		person_id = person_mgt.addPerson(candidate['first_name'],candidate['last_name'], check=False)
		candidate_id = person_mgt.makeCandidate(person_id, election_id, candidate['party'], candidate_id=candidate['candidate_id'])
	

def printConfirmation(message):
	if "error" in message:
		print "CONFIRMATION RECEIVED FROM SERVER WITH ERROR:\n"+message["error"]
	else:
		print "CONFIRMATION RECEIVED FROM SERVER"
		for i in message:
			print "%s: %s" % (i, message[i])
	

def candidates():
	"""Display a table of candidates retrieved from the database"""
	con = sqlite3.connect('./app/static/data/election.db')
	candidate_model  = PersonMgt(con)
	candidates = candidate_model.getCandidates(1)
	con.close()
	return candidates

