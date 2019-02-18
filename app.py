#Python libraries that we need to import for our bot
import random
import os
import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, request
from pymessenger.bot import Bot
app = Flask(__name__)



ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text_to_send = message['message']['text']
                    #resposta = tokenize_sentence(text)
                    response_sent_text = get_message(text_to_send)
                    response_tokenized = tokenize_sentence(text_to_send)
                    send_message(recipient_id, response_tokenized)


    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(message_text):
    message_text = tokenize_sentence(message_text)
    return message_text
    # return selected item to the user
    #return random.choice(sample_responses)


def tokenize_sentence(text):
    texto_tokenizado = word_tokenize(text.lower)
    return texto_tokenizado


def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
