#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecMessage.py

Created by Peter Meckiffe on 2013-02-03.
Copyright (c) 2013 UWE. All rights reserved.
"""

from SMSMessage import SMSMessage

class SMSSecMessage(SMSMessage):
	def __init__(self, recipient_telephone, sender_telephone):
		super(SMSSecMessage, self).__init__(recipient_telephone, sender_telephone)
	
	def createMessage(self):
		pass
	
	def decryptMessage(self):
		pass
	
