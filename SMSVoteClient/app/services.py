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
from SMSVoteState.SMSMachineModel import *
from SMSVoteState.SMSVoteMachine import *
import xml.etree.ElementTree as ET

@app.route("/vote")
def sendVote():
	conn = sqlite3.connect("app/static/data/machines.db")
	machine_model = SMSMachineModel("+442033229681", conn)
	twilio = TwilioMessageManager()
	conn.close()
	machine = SMSVoteMachine("+441252236305","+442033229681" , "app/static/data/machines.db")
	response = machine.sendMessage(xml)
	if response["status"]<2:
		print response["message"].message
		twilio.sendMessage(response["message"])
	elif response["status"]==2:
		for message in response["messages"]:
			twilio.sendMessage(message)
	elif response["status"]==5:
		print response["message"]
	return "Vote sent"

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
		processXML(response["message"])
	return "200"

#@app.route("/addCandidate", methods=["POST"])
# Internal method use only
def processXML(xml):
	# get candidates
	# clear candidates db
	con = sqlite3.connect('./app/static/data/candidates.db')
	f = open('../PythonGateway/CandidateManagement/CandidateSchema.sql','r')
	sql = f.read()
	f.close()
	con.cursor().executescript(sql)
	con.commit()
	# add new candidtes
	candidates = ET.fromstring(xml)
	candidateslist = candidates._children
	for cand in candidateslist:
		child = cand._children
		print child[0].text
		print child[1].text
		print child[2].text
		con.cursor().execute("INSERT INTO candidate(candidate_number, first_name, last_name, party) VALUES(%d,'%s','%s','%s')" 
			% (int(cand.attrib["id"]),child[0].text,child[1].text,child[2].text))
	con.commit()
	
@app.route("/can", methods=["GET"])
def candidates():
	"""Display a table of candidates retrieved from the database"""
	con = sqlite3.connect('./app/static/data/candidates.db')
	candidate_model  = CandidateModel(con)
	candidates = candidate_model.getAllCandidates()
	con.close()
	
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
	return Response("<?xml version=\"1.0\" encoding=\"utf-8\"?>"+ET.tostring(root), mimetype="text/xml")



