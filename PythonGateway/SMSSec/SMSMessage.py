#!/usr/bin/env python
# encoding: utf-8
"""
SMSMessage.py

Created by Peter Meckiffe on 2013-02-05.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest


class SMSMessage(object):
	def __init__(self, recipient_telephone, sender_telephone):
		self.sender_telephone = sender_telephone
		self.recipient_telephone = recipient_telephone
		self.message = None
	
	def createMessage(self, payload):
		self.message = payload
	
	def getMessage(self):
		# Length must not excede 160 NORMAL CHARACTERS. SPECIAL CHARS WILL CAUSE INIHILATION
		output = []
		message_body = self.message
		while len(message_body)>0:
			size = 160
			if len(message_body)<size:
				output.append(message_body)
				message_body = ""
			else:
				output.append(message_body[:size])
				message_body = message_body[size:]
		return output


class SMSMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()