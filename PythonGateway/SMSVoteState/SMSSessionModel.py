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
	
	def initParameters(self, iv, key, random_challenge):
		iv = base64.b64encode(iv)
		random_challenge = base64.b64encode(random_challenge)
		c = self.conn.cursor()
		c.execute("SELECT * FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()
		if c is None:
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge, timestarted) values('%s', '%s', '%s', '%s', %f)" % (self.recipient_telephone, iv, key, random_challenge, time.time()))
		else:
			c.execute("UPDATE session SET terminated='%s' where telephone='%s' and terminated = 0" % (time.time(), self.recipient_telephone))
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge, timestarted) values('%s', '%s', '%s', '%s', %f)" % (self.recipient_telephone, iv, key, random_challenge, time.time()))
		self.conn.commit()
		return c.execute("SELECT session_id FROM session WHERE telephone='%s' AND terminated=0" % self.recipient_telephone).fetchone()[0]
	
	def key(self):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def randomChallenge(self):
		c = self.conn.cursor()
		return base64.b64decode(c.execute("SELECT random_challenge FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0])
	
	def sendIV(self):
		c = self.conn.cursor()
		(iv, send_sequence) = c.execute("SELECT iv, send_sequence FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()
		iv = base64.b64decode(iv)
		return getIV(iv, send_sequence)
	
	def receiveIV(self):
		c = self.conn.cursor()
		(iv, receive_sequence) = c.execute("SELECT iv, receive_sequence FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()
		iv = base64.b64decode(iv)
		return getIV(iv, receive_sequence)
	
	@ErrorIgnore([TypeError])
	def sessionID(self):
		c = self.conn.cursor()
		return c.execute("SELECT session_id FROM session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	def incrementSendSequence(self):
		c = self.conn.cursor()
		sq = c.execute("SELECT send_sequence from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
		sq = int(sq)+1
		c.execute("UPDATE session SET send_sequence=%d, last_send_at=%f where telephone='%s' and terminated = 0" % (sq, time.time(), self.recipient_telephone))
		self.conn.commit()
	
	def incrementReceiveSequence(self):
		c = self.conn.cursor()
		sq = c.execute("SELECT receive_sequence from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
		sq = int(sq)+1
		c.execute("UPDATE session SET receive_sequence=%d, last_receive_at=%f where telephone='%s' and terminated = 0" % (sq, time.time(), self.recipient_telephone))
		self.conn.commit()
	
	@ErrorIgnore([TypeError])
	def sendSequence(self):
		c = self.conn.cursor()
		return c.execute("SELECT send_sequence from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
	@ErrorIgnore([TypeError])
	def receiveSequence(self):
		c = self.conn.cursor()
		return c.execute("SELECT receive_sequence from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	
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
	
	def addReceivedMessagePart(self, message):
		c = self.conn.cursor()
		mes = c.execute("SELECT received_message from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
		if mes is not None:
			message = mes + message
		c.execute("UPDATE session SET received_message='%s' where telephone='%s' and terminated = 0" % (message, self.recipient_telephone))
		self.conn.commit()
	
	@ErrorIgnore([TypeError])
	def receivedMessage(self):
		c = self.conn.cursor()
		return c.execute("SELECT received_message from session where telephone='%s' and terminated = 0" % self.recipient_telephone).fetchone()[0]
	

def getIV(IV, SQ):
	for i in range(0,SQ):
		IV = hashlib.sha256(IV).hexdigest()[0:16]
	return IV
	



