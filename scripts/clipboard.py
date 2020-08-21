import keyboard
import AppKit

class ClipBoard():

    CLIPBOARD_KEY = "clipboard"
    #init the vars, will contain dict where the key is the word 'clipboard' and the values are the texts that copied to clipboard:
    #{'clipboard':['some text that copied','some more text that copied']}
    def __init__(self,logger,dateManager,redis,queue,elastic):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.pasteboard = AppKit.NSPasteboard.generalPasteboard()
        self.e = elastic
        self.elasticDocId = ClipBoard.CLIPBOARD_KEY # id of the class for elastic
        self.clipboardElasticIndex = self.dateManager.getDateWithoutSpecialCharsForElastic() + self.elasticDocId #index of elastic for this class
        self.refreshAndUpdateDataFromElastic() 


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
        result = self.e.getData(self.clipboardElasticIndex, self.elasticDocId)
        if(result != None):
            self.clipboardDictElastic = result
        else:
            self.clipboardDictElastic = {}
            self.clipboardDictElastic[ClipBoard.CLIPBOARD_KEY] = [] 

    # update the elastic index document with the object details of this class
    def updateElasticIndexes(self,result):
        self.clipboardDictElastic[ClipBoard.CLIPBOARD_KEY].append(result)
        self.e.putDataOnIndex(self.clipboardElasticIndex,self.clipboardDictElastic,self.elasticDocId)

                                
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
