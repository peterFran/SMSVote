#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Peter Meckiffe on 2013-02-23.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
from Crypto import Random
from SMSSec.SMSSec import AESCipher
from SMSVoteMachine import *
from Crypto.PublicKey import RSA
import base64


class test:
	def __init__(self):
		pass


class testTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	random = Random.new().read(20)
	
	b64 = base64.b64encode(random)
	
	enc = b64.encode("utf-8")
	b2 = enc.decode('utf-8')
	original = base64.b64decode(b2)
	print random
	print original
	print b64
	print b2
	print enc