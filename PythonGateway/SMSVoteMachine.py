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
from SMSSec.SMSSecInitiatorMessage import *
from SMSSec.SMSSecResponderMessage import *
from SMSSec.SMSSecSequenceMessage import *
from Crypto.PublicKey import RSA
from Crypto import Random


class SMSVoteMachine:
	def __init__(self, this_telephone, key, clients):
		# Create stores
		self.data_store = SMSSecDataStore(this_telephone, key)
		if clients is not None:
			for client in clients:
				self.data_store.addDetail(client["telephone"],client["password"],client["PK"])
	
	def receiveMessage(from_field, message_body):
		try:
			# If recieving an init
			if self.data_store.getSessionDetails(from_field) is None:
				# decrypt init
				init = SMSSecInitiatorMessage(self.data_store.this_telephone, from_field)
				details = init.decryptMessage(message_body, self.data_store.getPassword(from_field), self.data_store.private_key)
				self.data_store.startNewSession(from_field,details['session_id'], details['iv'], details['key_params'], details['random_challenge'])
				# increment recieved count
				self.data_store.incrementReceiveSequence(from_field)
				# send responder
				return self.sendMessage(None)
			
			# If receiving a responder
			elif self.data_store.getSessionDetails(from_field)['recieve_sequence']==0:
				# decrypt responder
				responder = SMSSecResponderMessage(from_field, self.data_store.this_telephone)
				details = self.data_store.getSessionDetails(from_field)
				responder.decryptMessage(message_body, details['random_challenge'], details['send_iv'], details['key'])
				# increment recieved count
				self.data_store.incrementReceiveSequence(from_field)
				# send message
				return self.sendMessage(None)
			
			# If receiving a message
			else:
				# Get session details
				details = self.data_store.getSessionDetails(from_field)
				
				# decrypt message
				message = SMSSecSequenceMessage(self.data_store.this_telephone, from_field)
				decrypted_message = message.decryptMessage(message_body, details["receive_sequence"], details["receive_iv"], details["key"])
				# increment recieved count
				self.data_store.incrementReceiveSequence(from_field)
				# append message to the store
				self.data_store.addRecievedMessagePart(from_field, message)
				details = self.data_store.getSessionDetails(from_field)
				# Check if end
				if details["received_message"][-3:] == "END":
					# check store for message, append this message to it, the return
					return {"status":5,"message":details["received_message"]}
				return {"status":4, "message":details["received_message"]}
		except:
			print "Recipient machine isn't registered"
	
	# Returns array of messages for sending to client
	def sendMessage(to_field, message_body):
		try:
			# If sending an initiator
			if self.data_store.getSessionDetails(to_field) is None:
				# get session id
				session_id = self.data_store.getNewSessionID()
				# put message on backburner
				self.data_store.storeMessage(to_field, message_body)
				# create init
				init = SMSSecInitiatorMessage(to_field, self.data_store.this_telephone)
				details = init.createMessage(self.data_store.getPublicKey(to_field), self.data_store.booth_password, session_id)
				# create session
				self.data_store.startNewSession(to_field, details["session_id"], details["iv"], details["key_params"], details["random_challenge"])
				# increment send count
				self.data_store.incrementSendSequence(to_field)
				# return message.
				return {"status": 0, "message":init}
			
			# If sending a responder
			elif self.data_store.getSessionDetails(to_field)["send_sequence"] == 0 && self.data_store.getSessionDetails(to_field)["receive_sequence"] == 1:
				# Create responder
				responder = SMSSecResponderMessage(to_field, self.data_store.this_telephone)
				details = self.data_store.getSessionDetails(to_field)
				responder.createMessage(details['random_challenge'], details['send_iv'], details['key'])
				return {"status":1, "message":responder, "random_challenge":details['random_challenge'], "iv":details['send_iv'], "key":details['key']}
			
			# If sending a message
			elif self.data_store.getSessionDetails(from_field)["send_sequence"] >= 1:
				if message_body is None and self.data_store.getSessionDetails(to_field)['stored_message'] is not None:
					message_body = self.data_store.getSessionDetails(to_field)['stored_message']
				if message_body is not None:
					# Divide message
					divided_messages = self.divideMessage(message_body)
					messages = []
					for message in divided_messages:
						# increment send count
						details = self.data_store.getSessionDetails(to_field)
						smsMessage = SMSSecSequenceMessage(to_field, self.data_store.this_telephone)
						smsMessage.createMessage(message, details["send_sequence"], details["send_iv"], details["key"])
						messages.append({"message":smsMessage, "sequence":details["send_sequence"],"iv":details["send_iv"],"key":details["key"]})
						self.data_store.incrementSendSequence(to_field)
					return {"status":2, "messages":messages}
					# return message
					
				else:
					print "Message is empty"
		except:
			"Recipient machine doesn't exist"
	
	def divideMessage(self, message_body):
		# Length must not excede 95 NORMAL CHARACTERS. SPECIAL CHARS WILL CAUSE INIHILATION
		output = []
		while len(message_body)>0:
			if len(message_body)<95:
				output.append(message_body)
				message_body = ""
			else:
				output.append(message_body[:95])
				message_body = message_body[95:]
		return output
	
	def actuallySendBloodyMessage(self, message):
		print message

class SMSVoteServerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()