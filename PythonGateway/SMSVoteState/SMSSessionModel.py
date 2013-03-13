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

class SMSSessionModel:
	def __init__(self, recipient_telephone, path):
		self.recipient_telephone = recipient_telephone
		self.conn = sqlite3.connect(path)
	
	def initParameters(self, iv, key, random_challenge):
		c = self.conn.cursor()
		c.execute("SELECT * FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()
		if c is None:
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge) values(%s, %s, %s, %s)" % (self.recipient_telephone, iv, key, random_challenge))
		else:
			c.execute("UPDATE session SET terminated=%s where telephone=%s and terminated = NULL" % (time.time(), self.recipient_telephone))
			c.execute("INSERT INTO session(telephone, iv, key, random_challenge) values(%s, %s, %s, %s)" % (telephone, iv, key, random_challenge))
		self.conn.commit()
		return c.execute("SELECT session_id FROM session WHERE telephone=%s AND terminated=NULL" % self.recipient_telephone).fetchone()[0]
	
	def key(self):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()[0]
	
	def randomChallenge(self):
		c = self.conn.cursor()
		return c.execute("SELECT random_challenge FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()[0]
	
	def sendIV(self):
		c = self.conn.cursor()
		(iv, send_sequence) = c.execute("SELECT iv, send_sequence FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()
		return getIV(iv, send_sequence)
	
	def receiveIV(self):
		c = self.conn.cursor()
		(iv, receive_sequence) = c.execute("SELECT iv, receive_sequence FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()
		return getIV(iv, receive_sequence)
	
	def sessionID(self):
		c = self.conn.cursor()
		return c.execute("SELECT session_id FROM session where telephone=%s and terminated = NULL" % telephone).fetchone()[0]
	
	def incrementSendSequence(self):
		c = self.conn.cursor()
		sq = c.execute("SELECT send_sequence from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
		sq = int(sq)+1
		c.execute("UPDATE session SET send_sequence=%d, last_send_at=%f where telephone=%s and terminated = NULL" % (sq, time.time(), self.recipient_telephone))
		self.conn.commit()
	
	def incrementReceiveSequence(self):
		c = self.conn.cursor()
		sq = c.execute("SELECT receive_sequence from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
		sq = int(sq)+1
		c.execute("UPDATE session SET receive_sequence=%d, last_receive_at=%f where telephone=%s and terminated = NULL" % (sq, time.time(), self.recipient_telephone))
		self.conn.commit()
	
	def sendSequence(self):
		c = self.conn.cursor()
		return c.execute("SELECT send_sequence from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
	
	def receiveSequence(self):
		c = self.conn.cursor()
		return c.execute("SELECT receive_sequence from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
	
	def terminate(self):
		c = self.conn.cursor()
		c.execute("UPDATE session SET terminated=%f where telephone=%s and terminated = NULL" % (time.time(), self.recipient_telephone))
		self.conn.commit()
	
	def addStoredMessage(self, message):
		c = self.conn.cursor()
		c.execute("UPDATE session SET stored_message=%s where telephone=%s and terminated = NULL" % (message, self.recipient_telephone))
		self.conn.commit()
	
	def storedMessage(self):
		c = self.conn.cursor()
		return c.execute("SELECT stored_message from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
	
	def addReceivedMessagePart(self, message):
		c = self.conn.cursor()
		mes = c.execute("SELECT received_message from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
		mes = mes + message
		c.execute("UPDATE session SET received_message=%s where telephone=%s and terminated = NULL" % (mes, self.recipient_telephone))
		self.conn.commit()
	
	def receivedMessage(self):
		c = self.conn.cursor()
		return c.execute("SELECT received_message from session where telephone=%s and terminated = NULL" % self.recipient_telephone).fetchone()[0]
	

def getIV(IV, SQ):
	for i in range(0,SQ):
		IV = hashlib.sha256(IV).hexdigest()[0:16]
	return IV
	



