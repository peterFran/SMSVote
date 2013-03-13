#!/usr/bin/env python
# encoding: utf-8
"""
PBEKey.py

Created by Peter Meckiffe on 2013-03-12.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from Crypto import Random


class ParameterGenerator(object):
	def __init__(self, machine_pass):
		self.machine_pass = machine_pass
		self.key_params = Random.new().read(32)
		self.random_challenge = Random.new().read(1)
		self.iv = Random.new().read(16)
		self.key = generate16ByteKey(self.machine_pass, self.key_params)
	
def generate16ByteKey(machine_pass, key_params):
	print "PASS: ", machine_pass
	print "KEYPARAMS: ", key_params
	x = hashlib.sha256(str(0)+str(machine_pass)+key_params)
	for i in range(0,29,1):
		x = hashlib.sha256(x.hexdigest()+str(machine_pass)+key_params)
	return x.hexdigest()[0:16]
	