#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecHandshakeResponseMessage.py

Created by Peter Meckiffe on 2013-02-05.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import hashlib
from Crypto import Random
from Crypto.PublicKey import RSA
from SMSSecMessage import SMSSecMessage


class SMSSecHandshakeResponseMessage(SMSSecMessage):
	def __init__(self, destination_telephone, sender_telephone):
		super(SMSSecHandshakeResponseMessage, self).__init__(destination_telephone, sender_telephone)
		pass
	def createMessage(self):
		hash_digest = hashlib.sha256(self.destination_telephone+machine_pass+session_id).digest()
		if(message_hash!=hash_digest):
			raise InputError("Hashes don't match")
		super(SMSSecHandshakeResponseMessage, self).generatePass(parts[32:64], machine_pass)



class SMSSecHandshakeResponseMessageTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()