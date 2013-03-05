#!/usr/bin/env python
# encoding: utf-8
"""
TwilioMessageDispatcher.py

Created by Peter Meckiffe on 2013-02-05.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
from twilio.rest import TwilioRestClient
from datetime import datetime


class TwilioMessageManager:
	def __init__(self, account_sid, auth_token):
		self.client = TwilioRestClient(account_sid, auth_token)
	def getMessagesRecievedInLastXMinutes(self,x):
		#message = client.sms.messages.create(to="+447872124086", from_="+442033229681", body="Hello there!")
		time =  datetime.now()
		time = time.replace(minute=time.minute-5)
		print str(time)
		messages = self.client.sms.messages.list(to="+442033229681",date_sent=(">"+str(time)))
		#for m in client.sms.messages.list(from="+447872124086"):
		for m in messages:
			print m.body
			print m.from_
	def sendMessage(message):
		# Download the Python helper library from twilio.com/docs/libraries
		from twilio.rest import TwilioRestClient

		# Your Account Sid and Auth Token from twilio.com/user/account
		account_sid = "My sid"
		auth_token  = "My auth"
		client = TwilioRestClient(account_sid, auth_token)

		twi_message = client.sms.messages.create(body=message.message,
		    to=message.to_field,
		    from_=message.from_field)
		print twi_message.sid


class TwilioTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	m = TwilioMessageManager("AC58b8ab2ad7e7141d938446113f56ccda","665924eabbf1d698908258c83999c670")
	m.getMessagesRecievedInLastXMinutes(1)