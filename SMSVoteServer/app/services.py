#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteGateway.py

Created by Peter Meckiffe on 2013-02-10.
Copyright (c) 2013 UWE. All rights reserved.
"""
from app import app
from flask import request, redirect, Response
from CandidateManagement.CandidateModel import CandidateModel
from TwilioMessageManager import TwilioMessageManager
import time
import json
import xml.etree.ElementTree as ET
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *


@app.route("/sendBallots")
def sendBallots():
	# Get candidates list as XML string
	cands = candidates()
	# Connect to DB containing client data
	conn = sqlite3.connect("app/static/data/machines.db")
	machine_model = SMSMachineModel("+442033229681", conn)
	# Init message sender
	twilio = TwilioMessageManager()
	# Get client tel numbers
	clients = machine_model.getAllClients()
	conn.close()
	
	# For each client send the candidate list
	for client in clients:
		# Create a voting machine object for sending/receiveing messages
		machine = SMSVoteMachine("+442033229681",client , "app/static/data/machines.db")
		# Create the message instance
		response = machine.sendMessage(json.dumps(cands))
		# Send the message
		twilio.sendMessage(response["message"])
	return redirect("/viewCandidates")

@app.route("/createElection" methods=["POST"])
def createElection():
	request.form["election_name"]
	request.form["time_start"]
	request.form["time_end"]

@app.route("/testFormat")
def testXmlVsJson():
	candidates = [{"id":1,"first_name":"aaaaa","last_name":"aaaaa","party":"aaaaa"}]
	for i in range(1, 31):
		candidatelist = candidates*i
		#print candidates
		print str(i)+"\t"+str(len(divideMessage(xmlConvert(candidatelist),0)))+ "\t" +str(len(divideMessage(jsonConvert(candidatelist),0)))
	print "\n"
	candidates = [{"id":1,"first_name":"a","last_name":"a","party":"a"}]
	for i in range(1,11):
		candidates[0]['first_name']+="a"
		candidates[0]['last_name']+="a"
		candidates[0]['party']+="a"
		candidatelist = candidates*7
		#print candidates
		print str(i)+"\t"+str(len(divideMessage(xmlConvert(candidatelist),0)))+ "\t" +str(len(divideMessage(jsonConvert(candidatelist),0)))
	import views
	return views.candidates()

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
		print response["message"]
	return "200"

@app.route("/addCandidate", methods=["POST"])
def addCandidate():
	first_name = request.form["first_name"]
	last_name =  request.form["last_name"]
	party = request.form["party"]
	if len(first_name) is not 0 and len(last_name) is not 0:
		if len(party) is 0:
			party = None
		
		con = sqlite3.connect('./app/static/data/candidates.db')
		candidate_model  = CandidateModel(con)
		try:
			candidate_model.addCandidate(first_name, last_name, party)
		except:
			pass
	return redirect("/viewCandidates")

@app.route("/saveCandidates", methods=["GET"])
def saveCandidates():
	f = open("app/static/data/candidates.txt","w")
	f.write(json.dumps(candidates()))
	f.close()
	return redirect("/candidates")
	
def xmlConvert(candidates):
	root = ET.Element('CandidateList')
	for candidate in candidates:
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
		root.append(candidate_element)
	return "<?xml version=\"1.0\" encoding=\"utf-8\"?>"+ET.tostring(root)
	
def jsonConvert(candidates):
	return json.dumps(candidates)
	
def candidates():
	"""Display a table of candidates retrieved from the database"""
	con = sqlite3.connect('./app/static/data/candidates.db')
	candidate_model  = CandidateModel(con)
	candidates = candidate_model.getAllCandidates()
	con.close()
	return candidates
	
	



