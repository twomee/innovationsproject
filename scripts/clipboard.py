import keyboard
import AppKit

class ClipBoard():

    #init the vars, will contain dict where the key is the word 'clipboard' and the values are the texts that copied to clipboard:
    #{'clipboard':['some text that copied','some more text that copied']}
    def __init__(self,logger,dateManager,redis,queue):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.pasteboard = AppKit.NSPasteboard.generalPasteboard()

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromRedisDB(self,data):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result =  self.r.getValue(self.dateManager.getDate())
            self.clipboardDict = result
            if(self.clipboardDict.get("clipboard") is None):
                self.clipboardDict["clipboard"] = [data]
            else:
                self.clipboardDict["clipboard"].append(data)
            self.logger.info("on ClipBoard ->refreshDataFromRedisDB-> self.clipboardDict: ")
            self.logger.info(self.clipboardDict)
        else:
            self.clipboardDict = {}
            self.clipboardDict["clipboard"] = [data]
        self.queue.put(self.clipboardDict)

            
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
            except Exception as error:
                self.logger.error(error)

    #insert and update the dict object on DB where the key is date.
    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on ClipBoard ->updatreDBValues-> self.clipboardDict: ")
        self.logger.info(self.clipboardDict)



                                
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
