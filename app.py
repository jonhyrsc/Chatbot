
#Python libraries that we need to import for our bot
import os
import sys



# import processing_data
# from processing_data import word_tokenization,extract_stopWord,tag_word, extract_grammar


import requests
from flask import Flask, request

#from pymessenger.bot import Bot

import numpy as np
import random
from tensorflow import keras
#from keras.models import load_model


import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import json
with open('intents.json') as json_data:
    intents = json.load(json_data)


words = []
classes = []
documents = []
ignore_words = ['?']

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))


#model = load_model('modelo_chatbot_1st.h5')
model = keras.models.load_model ("modelo_chatbot_1st.h5")


app = Flask(__name__)

#
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']#"hello"#
#bot = Bot (ACCESS_TOKEN)



if __name__ == "__main__":
    app.run(debug = True, port = 80)



def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET'])
def receive_message_get():
    return request.args['hub.challenge']
#    if request.method == 'GET':
        # token_sent = request.args.get("hub.verify_token")
        # return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
#    else:

@app.route("/", methods = ['POST'])
def receive_message_post():
    output = request.get_json()
    print(output)
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):  # recebemos mensagem de alguem
                #Facebook Messenger ID for user so we know where to send response back to
                sender_id = message['sender']['id']
                recipient_id = message['recipient']['id']

                if message['message'].get('text'):
                    text_received = message['message']['text']
                    #send_message(sender_id, text_received)
                    responseai = response(text_received, sender_id)
                    send_message(sender_id, responseai)
    return "ok"


# def send_message(recipient_id, response):
#     text_tokenized = word_tokenization(response)
#
#     #text_tagged = tag_word(text_tokenized)
#     # text_tagged = extract_grammar(text_tagged)
#     my_string = " ".join(text_tokenized)
#     #test = text_tagged[1]
#     #sends user the text message provided via input response parameter
#     bot.send_text_message(recipient_id, my_string)
#     return "success"


def response(sentence, userID, show_details = False):
    results = classify(sentence)
    print('Result:',results)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return (random.choice(i['responses']))
            results.pop(0)



def send_message(recipient_id, message_text):
    print("sending message to {recipient}: {text}".format(recipient = recipient_id, text = message_text))

    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details = False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


context = {}
ERROR_THRESHOLD = 0.65


def classify(sentence):
    # generate probabilities from the model
    p = bow(sentence, words)

    d = len(p)
    f = len(documents)-2
    a = np.zeros([f, d])
    tot = np.vstack((p,a))

    results = model.predict(tot)[0]

    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list



#clean the sentence
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words
