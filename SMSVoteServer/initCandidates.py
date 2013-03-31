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
import 
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
		try:
			candidates = json.loads(f.read())
		
			for candidate in candidates:
				con.cursor().execute("INSERT INTO candidate(candidate_number, first_name, last_name, party) VALUES(%d,'%s','%s','%s')" 
					% (int(candidate["id"]),candidate['first_name'],candidate['last_name'],candidate['party']))
		except:
			print "no candidates"
	con.commit()


if __name__ == '__main__':
	main()

