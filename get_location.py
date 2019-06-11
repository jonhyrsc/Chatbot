
#import googlemaps
#import webbrowser
import json
import requests

#from app import flag, user_local

######################DEFINE LOCATIONS#########################################

#gmaps = googlemaps.Client(key='AIzaSyA0EwTyG73shUDpzJYfYYmhIImNfwO6FHA')

loc_biblioteca= str(41.285641) + ',' + str(-7.740550)
loc_servico_academico = str(41.287856) + ',' + str(-7.739196)
loc_servico_social = str(41.301267) + ',' + str(-7.737407)
loc_cantina_principal = str(41.289540) + ',' + str(-7.736570)
loc_cantina_codessais = str(41.301299) + ',' + str(-7.737452)
loc_cantina_alem_rio = str(41.300481) + ',' + str(-7.732519)
loc_secretaria = str(41.287565) + ',' + str(-7.738699)
#loc_user=str(lat) + ',' + str(long)


####################SEND_REQUEST################################################
def get_loc(flag, ACCESS_TOKEN, userID, user_local)  :
    #get_flag()

    print('FLAG:', flag)



    if flag == 1:
    #cantina
        destination =  loc_cantina_principal

    elif flag == 2:
    #secretaria
        destination =  loc_secretaria

    elif flag == 3:
    #servicos sociais
        destination =  loc_servico_social

    elif flag == 4:
    #servicos academicos
        destination =  loc_servico_academico

    elif flag == 8:
    #biblioteca
        destination =  loc_biblioteca

    #result = gmaps.directions(user_local,destination)
    address = 'origin='+user_local+'&'+'destination='+destination
    address = address.lower()
    address = address.replace(" ","+")
    url = "https://www.google.com/maps/dir/?api=1&"
    result_url = url+address
    send_message_template(result_url,ACCESS_TOKEN, userID)

    #return result_url
    #webbrowser.open_new(result_url)



def send_message_template(result_url, ACCESS_TOKEN, userID):

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
                "template_type":"generic",
                "elements":[
                    {
                    "title":"Mapa",
                    "image_url":"https://logodownload.org/wp-content/uploads/2018/01/google-maps-logo.png",
                    "subtitle":"",
                    "default_action": {
                      "type": "web_url",
                      "url": result_url,
                      "webview_height_ratio": "tall",
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url":result_url,
                    "title":"View Website"
                  }
                  ]
            }
            ]
        }
    }
 }
})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
