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
import xml.etree.ElementTree as ET

def main():
	# Reset database
	con = sqlite3.connect('./app/static/data/candidates.db')
	f = open('app/static/data/candidates.txt')
	string = f.read()
	if len(string) is not 0:
		candidates = ET.fromstring()
		candidateslist = candidates._children
		for cand in candidateslist:
			child = cand._children
			print child[0].text
			print child[1].text
			print child[2].text
			con.cursor().execute("INSERT INTO candidate(candidate_number, first_name, last_name, party) VALUES(%d,'%s','%s','%s')" 
				% (int(cand.attrib["id"]),child[0].text,child[1].text,child[2].text))
		con.commit()


if __name__ == '__main__':
	main()

