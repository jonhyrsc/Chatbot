import pymongo
from pymongo import MongoClient

class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient("mongodb+srv://joao_user_1:eletro2014-@cluster0-df4f1.mongodb.net/test?retryWrites=true&w=majority")



# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = pymongo.MongoClient("mongodb+srv://joao_user_1:eletro2014-@cluster0-df4f1.mongodb.net/test?retryWrites=true&w=majority")
# db = client['test_database']
#
# users = db.user
# print(users)
#
# #db=client.admin
# # Issue the serverStatus command and print the results
# #serverStatusResult=db.command("serverStatus")
# #print(serverStatusResult)
