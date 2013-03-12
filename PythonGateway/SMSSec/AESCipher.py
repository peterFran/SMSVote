#!/usr/bin/env python
# encoding: utf-8
"""
AESCipher.py

Created by Peter Meckiffe on 2013-03-12.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import base64
from Crypto.Cipher import AES

class AESCipher(object):
	def __init__( self, key ):
		self.key = key 
		BS = 16
		self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
		self.unpad = lambda s : s[0:-ord(s[-1])]
	
	def encrypt( self, raw ,iv):
		raw = self.pad(raw)
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		bs = base64.b64encode( iv + cipher.encrypt( raw ) )
		bs = bs.encode("utf-8")
		return bs
	
	def decrypt( self, enc, iv):
		enc = enc.decode("utf-8")
		enc = base64.b64decode(enc)
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		return self.unpad(cipher.decrypt( enc[16:] ))