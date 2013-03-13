#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecResponder.py

Created by Peter Meckiffe on 2013-02-09.
Copyright (c) 2013 UWE. All rights reserved.
"""

from SMSSecMessage import *
from AESCipher import *


class SMSSecResponderMessage(SMSSecMessage):
	def __init__(self, recipient_telephone,sender_telephone):
		super(SMSSecResponderMessage, self).__init__(recipient_telephone,sender_telephone)
	
	def createMessage(self, random_challenge, iv, aes_key):
		enc_obj = AESCipher(aes_key)
		message = random_challenge+"0"
		self.message = enc_obj.encrypt(message, iv)
	
	def decryptMessage(self, encrypted_message, random_challenge, iv, aes_key):
		enc_obj = AESCipher(aes_key)
		plaintext = enc_obj.decrypt(encrypted_message, iv)
		sequence_number = plaintext[-1]
		if sequence_number != "0":
			raise ValueError("Sequence number incorrect. Exiting")
		if random_challenge != plaintext[0:1]:
			raise ValueError("Random challenge incorrect. Exiting")
		return True
	

class SMSSecResponderTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()