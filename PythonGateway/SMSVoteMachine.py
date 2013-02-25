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
	def __init__(self, key, clients):
		# Create stores
		self.data_store = SMSSecServerDataStore("+442033229681", key.exportKey(), key.publickey().exportKey())
		for client in clients:
			self.data_store.addDetail(client["telephone"],client["password"],client["PK"])
	
	def receiveMessage(from_field, message_body):
		try:
			if self.data_store.getSessionDetails(from_field) is None:
				# decrypt init
				details = SMSSecInitiatorMessage(self.data_store.this_telephone, from_field).decryptMessage(message_body)
				self.data_store.startNewSession(from_field,details['session_id'], details['iv'], details['key_params'], details['random_challenge'])
				# increment recieved count
				self.data_store.incrementReceiveSequence(from_field)
				# Create responder
				responder = SMSSecResponderMessage(from_field, self.data_store.this_telephone)
				details = self.data_store.getSessionDetails(from_field)
				responder.createMessage(details['random_challenge'], details['send_iv'], details['key'])
				# send responder
				self.sendMessage()
			else if self.data_store.getSessionDetails(from_field)['recieve_sequence']==0:
				# decrypt responder
				responder = SMSSecResponderMessage(from_field, self.data_store.this_telephone)
				details = self.data_store.getSessionDetails(from_field)
				responder.decryptMessage(message_body, details['random_challenge'], details['send_iv'], details['key'])
				# increment recieved count
				self.data_store.incrementReceiveCount(from_field)
				# get message from backburner
				message = details['message']
				# send message
			else:
				# decrypt message
				# increment recieved count
				if contents[-3:] == "END":
					# check store for message, append this message to it, the return
				else:
					# append message to the store
				# add message to contents to data_store
		except:
			print "Recipient machine isn't registered"
	# Returns array of messages for sending to client
	def sendMessage(to_field, message_body):
		try:
			if self.data_store.getSessionDetails(from_field) is None:
				# put message on backburner
				# create init
				# create session
				# increment send count
				# send message.
			else if self.data_store.getSessionDetails(from_field)["send_sequence"] >= 1:
				if message_body is not None:
					# Divide message
					for message in divided_messages:
						# send message
						# increment send count
				else:
					print "Message is empty"
			else:
				# Put message on backburner
				# Shake hands 
		except:
			"Recipient machine doesn't exist"
	
	def divideMessage(to_field, message_body):
		# Length must not excede 95 NORMAL CHARACTERS. SPECIAL CHARS WILL CAUSE INIHILATION

class SMSVoteServerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()