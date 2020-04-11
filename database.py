from connect import Connect
import pymongo
from pymongo import MongoClient
#from pprint import pprint
from send_templates import send_message, get_started


connection = Connect.get_connection()
db = connection.test

def verify_id(ACCESS_TOKEN, id):
    cursor = db.inventory.find_one({"id": {"$exists": "true", "$in": [id]}})
    if cursor:
        return True
    else:
        return False

def delete_id(id):
    db.inventory.delete_one({"id": {"$exists": "true", "$in": [id]}})

def insert_id(id):
    db.inventory.insert_one({"id": id, "language": 'english'})

def verify_language(id):
    #cursor_language = db.inventory.find_one({"id": {"$exists": "true", "$in": [id]}})
    cursor = db.inventory.find_one({"id": {"$exists": "true", "$in": [id]}})
    if cursor:
        language_bd = cursor['language']
        return language_bd
    else:
        language_bd = 'portuguese'
        return language_bd

        #print('Linguagem já existia,no user:' + str(id) + 'era:' + language_db)


def set_bd_language(ACCESS_TOKEN, id, language):
    cursor = db.inventory.find_one({"id": {"$exists": "true", "$in": [id]}})
    if cursor:
        db.inventory.update_one({"id":id},{"$set":{"language": language}})
        if language == 'portuguese':
            send_message(ACCESS_TOKEN, id, 'Vamos falar em Português! :)')
        elif language == 'english':
            send_message(ACCESS_TOKEN, id, 'We are going to speak in English! :)')
    #else: #
    #    db.inventory.insert_one({"id": id, "language": language}) #
