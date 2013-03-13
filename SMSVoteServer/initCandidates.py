#!/usr/bin/env python
# encoding: utf-8
"""
initCandidates.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os


def main():
	# Reset database
	con = sqlite3.connect('./candidates.db')
	f = open('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/SMSVoteServer/CandidateSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(sql)
	con.commit()


if __name__ == '__main__':
	main()

