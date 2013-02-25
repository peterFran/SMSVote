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
import time
import base64
from SMSMessage import SMSMessage
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


class SMSSecMessage(SMSMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecMessage, self).__init__(recipient_telephone, sender_telephone)
	
	def createMessage(self):
		pass
	
	def decryptMessage(self):
		pass
	

def generatePass(machine_pass, seed):
	x = hashlib.sha256(str(0)+machine_pass+seed)
	for i in range(0,29,1):
		x = hashlib.sha256(x.hexdigest()+machine_pass+seed)
	return x.hexdigest()[0:16]


class SMSSecServerDataStore(object):
	def __init__(self, this_telephone, this_key):
		self.this_telephone = this_telephone
		self.private_key = this_key.export_key()
		self.public_key =this_key.public_key().export_key()
		self.sessions_dictionary = dict()
		self.session_log = dict()
	
	def addDetail(self, recipient_telephone, recipient_password, recipient_PK):
		self.sessions_dictionary[recipient_telephone]={"password":recipient_password,"public_key":recipient_PK,"session":None}
	
	def startNewSession(self, recipient_telephone, session_id, iv, key_params, random_challenge):
		if self.sessions_dictionary[recipient_telephone]["session"] is not None:
			raise ValueError("Session already exists")
		self.sessions_dictionary[recipient_telephone]["session"]=SMSSecSession(recipient_telephone, session_id, iv, key_params, self.sessions_dictionary[recipient_telephone]["password"], random_challenge)
	
	def incrementReceiveSequence(self, recipient_telephone):
		if self.sessions_dictionary[recipient_telephone]["session"] != None:
			self.sessions_dictionary[recipient_telephone]["session"].incrementReceiveSequence()
	
	def incrementSendSequence(self, recipient_telephone):
		if self.sessions_dictionary[recipient_telephone]["session"] != None:
			self.sessions_dictionary[recipient_telephone]["session"].incrementSendSequence()
	
	def getSessionDetails(self, recipient_telephone):
		return self.sessions_dictionary[recipient_telephone]["session"].getDetails()
	
	def addRecievedMessagePart(self, recipient_telephone, message):
		self.sessions_dictionary[recipient_telephone]["session"].receiveMessagePart(message)
	
	def storeMessage(self, recipient_telephone, message):
		self.sessions_dictionary[recipient_telephone]["session"].addMessage(message)
	
	def getBoothPassword(self, recipient_telephone):
		return self.sessions_dictionary[recipient_telephone]["password"]
	
	def endSession(self, recipient_telephone):
		if self.sessions_dictionary[recipient_telephone]["session"]:
			terminated = self.sessions_dictionary[recipient_telephone]["session"].terminate()
			self.session_log[terminated["telephone"]][terminated["session_id"]]=self.sessions_dictionary[recipient_telephone]["session"].getDetails()
			self.sessions_dictionary[recipient_telephone]["session"] = None
	

class AESCipher(object):
	def __init__( self, key ):
		self.key = key 
		BS = 16
		self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
		self.unpad = lambda s : s[0:-ord(s[-1])]
	
	def encrypt( self, raw ,iv):
		raw = self.pad(raw)
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		return base64.b64encode( iv + cipher.encrypt( raw ) ) 
	
	def decrypt( self, enc, iv):
		enc = base64.b64decode(enc)
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		return self.unpad(cipher.decrypt( enc[16:] ))
	

class SMSSecMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	sms = SMSSecMessage(12345678,"+442033229681")
	m=sms.createMessage1()
	sms.getMessage1(m)