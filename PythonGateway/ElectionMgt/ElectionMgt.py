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
	
	def createElection(self, name, start_time, end_time, election_id=None):
		c = self.conn.cursor()
		if election_id is None:
			c.execute("INSERT INTO election(election_name, start_time, end_time) VALUES('?',?,?)", (name, start_time, end_time))
		else:
			c.execute("INSERT INTO election(election_name, start_time, end_time, election_id) VALUES('%s','%s','%s',%d)" % (name, start_time, end_time, election_id))
		self.conn.commit()
		return c.lastrowid
	
	def addVote(self, candidate_id, election_id):
		c = self.conn.cursor()
		candidate = self.persons.getCandidate(candidate_id, election_id)
		if candidate is None:
			# Candidate does not exist
			return None
		
		c.execute("INSERT INTO vote(candidate_id, election_id) VALUES(%d,%d)" % (candidate_id, election_id))
		self.conn.commit()
		vote_id = c.lastrowid
		return {"vote_id":vote_id, "candidate_id":candidate_id, "first_name":candidate["first_name"], "last_name":candidate["last_name"], "party":candidate["party"], "election_id":election_id, }
	
	def getAllVotes(self, election_id):
		c = self.conn.cursor()
		rows = c.execute("SELECT vote_id, candidate_id FROM vote WHERE election_id = %d" % (election_id))
		votes = []
		for vote in rows:
			votes.append({"vote_id":vote[0], "candidate_id":vote[1]})
		return votes
	
	def getCandidateVotes(self, candidate_id, election_id):
		c = self.conn.cursor()
		rows = c.execute("SELECT vote_id FROM vote WHERE candidate_id=%d and election_id = %d" % (candidate_id, election_id))
		votes = []
		for vote in rows:
			votes.append({"vote_id":vote[0], "candidate_id":candidate_id})
		return votes
	
	def countVotes(self, election_id):
		c = self.conn.cursor()
		rows = c.execute("SELECT DISTINCT candidate_id FROM vote WHERE election_id = %d" % (election_id))
		results = []
		total = 0
		winning_candidates = []
		for row in rows:
			votes = self.getCandidateVotes(row[0], election_id)
			total += len(votes)
			candidate_details = self.persons.getCandidate(row[0], election_id)
			candidate_details["votes"] = len(votes)
			results.append(candidate_details)
			if len(winning_candidates) == 0:
				winning_candidates.append(candidate_details)
			elif candidate_details["votes"]> winning_candidates[0]["votes"]:
				winning_candidates = [candidate_details]
			elif candidate_details["votes"] == winning_candidates[0]["votes"]:
				winning_candidates.append(candidate_details)
		return {"total_votes":total, "results":results, "winners":winning_candidates}

class ElectionMgtTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()