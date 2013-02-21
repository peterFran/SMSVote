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
import SMSSec
from SMSSec import SMSSecMessage
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

class SMSSecInitiatorMessage(SMSSecMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecInitiatorMessage, self).__init__(recipient_telephone,sender_telephone)
	
	def createMessage(self, public_key, booth_password, session_id):
		random_challenge = Random.new().read(1)
		key_params = Random.new().read(32)
		IV = Random.new().read(16)
		public_key = RSA.importKey(public_key)
		hashed_parts = hashlib.sha256(self.sender_telephone+booth_password+"{0:08d}".format(session_id)).digest()
		message = self.sender_telephone+":"+hashed_parts+key_params+IV+"{0:08d}".format(session_id)+random_challenge
		self.message = public_key.encrypt(message,32)[0]
		return {"random_challenge":random_challenge, "iv":IV, "key_params":key_params, "session_id":session_id}
	
	def decrypt(self, encrypted_message, booth_password, private_key):
		private_key =RSA.importKey(private_key)
		message = private_key.decrypt(encrypted_message)
		telephone, parts = message.split(":",1)
		session_id = parts[80:88]
		message_hash = parts[:32]
		IV = parts[64:80]
		key_params = parts[32:64]
		random_challenge = parts[88:]
		hash_digest = hashlib.sha256(self.sender_telephone+booth_password+session_id).digest()
		if(message_hash!=hash_digest):
			raise NameError("Hashes don't match")
		return {"from":telephone,"random_challenge":random_challenge, "iv":IV, "key_params":key_params, "session_id":session_id}
	

class SMSSecInitiatorTests(unittest.TestCase):
	def setUp(self):
		pass

if __name__ == '__main__':
	unittest.main()