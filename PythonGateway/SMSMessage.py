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
	
	def createMessage(payload):
		self.message = payload
	


class SMSMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()