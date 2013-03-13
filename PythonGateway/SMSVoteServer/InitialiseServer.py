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
	servkey = RSA.importKey(open("serverKey.txt","r").read())
	clientPub = open("clientPub.txt","r").read()
	
	# Reset database
	con = sqlite3.connect('./gateway.db')
	f = open('../SMSVoteState/DatabaseSchema.sql','r')
	sql = f.read()
	con.cursor().executescript(str)
	con.commit()
	
	# Create Machine Model
	machine_model = SMSMachineModel("+442033229681", "./gateway.db")
	# Load server details
	machine_model.addMachine("+442033229681", "hgfedcba")
	machine_model.addPublicKey("+442033229681", servKey.publickey().exportKey())
	machine_model.addPrivateKey("+442033229681", servKey.exportKey())
	# Load client details
	machine_model.addMachine("+441252236305", "abcdefgh")
	machine_model.addPublicKey("+441252236305", clientPub)
	


if __name__ == '__main__':
	main()

