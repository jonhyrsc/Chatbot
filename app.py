# Python libraries that we need to import for our bot
import os
# import sys
from get_location import get_loc
import requests
from flask import Flask, request, redirect, url_for
import json
import numpy as np
import random
from tensorflow import keras
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from send_templates import *
from database import *
import time
from sys import exit

ERROR_THRESHOLD = 0.6
flag = 0
user_local = ''
language_bd = 'english'
permission = ''

def set_language_dictionary(sender_id, language):
    global dicionario
    global stemmer
    global stop_words
    if language == 'portuguese':
        with open('dados.json', 'r') as json_file:
            dados = json.load(json_file)
        dicionario = {}
        dicionario = dados
        stemmer = SnowballStemmer('portuguese')
        stop_words = set(stopwords.words('portuguese'))

    else:
        with open('dados_ingleses.json', 'r') as json_file:
            dados = json.load(json_file)
        dicionario = {}
        dicionario = dados
        stemmer = SnowballStemmer('english')
        stop_words = set(stopwords.words('english'))



def strip_accents(text):
    try:
        text = str(text)
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)


def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


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
        return random.choice(lista_respostas)


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
    d = len(p)  # numero de palavras em p
    f = len(documents)
    a = np.zeros([f, d])
    tot = np.vstack((p, a))
    model = keras.models.load_model(model)
    results = model.predict(tot)[0]
    # filtrar previsões abaixo do threshold
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # numerar por probabilidade
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []

    if not results:
        return return_list
    for r in results:
        return_list.append((classes[r[0]], r[1]))
        # return tuple of intent and probability
    return return_list[0]


def find_model():
    #global flag
    keys = []
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

app = Flask(__name__)


ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']


if __name__ == "__main__":
    app.run(debug=True)


########################################## RESPOSTA ###########################################################

# receber token enviado pelo facebook e verificar se é igual ao VERIFY_TOKEN que eu tenho
# se forem iguais, permitir o pedido, senão enviar erro
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET'])
def receive_message_get():
    return request.args['hub.challenge']


