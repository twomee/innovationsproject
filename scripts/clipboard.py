import keyboard
import AppKit


class ClipBoard():

    CLIPBOARD_KEY = "clipboard"
    MONGO_OBJECT_ID_KEY = "name"
    MONGO_OBJECT_DATA_KEY = "data"
    #init the vars, will contain dict where the key is the word 'clipboard' and the values are the texts that copied to clipboard:
    #{'clipboard':['some text that copied','some more text that copied']}
    def __init__(self,logger,dateManager,redis,queue,elastic,mongo,propertiesLoader):
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.pasteboard = AppKit.NSPasteboard.generalPasteboard()
        self.e = elastic
        self.m = mongo
        self.NoSqlDocId = ClipBoard.CLIPBOARD_KEY # id of the class for elastic
        self.keyListenerElasticIndexAndMongoDocId = self.dateManager.getDateWithoutSpecialCharsForElastic() + self.NoSqlDocId #index of elastic for this class
        self.refreshAndUpdateDataFromElastic() 
        self.refreshAndUpdateDataFromMongoDB()

    def initalizeProperties(self):
        self.CLIPBOARD_KEY = self.propertiesLoader.getProperty("CLIPBOARD_KEY")
        self.MONGO_OBJECT_ID_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_ID_KEY")
        self.MONGO_OBJECT_DATA_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_DATA_KEY")
        self.logger.info("on ClipBoard -> properties initalized")

    #take the text that copy to clipboard and insert him to DB only when he get changed. alwayes listen to changes by loop
    def copyFromClipBoard(self):
        #take temp copy of clipboard to prevent insert same value all the time
        #and also for prevent to insert trash like copy from last run
        tempCopy = self.pasteboard.stringForType_(AppKit.NSStringPboardType)
        pasteboardString = None
        while True:
            try:
                pasteboardString = self.pasteboard.stringForType_(AppKit.NSStringPboardType)
                if(pasteboardString != tempCopy and pasteboardString is not None):
                    tempCopy = pasteboardString
                    # self.insertToDict(pasteboardString)
                    self.refreshAndUpdateDataFromRedisDB(pasteboardString)
                    self.updatreDBValues()
                    self.updateElasticIndexes(pasteboardString)
                    self.updateMongoDBValues(pasteboardString)
            except Exception as error:
                self.logger.error(error)

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromRedisDB(self,data):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result =  self.r.getValue(self.dateManager.getDate())
            self.clipboardDict = result
            if(self.clipboardDict.get(self.NoSqlDocId) is None):
                self.clipboardDict[self.NoSqlDocId] = [data]
            else:
                self.clipboardDict[self.NoSqlDocId].append(data)
        else:
            self.clipboardDict = {}
            self.clipboardDict[self.NoSqlDocId] = [data]
            self.logger.info("REDISDB ==> initalize clipboardDict: " + str(self.clipboardDict))
        self.queue.put(self.clipboardDict)
        self.logger.info("REDISDB ==> update self.clipboardDict: " + str(self.clipboardDict))

    #insert and update the dict object on DB where the key is date.
    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on ClipBoard ->updatreDBValues-> self.clipboardDict: " )
        self.logger.info(self.clipboardDict)


    # get the data from elastic to this object when the code is loading to continue the consisntent of the data
    def refreshAndUpdateDataFromElastic(self):
        result = self.e.getData(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.clipboardDictElastic = result
        else:
            self.clipboardDictElastic = {}
            self.clipboardDictElastic[self.NoSqlDocId] = [] 
            self.logger.info("ELASTIC ==> initalize clipboardDictElastic: " + str(self.clipboardDictElastic))


    # update the elastic index document with the object details of this class
    def updateElasticIndexes(self,result):
        self.clipboardDictElastic[self.NoSqlDocId].append(result)
        self.logger.info("ELASTIC ==> update clipboardDictElastic: " + str(self.clipboardDictElastic))
        self.e.putDataOnIndex(self.keyListenerElasticIndexAndMongoDocId,self.clipboardDictElastic,self.NoSqlDocId)


    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromMongoDB(self):
        result = self.m.retrieveDocument(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.clipboardDictMongo = result
        else:
            self.clipboardDictMongo = {self.MONGO_OBJECT_ID_KEY : self.NoSqlDocId, self.MONGO_OBJECT_DATA_KEY : [] }
            self.logger.info("MONGODB ==> initalize clipboardDictMongo: " + str(self.clipboardDictMongo))

    #insert and update the dict object on DB.
    def updateMongoDBValues(self,result):
        self.clipboardDictMongo[self.MONGO_OBJECT_DATA_KEY].append(result)
        self.logger.info("MONGODB ==> update clipboardDictMongo: " + str(self.clipboardDictMongo))
        self.m.updateNewOrExistDocument(self.keyListenerElasticIndexAndMongoDocId,self.NoSqlDocId,self.clipboardDictMongo[ClipBoard.MONGO_OBJECT_DATA_KEY])                            
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
