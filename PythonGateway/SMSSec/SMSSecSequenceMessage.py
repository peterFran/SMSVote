#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecSequenceMessage.py

Created by Peter Meckiffe on 2013-02-17.
Copyright (c) 2013 UWE. All rights reserved.
"""

from SMSSecMessage import *
from AESCipher import *

class SMSSecSequenceMessage(SMSSecMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecSequenceMessage, self).__init__(recipient_telephone, sender_telephone)
	
	def createMessage(self, message, sequence_number, iv, aes_key):
		encryptor = AESCipher(aes_key)
		SQ = str(sequence_number)
		self.message = encryptor.encrypt(message + SQ, iv)
		print "MESSAGE: ",self.message
		print "SQ:", sequence_number
		print "IV: ", iv
		print "KEY: ", aes_key
	
	def decryptMessage(self, encrypted_message, sequence_number, iv, aes_key):
		print "MESSAGE: ",encrypted_message
		print "SQ: ", sequence_number
		print "IV: ", iv
		print "KEY: ", aes_key
		decryptor = AESCipher(aes_key)
		plaintext = decryptor.decrypt(encrypted_message, iv)
		length = len(str(sequence_number))
		if str(sequence_number) != plaintext[-length:]:
			raise ValueError("AES Decryption Failed")
		message = plaintext[:-length]
		return message
	