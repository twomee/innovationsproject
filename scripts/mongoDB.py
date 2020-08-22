import pymongo
from pymongo import MongoClient



# models:
# keyListner:
# {name: keyListner, data: {a:1,b:2,c:3,g:8}}
# temperature:
# {name: cpu, data: [10,70,50]}
# clipboard:
# {name: clipboard, data: [some,text,that,copied]}
class mongoDB:
    CONNECTION_DETAILS = 'mongodb://localhost:27017'
    def __init__(self,logger):
        self.logger = logger
        self.client = MongoClient(mongoDB.CONNECTION_DETAILS)
        self.db = self.client.innovations # specify which database you actually want to use

    def updateNewOrExistDocument(self,docId,key,data):
        document = self.db[docId] # specifies which collection you’ll be using 
        filter = { 'name': key } 
        newvalues = { "$set": { "data": data } } 
        result = self.db[docId].update(filter,newvalues,upsert=True) #filter means takes the document with key in filter and update the same object with the newvalues we set above. upsert means if document doesnt exists, create new one
        print("!$#%#$&&#$*&#%*$%&@#$&^$@*$%^*(%#$^",result )
        self.logger.info('MONGODB ==> One doc: {0}'.format(result))

    def retrieveDocument(self,docId,key):
        doc = self.db[docId].find_one({"name":key},{'_id': False})
        self.logger.info("MONGODB ==> document value: ", doc)
        return doc

    def deleteDocument(self,docId):
        self.db[docId].drop()


 