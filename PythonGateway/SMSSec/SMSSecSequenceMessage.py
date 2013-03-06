#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecSequenceMessage.py

Created by Peter Meckiffe on 2013-02-17.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from SMSSec import *
from Crypto import Random

class SMSSecSequenceMessage(SMSSecMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecSequenceMessage, self).__init__(recipient_telephone, sender_telephone)
	
	def createMessage(self, message, sequence_number, iv, aes_key):
		encryptor = AESCipher(aes_key)
		SQ = str(sequence_number)
		self.message = encryptor.encrypt(message + SQ, iv)
	
	def decryptMessage(self, encrypted_message, sequence_number, iv, aes_key):
		decryptor = AESCipher(aes_key)
		print encrypted_message
		plaintext = decryptor.decrypt(encrypted_message, iv)
		length = len(str(sequence_number))
		if str(sequence_number) != plaintext[-length:]:
			raise ValueError("AES Decryption Failed")
		message = plaintext[:-length]
		return message
	