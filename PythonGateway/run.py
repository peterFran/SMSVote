# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from datetime import date
# Find these values at https://twilio.com/user/account
account_sid = "AC58b8ab2ad7e7141d938446113f56ccda"
auth_token = "665924eabbf1d698908258c83999c670"
client = TwilioRestClient(account_sid, auth_token)
 
#message = client.sms.messages.create(to="+447872124086", from_="+442033229681", body="Hello there!")
messages = client.sms.messages.list(to="+442033229681")
#for m in client.sms.messages.list(from="+447872124086"):
for m in messages:
	print m.body
	print m.from_