#!/usr/bin/env python
# encoding: utf-8
"""
SMSSecClient.py

Created by Peter Meckiffe on 2013-02-04.
Copyright (c) 2013 UWE. All rights reserved.
"""

from SMSSec import *
from Crypto import Random
from Crypto.PublicKey import RSA

if __name__ == '__main__':
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	details = SMSSec.SMSSecMachineDetails("+447872124086","abcd1234")
	smsClient = SMSSecEncrypt.SMSSecHandshakeFirstMessage("+442033229681",details)
	
	smsClient.createMessage(key.publickey().exportKey(), 1)
	decryptor = SMSSecDecrypt.SMSSecDecryptFirstHandshakeMessage("+442033229681",details,key.exportKey())
	
	aes_key, session_id, random_challenge = decryptor.decrypt(smsClient.message)
	if (random_challenge!= smsClient.random_challenge):
	responseBuilder = SMSSecEncrypt.SMSSecHandshakeResponseMessage("442033229681", details)
	responseBuilder.createMessage(random_challenge, session_id)
	
	
	
