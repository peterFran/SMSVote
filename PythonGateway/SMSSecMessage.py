#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecMessage.py

Created by Peter Meckiffe on 2013-02-03.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from SMSMessage import SMSMessage
from Crypto import Random
from Crypto.Cipher import AES

class SMSSecMessage(SMSMessage):
	def __init__(self, destination_telephone, sender_telephone, machine_details):
		super(SMSSecMessage, self).__init__(destination_telephone, sender_telephone)
		self.machine_details = machine_details
	def createMessage(self, sequence_number, message, secret_key):
		pass


class SMSSecMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	sms = SMSSecMessage(12345678,"+442033229681")
	m=sms.createMessage1()
	sms.getMessage1(m)