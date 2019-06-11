
#Python libraries that we need to import for our bot
import os
import sys
from  get_location import get_loc
import requests
from flask import Flask, request, redirect, url_for
import json
import numpy as np
import random
from tensorflow import keras
import csv
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from select_language_reply import send_select_language

language = 'portuguese'
ERROR_THRESHOLD = 0.5
flag = 0
user_local = ''

with open('dados.json','r') as json_file:
    dados = json.load(json_file)

dicionario = {}
dicionario = dados
stemmer = SnowballStemmer('portuguese')
stop_words = set(stopwords.words('portuguese'))

def change_language(language, sender_id):
    global dicionario
    global stemmer
    global stop_words

    if language == 'portuguese':
        with open('dados.json','r') as json_file:
            dados = json.load(json_file)
        dicionario = {}
        dicionario = dados
        stemmer = SnowballStemmer('portuguese')
        stop_words = set(stopwords.words('portuguese'))
        send_message(sender_id, 'Agora iremos passar a falar em Português!')

    elif language == 'english':
        with open('dados_ingleses.json','r') as json_file:
             dados = json.load(json_file)
        dicionario = {}
        dicionario = dados
        stemmer = SnowballStemmer('english')
        stop_words = set(stopwords.words('english'))
        send_message(sender_id, 'Now, we will start chatting in English!')

    else:
        send_message(sender_id,'Nenhuma linguagem suportada foi escolhida!')



def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)


def bow(sentence, words):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))


def clean_up_sentence(sentence):
    # tokenizar a frase
    sentence_words = nltk.word_tokenize(sentence)
    # stemizar cada palavra, retornar as palavras tokenizadas e stemizadas
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def search_response(results, responses):
    lista_respostas = []
    while results:
        for i in responses:
            if i[1] == results[0]:
                lista_respostas.append(i[0])
        return (random.choice(lista_respostas))


def select_if(results):
    global flag
    if results == 'cantina' or results == 'canteen':
       flag = 1
       return flag
    elif results == 'secretaria' or results == 'secretary':
       flag = 2
       return flag

    elif results == 'serviços sociais' or results == 'social services':
       flag = 3
       return flag

    elif results == 'serviços académicos' or results == 'academic services':
       flag = 4
       return flag

    elif results == 'saudação' or results == 'salutation':
        flag = 5
        return flag

    elif results == 'despedida' or results == 'farewell':
        flag = 6
        return flag

    elif results == 'agradecimento' or results == 'thanks':
        flag = 7
        return flag

    elif results == 'biblioteca' or results == 'library':
        flag = 8
        return flag
    else:
       print('Não encontrei nada parecido')
       flag = 0
       return flag


def classify(sentence, words, classes, documents, model):
    # gerar probabilidades para o modelo
    p = bow(sentence, words)
    d = len(p) #numero de palavras em p
    f = len(documents)
    a = np.zeros([f, d])
    tot = np.vstack((p,a))
    model = keras.models.load_model(model)
    results = model.predict(tot)[0]
    # filtrar previsões abaixo do threshold
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    # numerar por probabilidade
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    if not results:
        return return_list
    for r in results:
        return_list.append((classes[r[0]], r[1]))
        # return tuple of intent and probability
    return return_list[0]



def find_model(flag):
    keys= []
    words = []
    classes = []
    documents = []
    responses = []
    model = []

    if flag == 0:
       sentence = 'teste'
    elif flag == 1:
        sentence = 'cantina'
    elif flag == 2:
        sentence = 'secretaria'
    elif flag == 3:
        sentence = 'serviços sociais'
    elif flag == 4:
        sentence = 'serviços académicos'
    elif flag == 8:
        sentence = 'biblioteca'

    for intent in dicionario:
        for key, value in intent.items():
            if value == sentence:
                keys = intent['keys']
                words = intent['words']
                classes = intent['classes']
                documents = intent['documents']
                responses = intent['responses']
                model = intent['model']
                return keys, words, classes, documents, responses, model

########################################## SERVIDOR ###########################################################

