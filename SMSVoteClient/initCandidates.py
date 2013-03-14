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


def main():
	# Reset database
	con = sqlite3.connect('./app/static/data/candidates.db')
	f = open('../PythonGateway/CandidateManagement/CandidateSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(sql)
	con.commit()


if __name__ == '__main__':
	main()

