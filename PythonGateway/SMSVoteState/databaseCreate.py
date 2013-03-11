#!/usr/bin/env python
# encoding: utf-8
"""
databaseCreate.py

Created by Peter Meckiffe on 2013-03-07.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import sqlite3 as lite

if __name__ == '__main__':
	client = lite.connect(client.db)
	server = lite.connect(server.db)
	with client:
		cur = con.cursor()    
		cur.execute("CREATE TABLE session(INT random_challenge, VARCHAR telephone, INT )")