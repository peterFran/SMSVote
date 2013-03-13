#!/usr/bin/env python
# encoding: utf-8
"""
SMSClientModel.py

Created by Peter Meckiffe on 2013-03-12.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sqlite3

class SMSMachineModel(object):
	def __init__(self, this_telephone, path):
		self.conn = sqlite3.connect(path)
		self.this_telephone = this_telephone
	
	def getAllClients(self):
		c = self.conn.cursor()
		clients = c.execute("SELECT telephone FROM machine WHERE telephone IS NOT '%s'" % self.this_telephone).fetchall()
		numbers = list()
		for row in clients:
			numbers.append(row[0])
		return numbers
	
	def addMachine(self, telephone, password):
		c = self.conn.cursor()
		c.execute("INSERT INTO machine(telephone, password) VALUES('%s', '%s')" % (telephone, password))
		self.conn.commit()
	
	def addPublicKey(self, telephone, key):
		c = self.conn.cursor()
		c.execute("INSERT INTO public_key(telephone, key) VALUES('%s', '%s')" % (telephone, key))
		self.conn.commit()
	
	def addPrivateKey(self, telephone, key):
		c = self.conn.cursor()
		c.execute("INSERT INTO private_key(telephone, key) VALUES('%s', '%s')" % (telephone, key))
		self.conn.commit()
	
	def getPrivateKey(self, telephone):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM private_key WHERE telephone='%s'" % telephone).fetchone()[0]
	
	def getPublicKey(self, telephone):
		c = self.conn.cursor()
		return c.execute("SELECT key FROM public_key WHERE telephone='%s'" % telephone).fetchone()[0]
	
	def getPassword(self, telephone):
		c = self.conn.cursor()
		return c.execute("SELECT password FROM machine WHERE telephone='%s'" % telephone).fetchone()[0]
	
if __name__ == '__main__':
	sms = SMSMachineModel("+442033229681", "../SMSVoteServer/gateway.db")
	#sms.addMachine("+441252236305", "abcdefgh")
	print sms.getAllClients()
	print sms.getPrivateKey("+442033229681")
	