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
	random_generator = Random.new().read
	key2 = RSA.generate(1024, random_generator)
	obj = SMSVoteMachine("+442033229681",key, "gfedcba", [{"telephone":"+447872124086","password":"abcdefg","PK":key2.publickey().exportKey()}])
	obj2 = SMSVoteMachine("+447872124086",key2, "abcdefg", [{"telephone":"+442033229681","password":"gfedcba","PK":key.publickey().exportKey()}])
	note = "ab"*95+"END"
	
	message = obj.sendMessage("+447872124086", note)
	#print message
	message2 = obj2.receiveMessage(message['message'].sender_telephone, message['message'].message)
	#print message2['message'].message
	message3 = obj.receiveMessage(message2['message'].sender_telephone, message2['message'].message)
	#print message3
	for i in message3["messages"]:
		message4 = obj2.receiveMessage(i['message'].sender_telephone, i['message'].message)
		print message4
	