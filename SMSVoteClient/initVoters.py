#!/usr/bin/env python
# encoding: utf-8
"""
initVoters.py

Created by Peter Meckiffe on 2013-03-30.
Copyright (c) 2013 UWE. All rights reserved.
"""
import sys
import sqlite3
from ElectionMgt.PersonMgt import *
from ElectionMgt.ElectionMgt import *
from datetime import *
import os
import json
def main():
	# Reset database
	con = sqlite3.connect('./app/static/data/election.db')
	f = open('../PythonGateway/ElectionMgt/ElectionSchema.sql','r')
	sql = f.read()
	f.close()
	con.cursor().executescript(sql)
	con.commit()
	election_mgt = ElectionMgt(con)
	election_id = election_mgt.createElection("President of Nigeria", datetime.now(), datetime.now()+timedelta(days=1), election_id = 1)
	filename = 'app/static/data/voters.txt'
	with open(filename, 'r') as f:
		contents = f.read()
		if len(contents) is not 0:
			
			voters = json.loads(contents)
			person_mgt = PersonMgt(con)
			for voter in voters:
				person_id = person_mgt.addPerson(voter["first_name"], voter["last_name"])
				print person_mgt.makeVoter(person_id,1, voter_id=voter["voter_id"]),"\t%s\t%s" % (voter["first_name"],voter["last_name"])
		print "\n"
	
	filename = 'app/static/data/candidates.txt'
	with open(filename, 'r') as f:
		contents = f.read()
		if len(contents) is not 0:
			candidates = json.loads(contents)
			person_mgt = PersonMgt(con)
			for candidate in candidates:
				person_id = person_mgt.addPerson(candidate["first_name"], candidate["last_name"], check=False)
				print person_mgt.makeCandidate(person_id, election_id, candidate["party"], candidate_id=candidate["candidate_id"]),"\t%s\t%s" % (candidate["first_name"],candidate["last_name"])


if __name__ == '__main__':
	main()