#criada uma instância da classe para a nossa aplicação, o argumento é o nome do módulo/pacoteself.
#deve ser colocado _name_, porque o _name_ do módulo pode mudar. É necessário para o Flask
#saber onde procurar por templates, ficheiros estátios, etc...
app = Flask(__name__)

#Aceder às variáveis do ambiente, precisamos do ACCESS TOKEN e VERIFY TOKEN, para conectar
#a aplicação ao facebook
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
#bot = Bot (ACCESS_TOKEN)

if __name__ == "__main__":
    app.run(debug = True)

########################################## RESPOSTA ###########################################################

#receber token enviado pelo facebook e verificar se é igual ao VERIFY_TOKEN que eu tenho
#se forem iguais, permitir o pedido, senão enviar erro
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET'])
def receive_message_get():
    return request.args['hub.challenge']


@app.route("/", methods = ['POST'])
def receive_message_post():
    output = request.get_json()
    print(output)
    global user_local
    global flag
    global language

    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('postback'):
                sender_id = message['sender']['id']
                recipient_id = message['recipient']['id']
                language = str(message['postback']['payload']).lower()
                change_language(language, sender_id)

            if message.get('message'):  # recebemos mensagem de alguem retirar o ID do utilizador que enviou a mensagem, para sabermos a quem enviar a msg
                sender_id = message['sender']['id']
                recipient_id = message['recipient']['id']

                if message['message'].get('text'):
                    text_received = message['message']['text']
                    text_received = text_received.lower()

                    if text_received == 'language':
                        send_select_language(ACCESS_TOKEN,sender_id)

                    else:
                        response_ai = response(text_received, sender_id)
                        print(response_ai)
                        if response_ai is None:
                            send_message(sender_id,'Não entendi o que disseste, escreve novamente a frase e de forma mais explícita, por favor.')
                        send_message(sender_id, response_ai)

                if message['message'].get('attachments'):
                    coordinates_received = message['message']['attachments']
                    for w in coordinates_received:
                        print(coordinates_received)
                        lat = w['payload']['coordinates']['lat']
                        long = w['payload']['coordinates']['long']
                        user_local = str(lat) + ',' + str(long)
                        get_loc(flag, ACCESS_TOKEN, sender_id, user_local)

    return "ok"


def response(sentence, userID, show_details = False):
    global flag
    flag = 0
    keys, words, classes, documents, responses, model = find_model(flag)
    results = classify(sentence, words, classes, documents, model)
    print(results)

    if not results:
        return None


    flag = select_if(results[0])
    print('FLAG1', flag)
    if flag == 1:
        #cantina
        keys, words, classes, documents, responses, model = find_model(flag)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)

        if results2[0] == 'localizaçao':
           send_message(userID,'Manda a tua localização')
        if results2[0] == 'location':
           send_message(userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta

    elif flag == 2:
        #secretaria
        keys, words, classes, documents, responses, model = find_model(flag)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)

        if results2[0] == 'localizaçao':
           send_message(userID,'Manda a tua localização')
        if results2[0] == 'location':
           send_message(userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta


    elif flag == 3:
        #servicos sociais
        keys, words, classes, documents, responses, model = find_model(flag)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)

        if results2[0] == 'localizaçao':
           send_message(userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
           send_message(userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta


    elif flag == 4:
        #servicos academicos
        keys, words, classes, documents, responses, model = find_model(flag)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)

        if results2[0] == 'localizaçao':
           send_message(userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
           send_message(userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta



    elif flag == 5 or flag == 6 or flag == 7:

        resposta = search_response(results, responses)
        return resposta

    elif flag == 8:
        #biblioteca
        keys, words, classes, documents, responses, model = find_model(flag)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)

        if results2[0] == 'localizaçao':
           send_message(userID,'Manda a tua localização')
        if results2[0] == 'location':
           send_message(userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta



def send_message(recipient_id, message_text):
    #print("sending message to {recipient}: {text}".format(recipient = recipient_id, text = message_text))
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
