#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecMachineDetails.py

Created by Peter Meckiffe on 2013-02-08.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest


class SMSSecMachineDetails:
	def __init__(self, telephone_number, machine_pass):
		self.telephone_number = telephone_number
		self.machine_pass = machine_pass
	
	def generatePass(self, seed):
		x = hashlib.sha256(str(0)+self.machine_pass+seed)
		for i in range(0,29,1):
			x = hashlib.sha256(x.digest()+self.machine_pass+seed)
		return secret_key = x.digest()
	
	def generateHash(self, session_id):
		return hashlib.sha256(self.sender_telephone+self.machine_pass+"{0:08d}".format(session_id)).digest()
	
class SMSSecMachineDetails(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()