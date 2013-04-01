#!/usr/bin/env python
# encoding: utf-8
"""
PartyMgt.py

Created by Peter Meckiffe on 2013-03-29.
Copyright (c) 2013 UWE. All rights reserved.
"""

from ErrorIgnore import ErrorIgnore

class PersonMgt(object):
	def __init__(self, conn):
		self.conn = conn

	def close(self):
		self.conn.close()
	
	def addPerson(self, first_name, last_name, check=True):
		c = self.conn.cursor()
		if check:
			if self.getPersonWithNames(first_name, last_name) is None:
				c.execute("INSERT INTO person(first_name, last_name) VALUES('%s','%s')" % (first_name, last_name))
				self.conn.commit()
				return c.lastrowid
			else:
				raise Exception()
		else:
			person = self.getPersonWithNames(first_name, last_name)
			if person is None:
				c.execute("INSERT INTO person(first_name, last_name) VALUES('%s','%s')" % (first_name, last_name))
				self.conn.commit()
				return c.lastrowid
			else:
				return person["person_id"]
	
	def makeVoter(self, person_id, election_id, voter_id=None):
		c = self.conn.cursor()
		if voter_id is None:
			c.execute("INSERT INTO voter(person_id, election_id) VALUES(%d,%d)" % (person_id, election_id))
		else:
			c.execute("INSERT INTO voter(person_id, election_id, voter_id) VALUES(%d,%d,%d)" % (person_id, election_id, voter_id))
		self.conn.commit()
		return c.lastrowid
	
	def makeCandidate(self, person_id, election_id, party, candidate_id = None):
		c = self.conn.cursor()
		if candidate_id is None:
			if party is None:
				c.execute("INSERT INTO candidate(person_id, election_id) VALUES(%d,%d)" % (person_id, election_id))
			else:
				c.execute("INSERT INTO candidate(person_id, election_id, party) VALUES(%d,%d,'%s')" % (person_id, election_id, party))
		else:
			if party is None:
				c.execute("INSERT INTO candidate(person_id, election_id, candidate_id) VALUES(%d,%d,%d)" % (person_id, election_id,candidate_id))
			else:
				c.execute("INSERT INTO candidate(person_id, election_id, party, candidate_id) VALUES(%d, %d, '%s', %d)" % (person_id, election_id, party, candidate_id))
		self.conn.commit()
		return c.lastrowid
	
	@ErrorIgnore([TypeError])
	def getPerson(self, person_id):
		c = self.conn.cursor()
		row = c.execute("SELECT * FROM person WHERE person_id = %d" % (person_id)).fetchone()
		return {"person_id":person_id,"first_name":row[1],"last_name":row[2]}
	
	@ErrorIgnore([TypeError])
	def getPersonWithNames(self, first_name, last_name):
		c = self.conn.cursor()
		row = c.execute("SELECT person_id FROM person WHERE first_name = '%s' and last_name = '%s'" % (first_name, last_name)).fetchone()
		return {"person_id":row[0],"first_name":first_name,"last_name":last_name}
	
	@ErrorIgnore([TypeError])
	def getCandidate(self, candidate_id, election_id):
		c = self.conn.cursor()
		row = c.execute("SELECT person_id, party FROM candidate WHERE candidate_id = %d and election_id=%d" % (candidate_id, election_id)).fetchone()
		person_id = row[0]
		details = self.getPerson(person_id)
		details["party"] = row[1]
		details["candidate_id"] = candidate_id
		details["election_id"] = election_id
		return details
	
	def getCandidates(self, election_id):
		c = self.conn.cursor()
		rows = c.execute("SELECT candidate_id FROM candidate WHERE election_id=%d" % (election_id)).fetchall()
		candidates = []
		for row in rows:
			candidates.append(self.getCandidate(row[0],election_id))
		return candidates
	
	def clearCandidates(self, election_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM candidate WHERE election_id = %d" % election_id)
		self.conn.commit()
	
	def clearCandidate(self, candidate_id, election_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM candidate WHERE candidate_id = %d and election_id = %d" % (candidate_id, election_id))
		self.conn.commit()
		
	def getVoters(self, election_id):
		c = self.conn.cursor()
		rows = c.execute("SELECT voter_id FROM voter WHERE election_id=%d" % (election_id)).fetchall()
		voters = []
		for row in rows:
			voters.append(self.getVoter(row[0],election_id))
		return candidates
	
	def vote(self, voter_id, election_id):
		c = self.conn.cursor()
		c.execute("UPDATE voter SET voted=1 where voter_id=%d and election_id=%d" % (voter_id,election_id))
		self.conn.commit()
	
	@ErrorIgnore([TypeError])
	def getVoter(self, voter_id, election_id, voted=0):
		c = self.conn.cursor()
		row = c.execute("SELECT person_id, voted FROM voter WHERE voter_id = %d and election_id=%d and voted=%d" % (voter_id, election_id, voted)).fetchone()
		person_id = row[0]
		details = self.getPerson(person_id)
		details["voted"] = row[1]
		details["voter_id"] = voter_id
		details["election_id"] = election_id
		return details
	

