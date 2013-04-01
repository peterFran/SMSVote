#!/usr/bin/env python
# encoding: utf-8
"""
initCandidates.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import sqlite3
import os
import json
from datetime import *
from ElectionMgt.ElectionMgt import *
from ElectionMgt.PersonMgt import *

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
	filename = 'app/static/data/candidates.txt'
	with open(filename, 'r') as f:
		contents = f.read()
		if len(contents) is not 0:
			candidates = json.loads(contents)
			person_mgt = PersonMgt(con)
			for candidate in candidates:
				person_id = person_mgt.addPerson(candidate["first_name"], candidate["last_name"])
				print person_mgt.makeCandidate(person_id, election_id, candidate["party"], candidate_id=candidate["candidate_id"]),"\t%s\t%s\t%s" % (candidate["first_name"],candidate["last_name"],candidate["party"])


if __name__ == '__main__':
	main()

