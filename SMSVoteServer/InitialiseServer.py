#!/usr/bin/env python
# encoding: utf-8
"""
InitialiseClient.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import sqlite3
from SMSVoteState.SMSMachineModel import *
from Crypto.PublicKey import RSA


def main():
	import os
	server_key = RSA.importKey(open("serverKey.txt","r").read())
	client_public_key = open("clientPub.txt","r").read()
	
	# Reset database
	con = sqlite3.connect('./gateway.db')
	f = open('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway/SMSVoteState/DatabaseSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(sql)
	con.commit()
	
	# Create Machine Model
	server_model = SMSMachineModel("+442033229681",con)
	client_model = SMSMachineModel("+441252236305", con)
	
	# Load server details
	server_model.initMachine("hgfedcba")
	server_model.addPublicKey(server_key.publickey().exportKey())
	server_model.addPrivateKey(server_key.exportKey())
	
	# Load client details
	client_model.initMachine("abcdefgh")
	client_model.addPublicKey(client_public_key)
	


if __name__ == '__main__':
	main()

