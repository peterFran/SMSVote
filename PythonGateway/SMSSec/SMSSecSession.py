#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecSession.py

Created by Peter Meckiffe on 2013-02-23.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import SMSSec
import time
import hashlib


class SMSSecSession(object):
	def __init__(self, assoc_telephone, session_id, iv, key_params, password, random_challenge):
		self.aes_key = SMSSec.generatePass(password, key_params)
		self.iv = iv
		self.random_challenge = random_challenge
		self.assoc_telephone = assoc_telephone
		self.session_id = session_id
		self.receive_sequence = 0
		self.send_sequence = 0
		self.time_terminated = None
		self.stored_message = None
		self.received_message = ""
		self.time_started = self.last_send_increment = self.last_receive_increment = time.time()
	
	def incrementSendSequence(self):
		self.last_send_increment = time.time()
		self.send_sequence+=1
	
	def addMessage(self, message):
		self.stored_message = message
	
	def addReceivedMessagePart(self, message):
		self.received_message += message
	
	def incrementReceiveSequence(self):
		self.last_receive_increment = time.time()
		self.receive_sequence+=1
	
	def getDetails(self):
		return {"random_challenge":self.random_challenge,
				"telephone":self.assoc_telephone,
				"session_id":self.session_id,
				"send_sequence":self.send_sequence,
				"receive_sequence":self.receive_sequence,
				"stored_message":self.stored_message,
				"received_message":self.received_message,
				"key":self.aes_key,
				"send_iv":self._getIV(self.send_sequence),
				"receive_iv":self._getIV(self.receive_sequence),
				"timestarted":self.time_started,
				"last_recieve_at":self.last_receive_increment,
				"last_send_at":self.last_send_increment,
				"terminated":self.time_terminated}
	
	def terminate(self):
		self.time_terminated = time.time()
		return {"telephone": self.assoc_telephone, "session_id":self.session_id}
	
	def _getIV(self, SQ):
		IV = self.iv
		for i in range(0,SQ):
			IV = hashlib.sha256(IV).hexdigest()[0:16]
		return IV



class SMSSecSessionTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()