1. recieve a message.
2. check if session is active for telephone no. provided
3. if yes: goto 5
4. if no: goto 6

5. check SQ. if 0: Decrypt responder. else: decrypt message with iv & aes key

6. create session (if tel exists) and decrypt initiator.