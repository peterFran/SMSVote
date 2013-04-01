#!/usr/bin/env python
# encoding: utf-8
"""
SMSClientModel.py

Created by Peter Meckiffe on 2013-03-12.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sqlite3
from ErrorIgnore import ErrorIgnore

class SMSMachineModel(object):
	def __init__(self, this_telephone, conn):
		self.conn = conn
		self.this_telephone = this_telephone
	
	def close(self):
		self.conn.close()
	
	def getAllClients(self):
		c = self.conn.cursor()
		clients = c.execute("SELECT telephone FROM machine WHERE telephone IS NOT '%s'" % self.this_telephone).fetchall()
		numbers = list()
		for row in clients:
			numbers.append(row[0])
		return numbers
	
	@ErrorIgnore([TypeError])
	def getInitiatorPart(self):
		c = self.conn.cursor()
		return c.execute("SELECT part_init FROM machine WHERE telephone='%s'" % self.this_telephone).fetchone()[0]
	
	def addInitiatorPart(self, part):
		c = self.conn.cursor()
		c.execute("UPDATE machine SET part_init='%s' WHERE telephone='%s'" % (part, self.this_telephone))
		self.conn.commit()
	
	def wipeInitiatorPart(self):
		c = self.conn.cursor()
		c.execute("UPDATE machine SET part_init=NULL WHERE telephone='%s'" % (self.this_telephone))
		self.conn.commit()
	
	def initMachine(self, password):
		c = self.conn.cursor()
		c.execute("INSERT INTO machine(telephone, password) VALUES('%s', '%s')" % (self.this_telephone, password))
		self.conn.commit()
	
	def addPublicKey(self, key):
		c = self.conn.cursor()
		c.execute("INSERT INTO public_key(telephone, key) VALUES('%s', '%s')" % (self.this_telephone, key))
		self.conn.commit()
	
	def addPrivateKey(self, key):
		c = self.conn.cursor()
		c.execute("INSERT INTO private_key(telephone, key) VALUES('%s', '%s')" % (self.this_telephone, key))
		self.conn.commit()
	
	def getPrivateKey(self):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM private_key WHERE telephone='%s'" % self.this_telephone).fetchone()[0]
	
	def getPublicKey(self):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM public_key WHERE telephone='%s'" % self.this_telephone).fetchone()[0]
	
	def getPassword(self):
		c = self.conn.cursor()
		return c.execute("SELECT password FROM machine WHERE telephone='%s'" % self.this_telephone).fetchone()[0]
	
if __name__ == '__main__':
	sms = SMSMachineModel("+442033229681", "../SMSVoteServer/gateway.db")
	#sms.addMachine("+441252236305", "abcdefgh")
	print sms.getAllClients()
	print sms.getPrivateKey()
	