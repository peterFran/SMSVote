#!/usr/bin/env python
# encoding: utf-8
"""
ElectionMgt.py

Created by Peter Meckiffe on 2013-03-29.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
from PersonMgt import PersonMgt


class ElectionMgt:
	def __init__(self, conn):
		self.conn = conn
		self.persons = PersonMgt(conn)
	
	def close(self):
		self.conn.close()
	
	def createElection(self, name, start_time, end_time):
		c = self.conn.cursor()
		c.execute("INSERT INTO election(election_name, start_time, end_time) VALUES(%d,%d)" % (name, start_time, end_time))
		self.conn.commit()
		return c.lastrowid
	
	def addVote(self, candidate_id, election_id):
		
		c = self.conn.cursor()
		if self.persons.getPersons(person_id=candidate_id, party_types=["CANDIDATE"], election_id=election_id) is None:
			# Candidate does not exist
			return None
		
		c.execute("INSERT INTO vote(candidate_id, election_id) VALUES(%d,%d)" % (candidate_id, election_id))
		self.conn.commit()
		vote_id = c.lastrowid
		return {"vote_id":vote_id, "candidate_id":candidate_id, "election_id":election_id}
	

class ElectionMgtTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()