#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecClient.py

Created by Peter Meckiffe on 2013-02-04.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from SMSSecMessage import SMSSecMessage
from SMSSecHandshakeFirstMessage import SMSSecHandshakeFirstMessage
from SMSSecHandshakeResponseMessage import SMSSecHandshakeResponseMessage
from Crypto.PublicKey import RSA
from Crypto import Random

if __name__ == '__main__':
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	smsClient = SMSSecHandshakeFirstMessage("+44898989898","+4489791469")
	smsClient.createMessage("1234abcd", key.publickey().exportKey(), 1)
	smsServer = SMSSecHandshakeResponseMessage("+4489791469","+44898989898")
	smsServer.createMessage(smsClient.message,"1234abcd",key.exportKey())
