#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecDecryptHandshake.py

Created by Peter Meckiffe on 2013-02-08.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest


class SMSSecDecryptHandshake(SMSSecMessage):
	def __init__(self, destination_telephone, sender_telephone, private_key):
		super(SMSSecDecryptHandshake, self).__init__(destination_telephone, sender_telephone)
		self.private_key =RSA.importKey(private_key)
	def decrypt(self, encrypted_message, machine_pass):
		message = self.private_key.decrypt(encrypted_message[0])
		print len(message)
		telephone, parts = message.split(":",1)
		session_id = parts[64:72]
		message_hash = parts[:32]
		hash_digest = hashlib.sha256(self.sender_telephone+machine_pass+session_id).digest()
		if(message_hash!=hash_digest):
			raise InputError("Hashes don't match")
		super(SMSSecHandshakeResponseMessage, self).generatePass(parts[32:64], machine_pass)


class SMSSecDecryptHandshakeTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()