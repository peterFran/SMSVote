from SMSSec.SMSSec import *
from SMSSec.SMSSecInitiatorMessage import *
from SMSSec.SMSSecResponderMessage import *
from SMSSec.SMSSecSequenceMessage import *
from Crypto.PublicKey import RSA
from Crypto import Random
# Create Key Pair
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
fromField= "+447872124086"

# Create stores
store = SMSSecServerDataStore("+442033229681", key.exportKey(), key.publickey().exportKey())
clientstore = SMSSecClientStore("+447872124086", "abcd1234", "442033229681", key.publickey().exportKey())

# Create detail in server store
store.addDetail("+447872124086","abcd1234")

# Create client initiator
initiator = SMSSecInitiatorMessage(clientstore.server_telephone, clientstore.booth_telephone)
initDetails = initiator.createMessage(clientstore.server_public_key, clientstore.booth_password, 1)
clientstore.startNewSession(initDetails["session_id"], initDetails["iv"],initDetails["key_params"],initDetails["random_challenge"])

# Send message to server

# Decrypt client initiator
# Create responder
# Create session on server
# Send responder to client
servInitiator = SMSSecInitiatorMessage(store.server_telephone, fromField)
servInitDetails = servInitiator.decrypt(initiator.message, store.getBoothPassword(fromField), store.private_key)

responder = SMSSecResponderMessage(store.server_telephone, fromField)
store.startNewSession(fromField,servInitDetails['session_id'], servInitDetails['iv'], servInitDetails['key_params'], servInitDetails['random_challenge'])

details = store.getSessionDetails(fromField)
responder.createMessage(details['random_challenge'], details['send_iv'], details['key'])
store.incrementSendSequence(fromField)

# Decrypt responder 
clientResp = SMSSecResponderMessage(clientstore.server_telephone, clientstore.booth_telephone)
curSesh = clientstore.getCurrentSessionDetails()
message = SMSSecSequenceMessage(clientstore.server_telephone, clientstore.booth_telephone)
if clientResp.decrypt(responder.message, curSesh['random_challenge'], curSesh['receive_iv'], curSesh['key']):
	clientstore.incrementRecieveSequence()
	message = SMSSecSequenceMessage(clientstore.server_telephone, clientstore.booth_telephone)
	details = clientstore.getCurrentSessionDetails()
	# Encrypt first message
	message.createMessage("candidates:{candidate: {name1:'ben' name2:'kingsley' party:'Pirate Party'},candidate: {name1:'ben' name2:'kingsley' party:'Pirate Party'}}", details['send_sequence'], details['send_iv'], details['key'])
	# Inc sequence no to 1 (for next msg)
	clientstore.incrementSendSequence()

# Decrypt first message
details = store.getSessionDetails(fromField)
servMessage = SMSSecSequenceMessage(store.server_telephone, fromField)
print servMessage.decryptMessage(message.message, details['receive_sequence'], details['receive_iv'], details['key'])

servMessage = SMSSecSequenceMessage(fromField, store.server_telephone)
servMessage.createMessage("RightBackAtcha", details['send_sequence'], details['send_iv'], details['key'])
store.incrementSendSequence(fromField)
store.incrementReceiveSequence(fromField)

details = clientstore.getCurrentSessionDetails()
clientMessage = SMSSecSequenceMessage(fromField, store.server_telephone)
print clientMessage.decryptMessage(servMessage.message, details['receive_sequence'], details['receive_iv'], details['key'])

# Inc sequence no to 1
# Create second message
# Inc sequence no to 2 (for next message)

# Decrypt message n
# Inc seq
# Create next message
# Inc seq

