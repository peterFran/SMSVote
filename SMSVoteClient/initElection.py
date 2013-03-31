#!/usr/bin/env python
# encoding: utf-8
"""
initCandidates.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sqlite3
from ElectionMgt.PersonMgt import *
from ElectionMgt.ElectionMgt import *
import json
def main():
	# Reset database
	con = sqlite3.connect('./app/static/data/candidates.db')
	f = open('../PythonGateway/CandidateManagement/CandidateSchema.sql','r')
	sql = f.read()
	f.close()
	con.cursor().executescript(sql)
	con.commit()
	filename = 'app/static/data/candidates.txt'
	with open(filename, 'r') as f:
		candidates = json.loads(f.read())
		person_mgt = PersonMgt(con)
		for candidate in candidates:
			person_mgt.addPerson(candidate['first_name'], candidate['last_name'], party_types=["CANDIDATE","VOTER"], election_id=1, party=candidate['party'])
			con.cursor().execute("INSERT INTO candidate(candidate_number, first_name, last_name, party) VALUES(%d,'%s','%s','%s')" 
				% (int(candidate["person_id"]),candidate['first_name'],candidate['last_name'],candidate['party']))


if __name__ == '__main__':
	main()