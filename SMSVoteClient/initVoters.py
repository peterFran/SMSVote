#!/usr/bin/env python
# encoding: utf-8
"""
initVoters.py

Created by Peter Meckiffe on 2013-03-30.
Copyright (c) 2013 UWE. All rights reserved.
"""
import sys
import sqlite3
import os
import json
def main():
	# Reset database
	con = sqlite3.connect('./app/static/data/voters.db')
	f = open('../PythonGateway/VoterMgt/VoterSchema.sql','r')
	sql = f.read()
	f.close()
	con.cursor().executescript(sql)
	con.commit()
	filename = 'app/static/data/voters.txt'
	with open(filename, 'r') as f:
			voters = json.loads(f.read())
		
			for voter in voters:
				print voter["voter_id"]
				con.cursor().execute("INSERT INTO voter(voter_id, first_name, last_name) VALUES(%d,'%s','%s')" 
					% (int(voter["voter_id"]),voter['first_name'],voter['last_name']))
	con.commit()


if __name__ == '__main__':
	main()