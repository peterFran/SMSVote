#!/usr/bin/env python
# encoding: utf-8
"""
run2.py

Created by Peter Meckiffe on 2013-03-02.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
from Crypto import Random
from Crypto.PublicKey import RSA
from SMSVoteMachine import *
if __name__ == '__main__':
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	obj = SMSVoteMachine("+442033229681",key, "+447872124086")
	note = "ab"*95+"END"
	for i in obj.divideMessage(note):
		print i
	