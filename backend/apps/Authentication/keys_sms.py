from twilio.rest import Client
account_sid='AC0c428a4fb624eaf6d935788814f470df'
auth_token='aeeb105b08138ec7733f50d64cd16054'
twillio_number='+12762779587'
body="""
    Hello,
"""



client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+84837359391", 
    from_="+12762779587",
    body="Chào Thãi nha,")

print(message.sid)
