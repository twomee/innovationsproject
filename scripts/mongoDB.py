import pymongo
from pymongo import MongoClient



# documents:
# 24082020keyListner:
# {name: keyListner, data: {a:1,b:2,c:3,g:8}}
# 24082020temperature:
# {name: cpu, data: [10,70,50]}
# 24082020clipboard:
# {name: clipboard, data: [some,text,that,copied]}
class mongoDB:

    def __init__(self,logger,propertiesLoader):
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()
        try:
            self.client = MongoClient(self.MONGODB_CONNECTION_DETAILS)
            # self.client.drop_database('innovations')
            self.db = self.client.innovations # specify which database you actually want to use
        except Exception as e:
            self.logger.error("error on connect to mongoDB")


    def initalizeProperties(self):
        self.MONGODB_CONNECTION_DETAILS = self.propertiesLoader.getProperty("MONGODB_CONNECTION_DETAILS")
        self.logger.info("on mongoDB -> properties initalized")

    # update or insert new(if not exist) the data to the same object by key name which is 'name'
    def updateNewOrExistDocument(self,docId,key,data):
        try:
            document = self.db[docId] # specifies which collection you’ll be using 
            filter = { 'name': key } 
            newvalues = { "$set": { "data": data } } 
            result = self.db[docId].find_one_and_update(filter,newvalues,upsert=True,new = True) #filter means takes the document with key in filter and update the same object with the newvalues we set above. upsert means if document doesnt exists, create new one
            self.logger.info('MONGODB ==> One doc updated: {0}'.format(result))
        except Exception as e:
            self.logger.error('MONGODB ==> error on updating document')

    # get the value of dict with key name of key parameter
    def retrieveDocument(self,docId,key):
        doc = None
        try:
            doc = self.db[docId].find_one({"name":key},{'_id': False})
            self.logger.info("MONGODB ==> document value: ", doc)
        except Exception as e:
            self.logger.error('MONGODB ==> error on retrieve document')   
        return doc

    # delete document
    def deleteDocument(self,docId):
        self.db[docId].drop()
        self.logger.info("MONGODB ==> docId: " + docId + "was dropped")



 