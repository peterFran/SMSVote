#!/usr/bin/env python
# encoding: utf-8
"""
VoterMgt.py

Created by Peter Meckiffe on 2013-03-29.
Copyright (c) 2013 UWE. All rights reserved.
"""

from ErrorIgnore import ErrorIgnore

class VoterMgt(object):
	def __init__(self, conn):
		self.conn = conn

	def close(self):
		self.conn.close()
	
	def addCandidate(self, first_name, last_name):
		c = self.conn.cursor()
		c.execute("INSERT INTO voter(first_name, last_name) VALUES('%s','%s')" % (first_name, last_name))
		self.conn.commit()
		return {"voter_id":c.lastrowid,"first_name":first_name,"last_name":last_name}
	
	@ErrorIgnore([TypeError])
	def getVoter(self, voter_id):
		c = self.conn.cursor()
		row = c.execute("SELECT * FROM voter WHERE voter_id = %d" % voter_id).fetchone()
		return {"voter_id":row[0],"first_name":row[1],"last_name":row[2]}
	