@app.route("/", methods=['POST'])
def receive_message_post():
    output = request.get_json()
    print(output)
    global user_local
    #global flag
    global language_bd



    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            sender_id = message['sender']['id']
            recipient_id = message['recipient']['id']

            if message.get('message'):  # recebemos mensagem

                if message['message'].get('quick_reply'):
                    received_reply =  message['message']['quick_reply']
                    payload_reply = received_reply['payload']
                    if payload_reply == "yes_db":
                        insert_id(sender_id)
                        time.sleep(2)
                        #guardar na BD
                    elif payload_reply == 'no_db':
                        send_message(ACCESS_TOKEN, sender_id, 'Desculpa, assim não poderei falar contigo...')
                        #set_language_dictionary(sender_id, 'portuguese')
                        time.sleep(2)
                    # elif payload_reply == 'yes_talk':
                    #     permission = 'user_gave_permission'
                    #
                    # elif payload_reply == 'no_talk':
                    #     permission = 'user_did_not_gave_permission'


                if message['message'].get('text'):
                    text_received = message['message']['text']
                    text_received = text_received.lower()
                    text_received = strip_accents(text_received)
                    print(text_received)
                    bool_db = verify_id(ACCESS_TOKEN, sender_id)


                    if bool_db == False: #User não existe
                        #send_select_language(ACCESS_TOKEN, sender_id) #
                        send_message(ACCESS_TOKEN,sender_id,"Hi, I'm a bot! I can help you find university services, consult the menu of the canteen, see the schedule of the services of the university and even some aditional informations about them!")
                        send_message(ACCESS_TOKEN,sender_id,"You can also change language! To change between portuguese and english just type: language or linguagem. Then you can select wich language do you prefer :). ") #
                        send_select_bd_permission(ACCESS_TOKEN, sender_id)
                        #if language == 'portuguese':
                        #    send_message(ACCESS_TOKEN,sender_id,"Olá, eu sou um bot! Posso-te ajudar a encontrar serviços na universidade, saber ementa da cantina, horários de funcionamento e até informações adicionais!")
                        #    #send_select_language(ACCESS_TOKEN, sender_id)  ###########
                        #    send_select_bd_permission(ACCESS_TOKEN, sender_id)

                                                               #

                    language_bd = verify_language(sender_id)
                    set_language_dictionary(sender_id, language_bd) ###############


                    if text_received == 'language' or text_received == 'linguagem':
                        send_select_language(ACCESS_TOKEN, sender_id)
                    elif text_received == 'yes':   #/ yes':
                        send_permission_to_talk(ACCESS_TOKEN, sender_id)

                    elif text_received == 'no':  # / no':
                        send_message(ACCESS_TOKEN, sender_id, 'Ok... :( ')
                        time.sleep(5)
                        send_permission_to_talk(ACCESS_TOKEN, sender_id)
                        pass
                        #send_permission_to_talk(ACCESS_TOKEN, sender_id)

                    elif text_received == 'yes, sure!':  # / yes, sure!':
                        send_message(ACCESS_TOKEN, sender_id, 'What can I help you with?')

                    elif text_received == 'no thanks...':   #'/ No I do not want':
                        send_message(ACCESS_TOKEN, sender_id, 'Ok, until next time! ;)')
                    else:
                        if bool_db == True:
                            response_ai = response(text_received, sender_id)
                            print(response_ai)
                            if response_ai is None:
                                if language_bd == 'portuguese':
                                    send_message(ACCESS_TOKEN, sender_id,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                                    send_message(ACCESS_TOKEN, sender_id, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')
                                if language_bd == 'english':
                                    send_message(ACCESS_TOKEN, sender_id,'I don\'t understand what you want, try to write in a different way, please :)')
                                    send_message(ACCESS_TOKEN, sender_id, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')
                            send_message(ACCESS_TOKEN, sender_id, response_ai)

                if message['message'].get('attachments'):
                    attachment = message['message']['attachments']
                    for w in attachment:
                        if w['type'] == 'image':
                            send_message(ACCESS_TOKEN, sender_id, 'De nada! ;)')
                        if w['type'] == 'location':
                            lat = w['payload']['coordinates']['lat']
                            long = w['payload']['coordinates']['long']
                            user_local = str(lat) + ',' + str(long)
                            time.sleep(2)
                            print(flag)
                            get_loc(flag, ACCESS_TOKEN, sender_id, user_local)


            if message.get('postback'):
                print('Cheguei aqui')
                if message['postback'].get('payload'):
                    payload = str(message['postback']['payload']).lower()
                    language_bd = payload
                    # if bool_db == False:                                    #####
                    #     send_select_bd_permission(ACCESS_TOKEN, sender_id)  #########
                    # time.sleep(2)                                           ######
                    set_bd_language(ACCESS_TOKEN, sender_id, language_bd)


    return "ok"


def response(sentence, userID, show_details=False):
    global flag
    flag = 0
    #print(flag)
    keys, words, classes, documents, responses, model = find_model()
    print(keys)
    print(model)
    results = classify(sentence, words, classes, documents, model)
    print('RESULTS 1:', results)

    if not results:
        return None

    flag = select_if(results[0])

    #print('FLAG1', flag)

    if flag == 1:
        # cantina
        keys, words, classes, documents, responses, model = find_model()
        print('Key 2:',keys)
        print('Model 2:',model)
        results2 = classify(sentence, words, classes, documents, model)
        print('RESULTS 2:', results2)
        if not results2:
            language_bd = verify_language(userID)
            if language_bd == 'portuguese':
                send_message(ACCESS_TOKEN, userID,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                send_message(ACCESS_TOKEN, userID, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')

            else:
                send_message(ACCESS_TOKEN, userID,'I don\'t understand what you want, try to write in a different way, please :)')
                send_message(ACCESS_TOKEN, userID, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')


        if results2[0] == 'localizaçao':
            send_message(ACCESS_TOKEN, userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
            send_message(ACCESS_TOKEN, userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta

    elif flag == 2:
        # secretaria
        keys, words, classes, documents, responses, model = find_model()
        print('Key 2:',keys)
        print('Model 2:',model)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)
        if not results2:
            language_bd = verify_language(userID)
            if language_bd == 'portuguese':
                send_message(ACCESS_TOKEN, userID,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                send_message(ACCESS_TOKEN, userID, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')

            else:
                send_message(ACCESS_TOKEN, userID,'I don\'t understand what you want, try to write in a different way, please :)')
                send_message(ACCESS_TOKEN, userID, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')


        if results2[0] == 'localizaçao':
            send_message(ACCESS_TOKEN, userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
            send_message(ACCESS_TOKEN, userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta


    elif flag == 3:
        # servicos sociais
        keys, words, classes, documents, responses, model = find_model()
        print('Key 2:',keys)
        print('Model 2:',model)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)
        if not results2:
            language_bd = verify_language(userID)
            if language_bd == 'portuguese':
                send_message(ACCESS_TOKEN, userID,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                send_message(ACCESS_TOKEN, userID, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')

            else:
                send_message(ACCESS_TOKEN, userID,'I don\'t understand what you want, try to write in a different way, please :)')
                send_message(ACCESS_TOKEN, userID, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')


        if results2[0] == 'localizaçao':
            send_message(ACCESS_TOKEN, userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
            send_message(ACCESS_TOKEN, userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta


    elif flag == 4:
        # servicos academicos
        keys, words, classes, documents, responses, model = find_model()
        print('Key 2:',keys)
        print('Model 2:',model)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)
        if not results2:
            language_bd = verify_language(userID)
            if language_bd == 'portuguese':
                send_message(ACCESS_TOKEN, userID,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                send_message(ACCESS_TOKEN, userID, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')

            else:
                send_message(ACCESS_TOKEN, userID,'I don\'t understand what you want, try to write in a different way, please :)')
                send_message(ACCESS_TOKEN, userID, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')


        if results2[0] == 'localizaçao':
            send_message(ACCESS_TOKEN, userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
            send_message(ACCESS_TOKEN, userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta

    elif flag == 5 or flag == 6 or flag == 7:
        resposta = search_response(results, responses)
        return resposta

    elif flag == 8:
        # biblioteca
        keys, words, classes, documents, responses, model = find_model()
        print('Key 2:',keys)
        print('Model 2:',model)
        results2 = classify(sentence, words, classes, documents, model)
        print('results2:', results2)
        if not results2:
            language_bd = verify_language(userID)
            if language_bd == 'portuguese':
                send_message(ACCESS_TOKEN, userID,'Não entendi o que disseste, tenta escrever de forma mais explícita, por favor. :)')
                send_message(ACCESS_TOKEN, userID, 'Posso-te dar informações da cantina, serviços académicos, serviços sociais, secretaria e biblioteca. Ou seja, posso-te fornecer a ementa, horários e informação adicional.')
                results2[0] == 'info'
            else:
                send_message(ACCESS_TOKEN, userID,'I don\'t understand what you want, try to write in a different way, please :)')
                send_message(ACCESS_TOKEN, userID, 'I can give you information about the canteen, academic services, social services, secretary office and library. For instance, I can give you the menu, schedules and aditional information.')
                results2[0] == 'info'

        if results2[0] == 'localizaçao':
            send_message(ACCESS_TOKEN, userID, 'Por favor, partilha a tua localização')
        if results2[0] == 'location':
            send_message(ACCESS_TOKEN, userID, 'Share your location, please')

        resposta = search_response(results2, responses)
        return resposta
