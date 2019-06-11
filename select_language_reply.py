
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
