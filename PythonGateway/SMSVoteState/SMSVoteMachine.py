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
from SMSSec.SMSSec import *
from SMSSec.ParameterGenerator import *
from SMSSec.SMSSecInitiatorMessage import *
from SMSSec.SMSSecResponderMessage import *
from SMSSec.SMSSecSequenceMessage import *
from Crypto.PublicKey import RSA
from Crypto import Random


class SMSVoteMachine(object):
	
	def __init__(self, this_telephone, counterpart_telephone, db_path): #key, password, clients):
		
		# Create stores
		self.this_telephone = this_telephone
		self.counterpart_telephone = counterpart_telephone
		self.machine = SMSMachineModel(this_telephone, db_path)
		self.counterpart = SMSMachineModel(counterpart_telephone)
		self.session = SMSSessionModel(counterpart_telephone, db_path)
		# self.data_store = SMSSecDataStore(this_telephone, key, password)
		# if clients is not None:
		# 	for client in clients:
		# 		self.data_store.addDetail(client["telephone"],client["password"],client["PK"])
	
	def receiveMessage(self, message_body):
		#try:
			# If recieving an init
			if self.counterpart.getSessionID()is None:
				# get stored init
				first_part = self.counterpart.getInitiatorPart()
				if first_part is not None:
					message_body = first_part + message_body
				else:
					self.counterpart.addInitiatorPart(message_body)
					return {"status":-1}
				# decrypt init
				init = SMSSecInitiatorMessage(self.this_telephone, self.counterpart_telephone)
				details = init.decryptMessage(message_body, self.counterpart.getPassword(), self.machine.getPrivateKey())
				self.session.initParams(details['iv'], generate16ByteKey(self.counterpart.getPassword(),details['key_params']), details['random_challenge'])
				# increment recieved count
				self.session.incrementReceiveSequence()
				# send responder
				return self.sendMessage(None)
				
			# If receiving a responder
			elif self.session.receiveSequence()==0:
				# decrypt responder
				responder = SMSSecResponderMessage(self.counterpart_telephone, self.this_telephone)
				responder.decryptMessage(message_body, self.session.randomChallenge(), self.session.receiveIV(), self.session.key())
				# increment recieved count
				self.session.incrementReceiveSequence()
				# send message
				return self.sendMessage(None)
			
			# If receiving a message
			else:
				# decrypt message
				message = SMSSecSequenceMessage(self.this_telephone, self.counterpart_telephone)
				decrypted_message = message.decryptMessage(message_body, self.session.randomChallenge(), self.session.receiveIV(), self.session.key())
				# increment recieved count
				self.session.incrementReceiveSequence()
				# append message to the store
				# If message is last, append to store then return
				if decrypted_message[-3:] == "END":
					decrypted_message=decrypted_message.rstrip("END")
					self.session.addRecievedMessagePart(decrypted_message)
					return {"status":5,"message":self.session.receivedMessage()}
				# Otherwise just append
				self.session.addRecievedMessagePart(decrypted_message)
				return {"status":4, "message":self.session.receivedMessage()}
		#except:
			#print "Recipient machine isn't registered"
	
	# Returns array of messages for sending to client
	def sendMessage(self, message_body):
		#try:
			# If sending an initiator
			if self.session.sessionID() is None:
				# get parameters
				pg = ParameterGenerator(self.counterpart.getPassword())
				
				# create session
				self.session.initParameters(self.counterpart_telephone, pg.iv, pg.key, pg.random_challenge)
				
				# create init
				init = SMSSecInitiatorMessage(self.counterpart_telephone, self.data_store.this_telephone)
				details = init.createMessage(self.counterpart.getPublicKey(), self.machine.getPassword(), self.session.sessionID(), pg.iv, pg.key_params, pg.random_challenge)
				
				# put message on backburner
				self.session.addStoredMessage(message_body)
				
				# increment send count
				self.session.incrementSendSequence()
				
				# return message.
				return {"status": 0, "message":init}
			
			# If sending a responder
			elif self.session.sendSequence() == 0 and self.session.receiveSequence() == 1:
				# Create responder
				responder = SMSSecResponderMessage(self.counterpart_telephone, self.this_telephone)
				responder.createMessage(self.session.randomChallenge(), self.session.sendIV(), self.session.key())
				return {"status":1, "message":responder}
			
			# If sending a message
			elif self.session.sendSequence() >= 1:
				if message_body is None and self.session.storedMessage() is not None:
					message_body = self.session.storedMessage()
				if message_body is not None:
					# Divide message
					message_body+="END"
					divided_messages = self.divideMessage(message_body, self.session.sendSequence())
					messages = []
					for message in divided_messages:
						# increment send count
						smsMessage = SMSSecSequenceMessage(self.counterpart_telephone, self.this_telephone)
						smsMessage.createMessage(message, self.session.sendSequence(), self.session.sendIV(), self.session.key())
						messages.append(smsMessage)
						self.session.incrementSendSequence()
					return {"status":2, "messages":messages}
					# return message
					
				else:
					print "Message is empty"
		#except:
			#"Recipient machine doesn't exist"
	
	def divideMessage(self, message_body, first_sq):
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
	

class SMSVoteServerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()