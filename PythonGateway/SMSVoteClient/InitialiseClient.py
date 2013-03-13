#!/usr/bin/env python
# encoding: utf-8
"""
InitialiseServer.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import sqlite3
from Crypto.PublicKey import RSA

def main():
	clientkey = RSA.importKey(open("clientKey.txt","r").read())
	serverPub = open("serverPub.txt","r").read()
	
	# Reset database
	con = sqlite3.connect('./client.db')
	f = open('../SMSVoteState/DatabaseSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(str)
	con.commit()
	
	# Create Machine Model
	machine_model = SMSMachineModel("+442033229681", "./client.db")
	
	# Load server details
	machine_model.addMachine("+441252236305", "abcdefgh")
	machine_model.addPublicKey("+441252236305", clientKey.publickey().exportKey())
	machine_model.addPrivateKey("+441252236305", clientKey.exportKey())
	
	# Load client details
	machine_model.addMachine("+442033229681", "hgfedcba")
	machine_model.addPublicKey("+442033229681", serverPub)


if __name__ == '__main__':
	main()

