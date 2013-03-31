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
	
	def addPerson(self, first_name, last_name, party_types=[], election_id=None, party=None, candidate_id=None):
		c = self.conn.cursor()
		c.execute("INSERT INTO person(first_name, last_name) VALUES('%s','%s')" % (first_name, last_name))
		person_id = c.lastrowid
		self.conn.commit()
		if "CANDIDATE" in party_types and election_id is not None and candidate_id is not None:
			self.makeCandidate(person_id, election_id, party, candidate_id)
		if "VOTER" in party_types and election_id is not None:
			self.makeVoter(person_id, election_id)
		return {"person_id":person_id,"first_name":first_name,"last_name":last_name}
	
	def makeVoter(self, person_id, election_id):
		c = self.conn.cursor()
		c.execute("INSERT INTO voter(person_id, election_id) VALUES(%d, %d)" % (person_id, election_id))
		self.conn.commit()
	
	def makeCandidate(self, person_id, election_id, party):
		c = self.conn.cursor()
		if party is None:
			c.execute("INSERT INTO candidate(person_id, election_id, candidate_id, party) VALUES(%d, %d, %s)" % (person_id, election_id, candidate_id, party))
		else:
			c.execute("INSERT INTO candidate(person_id, election_id, candidate_id) VALUES(%d, %d)" % (person_id, election_id, candidate_id))
		self.conn.commit()
	
	@ErrorIgnore([TypeError])
	def getPersons(self, person_id=None, candidate_id=None, party_types=[], election_id=None):
		c = self.conn.cursor()
		if person_id is None and candidate_id is None:
			rows = c.execute("SELECT * FROM person").fetchall()
			returnList = []
			for row in rows:
				if "CANDIDATE" in party_type:
					candidate = checkCandidate(row[0], election_id)
					if candidate is not None:
						returnList.append(candidate)
				elif "VOTER" in party_type:
					voter = checkVoter(row[0], election_id)
					if voter is not None:
						returnList.append(voter)
			
			return returnList
		
		if "VOTER" in party_types and election_id is not None:
			return [self.checkVoter(person_id, election_id)]
		elif "CANDIDATE" in party_types and election_id is not None:
			return [self.checkCandidate(person_id=person_id, candidate_id=candidate_id, election_id)]
		else:
			row = c.execute("SELECT * FROM person WHERE person_id = %d" % (person_id)).fetchone()
			return {"person_id":person_id,"first_name":row[1],"last_name":row[2]}
					
	def checkVoter(self, person_id, election_id):
		if c.execute("SELECT * FROM voter WHERE person_id = %d AND election_id = %d" % (person_id, election_id)) is not None:
			row = c.execute("SELECT * FROM person WHERE person_id = %d" % (person_id)).fetchone()
			return {"person_id":person_id,"first_name":row[1],"last_name":row[2]}
				
	def checkCandidate(self, person_id=None, candidate_id=None, election_id):
		if person_id is not None:
			if c.execute("SELECT * FROM candidate WHERE person_id = %d AND election_id = %d" % (person_id, election_id)) is not None:
				row = c.execute("SELECT * FROM person WHERE person_id = %d" % (person_id)).fetchone()
				return {"person_id":person_id, "candidate_id":row[1], "first_name":row[2],"last_name":row[3]}
		elif candidate_id is not None:
			if c.execute("SELECT * FROM candidate WHERE person_id = %d AND election_id = %d" % (person_id, election_id)) is not None:
				row = c.execute("SELECT * FROM person WHERE person_id = %d" % (person_id)).fetchone()
				return {"person_id":row[0], "candidate_id":candidate_id, "first_name":row[2],"last_name":row[3]}
	
	def getCandidate(self, candidate_id, election_id):
			
	
