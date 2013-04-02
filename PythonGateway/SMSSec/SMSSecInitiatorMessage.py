#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecInitiator.py

Created by Peter Meckiffe on 2013-02-09.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from SMSSecMessage import *
from Crypto.PublicKey import RSA
import base64

class SMSSecInitiatorMessage(SMSSecMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecInitiatorMessage, self).__init__(recipient_telephone,sender_telephone)
	
	def createMessage(self, public_key, booth_password, session_id, IV, key_params, random_challenge, number_messages):
		public_key = RSA.importKey(public_key)
		hashed_parts = hashlib.sha256(self.sender_telephone+booth_password+"{0:08d}".format(session_id)).digest()
		message = self.sender_telephone+":"+str(number_messages)+":"+hashed_parts+key_params+IV+"{0:08d}".format(session_id)+random_challenge
		self.message = base64.b64encode(public_key.encrypt(message,32)[0])
	
	def decryptMessage(self, encrypted_message, booth_password, private_key):
		private_key =RSA.importKey(private_key)
		message = private_key.decrypt(base64.b64decode(encrypted_message))
		telephone, number_messages, parts = message.split(":",2)
		number_messages = int(number_messages)
		session_id = parts[80:88]
		message_hash = parts[:32]
		IV = parts[64:80]
		key_params = parts[32:64]
		random_challenge = parts[88:]
		hash_digest = hashlib.sha256(self.sender_telephone+booth_password+session_id).digest()
		if(message_hash!=hash_digest):
			raise NameError("Hashes don't match")
		return {"from":telephone,"random_challenge":random_challenge, "iv":IV, "key_params":key_params, "session_id":session_id, "number_messages":number_messages}
	

class SMSSecInitiatorTests(unittest.TestCase):
	def setUp(self):
		pass

if __name__ == '__main__':
	unittest.main()