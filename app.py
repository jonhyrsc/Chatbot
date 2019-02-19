#Python libraries that we need to import for our bot
import random
import os
from flask import Flask, request
from pymessenger.bot import Bot
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

app = Flask(__name__)


ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

if __name__ == "__main__":
    app.run()

#We will receive messages that Facebook sends our bot at this endpoint
# @app.route("/", methods=['GET', 'POST'])
# def receive_message():
#     if request.method == 'GET':
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     #if the request was not get, it must be POST and we can just proceed with sending a message back to user
#     else:
#         # get whatever message a user sent the bot
#        output = request.get_json()
#        for event in output['entry']:
#           messaging = event['messaging']
#           for message in messaging:
#             if message.get('message'):
#                 #Facebook Messenger ID for user so we know where to send response back to
#                 recipient_id = message['sender']['id']
#                 if message['message'].get('text'):
#                     text_to_send = message['message']['text']
#                     text_tokenized = word_tokenize(text_to_send.lower())
#
#                     for p in text_tokenized:
#                         my_string = "-".join(text_tokenized)
#                     send_message(recipient_id, my_string)
#
#     return "Message Processed"

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message[::-1])

    return "ok"

@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
