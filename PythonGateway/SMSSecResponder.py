#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecResponder.py

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

class SMSSecResponder(SMSSecMessage):
	def __init__(self, station_telephone,machine_details):
		super(SMSSecHandshakeResponseMessage, self).__init__(station_telephone,machine_details)
	
	def createMessage(self, random_challenge, AES_key):
		IV = self.getIV(self.machine_details.lastIV)
		mode = AES.MODE_CBC
		encryptor = AES.new(AES_key, mode, IV)
		self.machine_details.setSequenceCount(1)
		self.message = encryptor.encrypt(""+random_challenge+str(1))
		self.machine_details.setLastIV(IV)
		self.machine_details.setCurrentSession(session_id)
		

	def decrypt(self, encrypted_message, AES_key):
		mode = AES.MODE_CBC
		IV = self.getIV(self.machine_details.lastIV)
		decryptor = AES.new(AES_key, mode, IV)
		plaintext = decryptor.decrypt(encrypted_message)
		sequence_number = plaintext.split("||")[-1]
		random_challenge = plaintext[0:1]
		self.machine_details.setLastIV(IV)
		self.machine_details.setCurrentSession(session_id)
		self.
		return sequence_number, random_challenge


class SMSSecResponderTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()