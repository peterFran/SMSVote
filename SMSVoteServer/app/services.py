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
import xml.etree.ElementTree as ET


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
	import initElection
	initElection.main()
	import views
	return redirect("/candidates")

@app.route("/removeCandidate", methods=["POST"])
def removeCandidate():
	con = sqlite3.connect('./app/static/data/election.db')
	person_mgt = PersonMgt(con)
	person_mgt.clearCandidate(int(request.form["candidate_id"]),1)
	import views
	return redirect("/candidates")

@app.route("/testFormat")
def testXmlVsJson():
	candidates = [{"id":1,"first_name":"aaaaa","last_name":"aaaaa","party":"aaaaa"}]
	for i in range(1, 31):
		candidatelist = candidates*i
		message = {"election_id":1,"candidate_list":candidatelist}
		#print candidates
		print str(i)+"\t"+str(len(divideMessage(xmlConvert(message),0)))+ "\t" +str(len(divideMessage(jsonConvert(message),0)))
	print "\n"
	candidates = [{"id":1,"first_name":"a","last_name":"a","party":"a"}]
	for i in range(1,11):
		candidates[0]['first_name']+="a"
		candidates[0]['last_name']+="a"
		candidates[0]['party']+="a"
		candidatelist = candidates*7
		message = {"election_id":1,"candidate_list":candidatelist}
		#print candidates
		print str(i)+"\t"+str(len(divideMessage(xmlConvert(message),0)))+ "\t" +str(len(divideMessage(jsonConvert(message),0)))
	import views
	return views.candidates()


def xmlConvert(candidates):
	root = ET.Element('Candidates')
	election_id_element = ET.Element('election_id')
	election_id_element.attrib["election_id"] = unicode(candidates["election_id"])
	root.append(election_id_element)
	candidate_list_element = ET.Element('candidate_list')
	for candidate in candidates["candidate_list"]:
		#Create a child element
		candidate_element = ET.Element('candidate')
		candidate_element.attrib["id"] = unicode(candidate["id"])
		#Create candidate fields
		first_name = ET.SubElement(candidate_element,"first_name")
		last_name = ET.SubElement(candidate_element,"last_name")
		party = ET.SubElement(candidate_element,"party")
		first_name.text = candidate["first_name"]
		last_name.text = candidate["last_name"]
		party.text = candidate["party"]
		candidate_list_element.append(candidate_element)
	root.append(candidate_list_element)
	message = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"+ET.tostring(root)
	#print message
	return message

def jsonConvert(candidates):
	return json.dumps(candidates)


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
	
	



