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
		c.execute("INSERT INTO election(voter_id, candidate_id) VALUES(%d,%d)" % (voter_id, candidate_id))
		self.conn.commit()
	
	def addVote(self, voter_id, candidate_id, election_id):
		
		c = self.conn.cursor()
		if self.persons.getPersons(person_id=candidate_id, party_types=["CANDIDATE"], election_id=election_id) is None:
			# Candidate does not exist
			return None
		
		c.execute("INSERT INTO vote(voter_id, candidate_id, election_id) VALUES(%d,%d,%d)" % (voter_id, candidate_id, election_id))
		self.conn.commit()
		vote_id = c.lastrowid
		row = c.execute("SELECT * FROM vote WHERE voter_id=%d and candidate_id=%d and election_id=%d" % (voter_id, candidate_id, election_id)).fetchone()
		return {"vote_id":row[0], "voter_id":voter_id, "candidate_id":candidate_id, "election_id":election_id}

class ElectionMgtTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()