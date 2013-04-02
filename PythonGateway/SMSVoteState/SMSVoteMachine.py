#!/usr/bin/env python
# encoding: utf-8
"""
SMSVoteServer.py

Created by Peter Meckiffe on 2013-02-22.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from SMSMachineModel import SMSMachineModel
from SMSSessionModel import *
from SMSSec.SMSSec import *
from SMSSec.ParameterGenerator import *
from SMSSec.SMSSecInitiatorMessage import *
from SMSSec.SMSSecResponderMessage import *
from SMSSec.SMSSecSequenceMessage import *
from Crypto.PublicKey import RSA
from Crypto import Random
import sqlite3

class SMSVoteMachine(object):
	
	def __init__(self, this_telephone, counterpart_telephone, db_path):
		
		# Create stores
		self.this_telephone = this_telephone
		self.counterpart_telephone = counterpart_telephone
		self.conn = sqlite3.connect(db_path)
		self.machine = SMSMachineModel(this_telephone, self.conn)
		self.counterpart = SMSMachineModel(counterpart_telephone, self.conn)
		self.session = SMSSessionModel(counterpart_telephone, self.conn)
	
	def receiveMessage(self, message_body):
		#try:
			# If recieving an init
			
			if self.session.sessionID()is None:
				# get stored init
				first_part = self.counterpart.getInitiatorPart()
				
				if first_part is not None:
					message_body = first_part + message_body
					self.counterpart.wipeInitiatorPart()
				else:
					self.counterpart.addInitiatorPart(message_body)
					return {"status":-1}
				# decrypt init
				init = SMSSecInitiatorMessage(self.this_telephone, self.counterpart_telephone)
				details = init.decryptMessage(message_body, self.counterpart.getPassword(), self.machine.getPrivateKey())
				print "INITIATOR RECEIVED"
				self.session.initParameters(details['iv'], generate16ByteKey(self.counterpart.getPassword(),details['key_params']), details['random_challenge'], details["number_messages"])
				
				# send responder
				return self.sendMessage(None)
				
			# If receiving a responder
			elif self.session.handshakeComplete()==0:
				# decrypt responder
				responder = SMSSecResponderMessage(self.counterpart_telephone, self.this_telephone)
				responder.decryptMessage(message_body, self.session.randomChallenge(), self.session.getIV(), self.session.key())
				print "Responder Received"
				# Declare handshake finished
				self.session.completeHandshake()
				# send message
				return self.sendMessage(None)
			
			# If receiving a message
			else:
				# Get sequence number
				
				message, sequence_number = message_body.rsplit(":", 1)
				sequence_number = int(sequence_number)
				print message," ", sequence_number
				messages = self.session.addMessage(message, sequence_number)
				if messages is not None:
					session_iv = self.session.getIV()
					sequence_message = SMSSecSequenceMessage(self.this_telephone, self.counterpart_telephone)
					full_message = ""
					for index, message in enumerate(messages):
						iv = calculateIV(session_iv, index)
						decrypted_message = sequence_message.decryptMessage(message, iv, self.session.key())
						full_message += decrypted_message
					self.session.terminate()
					return {"status":5,"message":full_message}
				
				return {"status":4, "message":"Awaiting further messages"}

		#except:
			#print "Recipient machine isn't registered"
	
	# Returns array of messages for sending to client
	def sendMessage(self, message_body):
		#try:
			# If sending an initiator
			if self.session.sessionID() is None:
				# get parameters
				pg = ParameterGenerator(self.machine.getPassword())
				number_messages = len(divideMessage(message_body, 0))
				# create session
				self.session.initParameters(pg.iv, pg.key, pg.random_challenge, number_messages)
				
				# create init
				init = SMSSecInitiatorMessage(self.counterpart_telephone, self.this_telephone)
				details = init.createMessage(self.counterpart.getPublicKey(), self.machine.getPassword(), self.session.sessionID(), pg.iv, pg.key_params, pg.random_challenge, number_messages)
				
				# put message on backburner
				self.session.addStoredMessage(message_body)
				
				# return message.
				self.conn.close()
				return {"status": 0, "message":init}
			
			# If sending a responder
			elif self.session.handshakeComplete() == 0:
				# Create responder
				responder = SMSSecResponderMessage(self.counterpart_telephone, self.this_telephone)
				responder.createMessage(self.session.randomChallenge(), self.session.getIV(), self.session.key())
				self.session.completeHandshake()
				self.conn.close()
				print "Responder sent"
				return {"status":1, "message":responder}
			
			# If sending a message
			elif self.session.handshakeComplete() ==1:
				if message_body is None and self.session.storedMessage() is not None:
					message_body = self.session.storedMessage()
				if message_body is not None:
					# Divide message
					divided_messages = divideMessage(message_body, 0)
					messages = []
					for index, message in enumerate(divided_messages):
						# increment send count
						iv = calculateIV(self.session.getIV(), index)
						smsMessage = SMSSecSequenceMessage(self.counterpart_telephone, self.this_telephone)
						smsMessage.createMessage(message, index, iv, self.session.key())
						messages.append(smsMessage)
					self.session.terminate()
					self.conn.close()
					return {"status":2, "messages":messages}
					# return message
					
				else:
					self.conn.close()
					print "Message is empty"
		#except:
			#"Recipient machine doesn't exist"
	
		
	def __exit__(self, type, value, traceback):
		self.conn.close()
	
def divideMessage(message_body, first_sq):
	# Length must not excede 94 NORMAL CHARACTERS. SPECIAL CHARS WILL CAUSE INIHILATION
	output = []
	count = first_sq
	while len(message_body)>0:
		size = 95 - len(str(count))
		if len(message_body)<size:
			output.append(message_body)
			message_body = ""
		else:
			output.append(message_body[:size])
			message_body = message_body[size:]
			count += 1
	return output
	

if __name__ == '__main__':
	pass
	
	