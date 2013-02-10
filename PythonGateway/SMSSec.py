#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecMessage.py

Created by Peter Meckiffe on 2013-02-03.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from SMSMessage import SMSMessage
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


class SMSSecMessage(SMSMessage):
	def __init__(self, station_telephone, machine_details):
		super(SMSSecMessage, self).__init__(station_telephone, machine_details.telephone_number)
		self.machine_details = machine_details
	
	def createMessage(self, sequence_number, message, AES_key):
		if sequence_number>99:
			raise ValueError("Sequence Number Greater than allowed by SMSSec")
		sequence_number = "{0:02d}".format(sequence_number)
		mode = AES.MODE_CBC
		IV = getIV(self.machine_details.lastIV)
		encryptor = AES.new(AES_key, mode, IV)
		self.message = encryptor.encrypt(message + sequence_number+"END")
		self.machine_details.setLastIV(IV)
		self.machine_details.setCurrentSession(session_id)
	
	def decryptMessage(self, encypted_message, AES_KEY):
		mode = AES.MODE_CBC
		IV = getIV(self.machine_details.lastIV)
		decryptor = AES.new(AES_key, mode, IV)
		plaintext = decryptor.decrypt(encypted_message)
		if(plaintext[-3:]!="END"):
			raise ValueError("AES DECRYPTION FAILED")
		sequence_number = plaintext[-5:-3]
		message = plaintext[:-5]
		return message, sequence_number
	
	def getIV(IV):
		return hashlib.sha256(IV)[0:16]
	
	def authenticateParams(IV,SQ,SID):
		if IV is not None and self.machine_details.lastIV is not None:
			self.machine_details.setLastIV(IV)
		if SID is not None and self.machine_details.session_id is not None:
			if SID == self.machine_details.session_id:
				self.machine_details.setCurrentSession(SID)
			else:
				print SID
				raise ValueError("Incorrect SID. Jump Ship, you're being had.")
		else if SID is not None:
			self.machine_details.setCurrentSession(SID)
		if SQ is not None and self.machine_details.sequence_number is not None:
			if SQ == self.machine_details.sequence_number+1:
				self.machine_details.setSequenceCount(SQ)
			else:
				print SQ
				print self.machine_details.sequence_number
				raise ValueError("Incorrect SQ. Resend?")
		else if SQ is not None:
			self.machine_details.setSequenceCount(SQ)
	

class SMSSecMachineDetails:
	def __init__(self, telephone_number, machine_pass):
		self.telephone_number = telephone_number
		self.machine_pass = machine_pass
		self.sequence_count = None
		self.lastIV = None
		self.session_id = None
	
	def generatePass(self, seed):
		x = hashlib.sha256(str(0)+self.machine_pass+seed)
		for i in range(0,29,1):
			x = hashlib.sha256(x.digest()+self.machine_pass+seed)
		return x.digest()[0:16]
	
	def generateHash(self, session_id):
		return hashlib.sha256(self.telephone_number+self.machine_pass+"{0:08d}".format(session_id)).digest()
	
	def setSequenceCount(num):
		self.sequence_count = num
	
	def setLastIV(IV):
		self.lastIV = IV
	
	def setCurrentSession(session_id):
		self.session_id = session_id
	

class SMSSecMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	sms = SMSSecMessage(12345678,"+442033229681")
	m=sms.createMessage1()
	sms.getMessage1(m)