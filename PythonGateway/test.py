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


class test:
	def __init__(self):
		pass


class testTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	test = "?0"
	IV = Random.new().read(16)
	key = Random.new().read(16)
	aes = AESCipher(key)
	enc = aes.encrypt(test,IV)