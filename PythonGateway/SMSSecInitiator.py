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
from SMSSec import *
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

class SMSSecInitiator(SMSSecMessage):
	def __init__(self, station_telephone,machine_details):
		super(SMSSecInitiator, self).__init__(station_telephone,machine_details)
	
	def createMessage(self, public_key, session_id):
		self.random_challenge = Random.new().read(1)
		key_params = Random.new().read(48)
		public_key = RSA.importKey(public_key)
		message = self.sender_telephone+":"+self.machine_details.generateHash(session_id)+key_params+"{0:08d}".format(session_id)+self.random_challenge
		self.authenticateParams(key_params[32:],None,session_id)
		self.message = public_key.encrypt(message,32)
	
	def decrypt(self, encrypted_message, private_key):
		private_key =RSA.importKey(private_key)
		message = private_key.decrypt(encrypted_message[0])
		telephone, parts = message.split(":",1)
		session_id = parts[80:88]
		message_hash = parts[:32]
		IV = parts[64:80]
		print message_hash
		aes_key = self.machine_details.generatePass(parts[32:64])
		random_challenge = parts[88:]
		hash_digest = hashlib.sha256(self.sender_telephone+self.machine_details.machine_pass+session_id).digest()
		
		if(message_hash!=hash_digest):
			raise NameError("Hashes don't match")
		self.machine_details.setLastIV(IV)
		self.machine_details.setCurrentSession(session_id)
		return aes_key, random_challenge
	



class SMSSecInitiatorTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()