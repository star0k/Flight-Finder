
from twilio.rest import Client

TWILIO_SID = "AC8895a4de0a6ade1defdcc0e70b3e882f"
TWILIO_AUTH_TOKEN = "dcaefc6ed8955ae3d4474b3acdc3c87b"
TWILIO_VIRTUAL_NUMBER = "+13215783972"
TWILIO_VERIFIED_NUMBER = "+905343936779"


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message , number  = TWILIO_VERIFIED_NUMBER):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=number,
        )
        # Prints if successfully sent.
        print(message.sid)
