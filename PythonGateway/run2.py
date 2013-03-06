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
	xml = "Hello my name is Pete"
	servkey = RSA.importKey(open("serverKey.txt","r").read())
	servPub = open("serverPub.txt","r").read()
	clientkey = RSA.importKey(open("clientKey.txt","r").read())
	clientPub = open("clientPub.txt","r").read()
	obj = SMSVoteMachine("+442033229681",servkey, "gfedcba", [{"telephone":"+447872124086","password":"abcdefg","PK":clientPub}])
	obj2 = SMSVoteMachine("+447872124086",clientkey, "abcdefg", [{"telephone":"+442033229681","password":"gfedcba","PK":servPub}])
	
	message = obj.sendMessage("+447872124086", xml)
	#print message
	
	message2 = obj2.receiveMessage(message['message'].sender_telephone, message['message'].message)
	#print message2['message'].message
	message3 = obj.receiveMessage(message2['message'].sender_telephone, message2['message'].message)
	#print message3
	high = 0
	for i in message3["messages"]:
		if len(i['message'].message)>high:
			high = len(i['message'].message)
		message4 = obj2.receiveMessage(i['message'].sender_telephone, i['message'].message)
	print message4['message']
	print high
	