#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecHandshakeMessage.py

Created by Peter Meckiffe on 2013-02-05.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from Crypto import Random
from Crypto.PublicKey import RSA
from SMSSecMessage import SMSSecMessage

class SMSSecHandshakeFirstMessage(SMSSecMessage):
	def __init__(self, destination_telephone, sender_telephone):
		super(SMSSecHandshakeFirstMessage, self).__init__(destination_telephone, sender_telephone)
	
	def createMessage(self, machine_pass, public_key, session_id):
		self.random_challenge = Random.new().read(1)
		key_params = Random.new().read(32)
		public_key = RSA.importKey(public_key)
		message = self.sender_telephone+":"+hashlib.sha256(self.sender_telephone+machine_pass+"{0:08d}".format(session_id)).digest()+key_params+"{0:08d}".format(session_id)+self.random_challenge
		self.message = public_key.encrypt(message,32)
	

class SMSSecHandshakeMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()