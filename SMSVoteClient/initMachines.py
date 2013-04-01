#!/usr/bin/env python
# encoding: utf-8
"""
initMachines.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import sqlite3
from SMSVoteState.SMSMachineModel import *
from Crypto.PublicKey import RSA


def main():
	# Get keys
	this_key = RSA.importKey(open("app/static/keys/clientKey.txt","r").read())
	server_public_key = open("app/static/keys/serverPub.txt","r").read()
	
	# Reset database
	con = sqlite3.connect('app/static/data/machines.db')
	f = open('../PythonGateway/SMSVoteState/DatabaseSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(sql)
	con.commit()
	
	# Create Machine Model
	this_model = SMSMachineModel("+441252236305",con)
	server_model = SMSMachineModel("+442033229681",con)
	
	# Load this details
	this_model.initMachine("abcdefgh")
	this_model.addPublicKey(this_key.publickey().exportKey())
	this_model.addPrivateKey(this_key.exportKey())
	
	# Load client details
	server_model.initMachine("hgfedcba")
	server_model.addPublicKey(server_public_key)
	


if __name__ == '__main__':
	main()

