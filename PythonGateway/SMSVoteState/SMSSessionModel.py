#!/usr/bin/env python
# encoding: utf-8
"""
SMSStateModel.py

Created by Peter Meckiffe on 2013-03-11.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sqlite3
import time
import hashlib
import base64
from ErrorIgnore import ErrorIgnore

class SMSSessionModel:
	def __init__(self, recipient_telephone, conn):
		self.recipient_telephone = recipient_telephone
		self.conn = conn
	
	def close(self):
		self.conn.close()
	
	def initParameters(self, iv, key, random_challenge, number_messages):
		iv = base64.b64encode(iv)
		random_challenge = base64.b64encode(random_challenge)
		c = self.conn.cursor()
		c.execute("SELECT * FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()
		if c is None:
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge, timestarted, number_messages) values('%s', '%s', '%s', '%s', %f, %d)" % (self.recipient_telephone, iv, key, random_challenge, time.time(),number_messages))
		else:
			c.execute("UPDATE session SET terminated='%s' where telephone='%s' and terminated = 0" % (time.time(), self.recipient_telephone))
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge, timestarted, number_messages) values('%s', '%s', '%s', '%s', %f, %d)" % (self.recipient_telephone, iv, key, random_challenge, time.time(), number_messages))
		self.conn.commit()
		return c.execute("SELECT session_id FROM session WHERE telephone='%s' AND terminated=0" % self.recipient_telephone).fetchone()[0]
	
	def key(self):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def randomChallenge(self):
		c = self.conn.cursor()
		return base64.b64decode(c.execute("SELECT random_challenge FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0])
	
	def handshakeComplete(self):
		c = self.conn.cursor()
		return c.execute("SELECT handshake_complete FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def completeHandshake(self):
		c = self.conn.cursor()
		c.execute("UPDATE session SET handshake_complete=1 where telephone='%s' and terminated = 0" % self.recipient_telephone)
		self.conn.commit()
	
	def getIV(self):
		c = self.conn.cursor()
		iv = c.execute("SELECT iv FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
		iv = base64.b64decode(iv)
		return iv
	
	@ErrorIgnore([TypeError])
	def sessionID(self):
		c = self.conn.cursor()
		return c.execute("SELECT session_id FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def terminate(self):
		c = self.conn.cursor()
		c.execute("UPDATE session SET terminated=%f where telephone='%s' and terminated = 0" % (time.time(), self.recipient_telephone))
		self.conn.commit()
	
	def addStoredMessage(self, message):
		c = self.conn.cursor()
		c.execute("UPDATE session SET stored_message='%s' where telephone='%s' and terminated = 0" % (message, self.recipient_telephone))
		self.conn.commit()
	
	@ErrorIgnore([TypeError])
	def storedMessage(self):
		c = self.conn.cursor()
		return c.execute("SELECT stored_message from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def addMessage(self, message, sequence_number):
		c = self.conn.cursor()
		number_messages = c.execute("SELECT number_messages FROM session WHERE session_id=%d" % self.sessionID()).fetchone()[0]
		c.execute("INSERT INTO messages(message, session_id, sequence_number) VALUES('%s', %d, %d)" % (message, self.sessionID(), sequence_number))
		self.conn.commit()
		messages = c.execute("SELECT message FROM messages WHERE session_id=%d ORDER BY sequence_number" % self.sessionID()).fetchall()
		if len(messages) == number_messages:
			message_list = []
			for m in messages:
				message_list.append(m[0])
			return message_list
	

def calculateIV(IV, SQ):
	for i in range(0,SQ+1):
		IV = hashlib.sha256(IV).hexdigest()[0:16]
	return IV
	



