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
from SMSSec.SMSSec import *
import base64


class test:
	def __init__(self):
		pass


class testTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	key = Random.new().read(32)
	iv = Random.new().read(16)
	
	m = "d"*95
	encryptor = AESCipher(key)
	message = encryptor.encrypt(m, iv)
	#print len(message)
	for i in range (1, 100000):
		print 95-len(str(i))
	
