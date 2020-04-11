
import json
import requests





def send_emoji(ACCESS_TOKEN, userID):

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
        "type":"image",
        "payload":{
        "url": 'https://scontent.xx.fbcdn.net/v/t39.1997-6/39178562_1505197616293642_5411344281094848512_n.png?_nc_cat=1&_nc_ad=z-m&_nc_cid=0&_nc_zor=9&_nc_ht=scontent.xx&oh=f6a78b2f5313605ed51753f36910ba5f&oe=5D7D2175'
        }
        }
        }
})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
