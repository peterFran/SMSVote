#!/usr/bin/env python
# encoding: utf-8
"""
TwilioMessageDispatcher.py

Created by Peter Meckiffe on 2013-02-05.
Copyright (c) 2013 UWE. All rights reserved.
"""

from twilio.rest import TwilioRestClient

class TwilioMessageManager:
	def __init__(self):
		self.client = TwilioRestClient("AC58b8ab2ad7e7141d938446113f56ccda", "665924eabbf1d698908258c83999c670")
	
	def sendMessage(self, message):
		for mes in message.getMessage():
			twi_message = self.client.sms.messages.create(body=mes,
				to=message.recipient_telephone,
				from_=message.sender_telephone)
			print twi_message.sid
	