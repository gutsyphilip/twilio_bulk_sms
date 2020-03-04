import os
from twilio.rest import Client

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(to, body):
    message = client.messages.create(
        body=body,
        from_=TWILIO_NUMBER,
        to=to
    )
    return message.sid
