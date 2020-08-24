import keyboard
import AppKit

class ClipBoard():

    CLIPBOARD_KEY = "clipboard"
    MONGO_OBJECT_ID_KEY = "name"
    MONGO_OBJECT_DATA_KEY = "data"
    #init the vars, will contain dict where the key is the word 'clipboard' and the values are the texts that copied to clipboard:
    #{'clipboard':['some text that copied','some more text that copied']}
    def __init__(self,logger,dateManager,redis,queue,elastic,mongo):
        self.logger = logger
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
            if(self.clipboardDict.get(ClipBoard.CLIPBOARD_KEY) is None):
                self.clipboardDict[ClipBoard.CLIPBOARD_KEY] = [data]
            else:
                self.clipboardDict[ClipBoard.CLIPBOARD_KEY].append(data)
        else:
            self.clipboardDict = {}
            self.clipboardDict[ClipBoard.CLIPBOARD_KEY] = [data]
        self.queue.put(self.clipboardDict)

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
            self.clipboardDictElastic[ClipBoard.CLIPBOARD_KEY] = [] 

    # update the elastic index document with the object details of this class
    def updateElasticIndexes(self,result):
        self.clipboardDictElastic[ClipBoard.CLIPBOARD_KEY].append(result)
        self.e.putDataOnIndex(self.keyListenerElasticIndexAndMongoDocId,self.clipboardDictElastic,self.NoSqlDocId)


    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromMongoDB(self):
        result = self.m.retrieveDocument(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.clipboardDictMongo = result
        else:
            self.clipboardDictMongo = {ClipBoard.MONGO_OBJECT_ID_KEY : self.NoSqlDocId, ClipBoard.MONGO_OBJECT_DATA_KEY : [] }

    #insert and update the dict object on DB.
    def updateMongoDBValues(self,result):
        self.clipboardDictMongo[ClipBoard.MONGO_OBJECT_DATA_KEY].append(result)
        self.m.updateNewOrExistDocument(self.keyListenerElasticIndexAndMongoDocId,self.NoSqlDocId,self.clipboardDictMongo[ClipBoard.MONGO_OBJECT_DATA_KEY])                            
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
