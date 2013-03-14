#!/usr/bin/env python
# encoding: utf-8
"""
CandidateModel.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest


class CandidateModel(object):
	def __init__(self, conn):
		self.conn = conn
	
	def close(self):
		self.conn.close()
	
	def getAllCandidates(self):
		c = self.conn.cursor()
		db_out = c.execute("SELECT * FROM candidate").fetchall()
		candidates = list()
		for row in db_out:
			candidates.append({"id":row[0],"first_name":row[1],"last_name":row[2],"party":row[3]})
		return candidates
	
	def addCandidate(self, first_name, last_name, party):
		c = self.conn.cursor()
		c.execute("INSERT INTO candidate(first_name, last_name, party) VALUES('%s','%s','%s')" % (first_name, last_name, party))
		self.conn.commit()

if __name__ == '__main__':
	unittest.main()