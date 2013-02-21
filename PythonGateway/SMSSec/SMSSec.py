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
	def __init__(self, server_telephone, private_key, public_key):
		self.server_telephone = server_telephone
		self.private_key = private_key
		self.public_key =public_key
		self.booth_current_sessions = dict()
		self.session_log = dict()
	
	def addDetail(self, booth_telephone, booth_password):
		self.booth_current_sessions[booth_telephone]={"password":booth_password,"session":None}
	
	def startNewSession(self, booth_telephone, session_id, iv, key_params, random_challenge):
		if self.booth_current_sessions[booth_telephone]["session"] is not None:
			raise ValueError("Session already exists")
		self.booth_current_sessions[booth_telephone]["session"]=SMSSecSession(booth_telephone, session_id, iv, key_params, self.booth_current_sessions[booth_telephone]["password"], random_challenge)
	
	def incrementReceiveSequence(self, booth_telephone):
		if self.booth_current_sessions[booth_telephone]["session"] != None:
			self.booth_current_sessions[booth_telephone]["session"].incrementReceiveSequence()
	
	def incrementSendSequence(self, booth_telephone):
		if self.booth_current_sessions[booth_telephone]["session"] != None:
			self.booth_current_sessions[booth_telephone]["session"].incrementSendSequence()
	
	def getReceiveSequence(self,booth_telephone):
		return self.booth_current_sessions[booth_telephone]["session"].receive_sequence
	
	def getSendSequence(self,booth_telephone):
		return self.booth_current_sessions[booth_telephone]["session"].send_sequence
	
	def getSessionDetails(self, booth_telephone):
		return self.booth_current_sessions[booth_telephone]["session"].getDetails()
	
	def getBoothPassword(self, booth_telephone):
		return self.booth_current_sessions[booth_telephone]["password"]
	
	def endSession(self, booth_telephone):
		if self.booth_current_sessions[booth_telephone]["session"]:
			self.session_log[self.booth_current_sessions[booth_telephone]["session"].terminate()]=self.booth_current_sessions[booth_telephone]["session"].getDetails()
			self.booth_current_sessions[booth_telephone]["session"] = None
	

class SMSSecSession(object):
	def __init__(self, assoc_telephone, session_id, iv, key_params, booth_password, random_challenge):
		self.aes_key = generatePass(booth_password, key_params)
		self.iv = iv
		self.random_challenge = random_challenge
		self.assoc_telephone = assoc_telephone
		self.session_id = session_id
		self.receive_sequence = 0
		self.send_sequence = 0
		self.time_terminated = None
		self.time_started = self.last_send_increment = self.last_receive_increment = time.time()
	
	def incrementSendSequence(self):
		self.last_send_increment = time.time()
		self.send_sequence+=1
	
	def incrementReceiveSequence(self):
		self.last_receive_increment = time.time()
		self.receive_sequence+=1
	
	def getDetails(self):
		return {"random_challenge":self.random_challenge,
				"telephone":self.assoc_telephone,
				"session_id":self.session_id,
				"send_sequence":self.send_sequence,
				"receive_sequence":self.receive_sequence,
				"key":self.aes_key,
				"send_iv":self._getIV(self.send_sequence),
				"receive_iv":self._getIV(self.receive_sequence),
				"timestarted":self.time_started,
				"last_recieve_at":self.last_receive_increment,
				"last_send_at":self.last_send_increment,
				"terminated":self.time_terminated}
	
	def terminate(self):
		self.time_terminated = time.time()
		return self.session_id
	
	def _getIV(self, SQ):
		IV = self.iv
		for i in range(0,SQ):
			IV = hashlib.sha256(IV).hexdigest()[0:16]
		return IV
	

class SMSSecClientStore(object):
	def __init__(self, booth_telephone, booth_password, server_telephone, server_public_key):
		self.booth_telephone = booth_telephone
		self.booth_password = booth_password
		self.server_telephone = server_telephone
		self.server_public_key = server_public_key
		self.session_log = dict()
		self.current_session = None
	
	def startNewSession(self, session_id, iv, key_params, random_challenge):
		self.endCurrentSession()
		self.current_session = SMSSecSession(self.server_telephone, session_id, iv, key_params, self.booth_password, random_challenge)
	
	def getCurrentSessionDetails(self):
		if self.current_session != None:
			return self.current_session.getDetails()
	
	def endCurrentSession(self):
		if self.current_session != None:
			self.session_log[self.current_session.terminate()]=self.current_session.getDetails
			self.current_session = None
	
	def incrementRecieveSequence(self):
		if self.current_session != None:
			self.current_session.incrementReceiveSequence()
	
	def incrementSendSequence(self):
		if self.current_session != None:
			self.current_session.incrementSendSequence()
	
	def getReceiveSequence(self):
		return self.current_session.receive_sequence
	
	def getSendSequence(self):
		return self.current_session.send_sequence
	

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