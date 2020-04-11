
import json
import requests


def send_select_language(ACCESS_TOKEN, userID):

    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": userID
        },
        "message":{
        "attachment":{
        "type":"template",
        "payload":{
        "template_type":"button",
        "text":"Select language",
        "buttons":[
          {
            "type":"postback",
            "title": "Português",
            "payload": "portuguese"
          },
          {
            "type":"postback",
            "title": "English",
            "payload": "english"
          }
          ]
         }
        }}
})
    r = requests.post("https://graph.facebook.com/v3.3/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def send_message(ACCESS_TOKEN, recipient_id, message_text):
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
    r = requests.post("https://graph.facebook.com/v3.3/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)



def get_started(ACCESS_TOKEN, recipient_id):
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
    "get_started":{
    "payload":"hand_shake"

    }
    })
    r = requests.post("https://graph.facebook.com/v3.3/me/messenger_profile", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)



def send_select_bd_permission(ACCESS_TOKEN, userID):
    hello_str_pt = "Olá, eu sou um bot para te ajudar a encontrar serviços na universidade, saber ementa, horários de funcionamento e até informações adicionais!"
    hello_str_eng = "Hi, I'm a bot that will help you find some services in the university, know the menu, schedules and even aditional informations!"
    str_pt = "Para poder falar contigo preciso de armazenar informação na base de dados, Isso inclui o teu Facebook ID e a tua linguagem de preferência, nada mais! Posso? :) "
    str_eng = "But first, to be able to talk to you I need to store information in my database, that includes your Facebook ID and your language of preference, nothing more! Can I? :)"
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": userID
        },
        "messaging_type": "RESPONSE",
        "message":{
         "text": str_eng, #+ "\n" + str_eng,
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Yes",#/ Yes",
        "payload":"yes_db",
      },{
        "content_type":"text",
        "title":"No",# / No",
        "payload":"no_db",
      }
    ]
         }
    })
    r = requests.post("https://graph.facebook.com/v3.3/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def send_permission_to_talk(ACCESS_TOKEN, userID):
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": userID
        },
        "messaging_type": "RESPONSE",
        "message":{
         "text": "Let\'s start talking!",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Yes, sure!",
        "payload":"yes_talk",
      },{
        "content_type":"text",
        "title":"No thanks...",
        "payload":"no_talk",
      }
    ]
         }
    })
    r = requests.post("https://graph.facebook.com/v3.3/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
