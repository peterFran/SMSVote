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


class test:
	def __init__(self):
		pass


class testTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	random_generator = Random.new().read
	key2 = RSA.generate(1024, random_generator)
	f = open('clientKey.txt','w')
	f.write(key.exportKey())
	f = open('serverKey.txt','w')
	f.write(key2.exportKey())
	f = open('clientPub.txt','w')
	f.write(key.publickey().exportKey())
	f = open('serverPub.txt','w')
	f.write(key.publickey().exportKey())