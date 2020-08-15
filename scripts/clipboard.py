import keyboard
import AppKit

class ClipBoard():

    #init the vars, will contain dict where the key is the word 'clipboard' and the values are the texts that copied to clipboard:
    #{'clipboard':['some text that copied','some more text that copied']}
    def __init__(self,logger,dateManager,redis):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.refreshDataFromRedisDB()
        self.pasteboard = AppKit.NSPasteboard.generalPasteboard()

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshDataFromRedisDB(self):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result =  self.r.getValue(self.dateManager.getDate())
            self.clipboardDict = result
            self.clipboardDict["clipboard"] = []
            self.logger.info("on ClipBoard ->refreshDataFromRedisDB-> self.clipboardDict: ")
            self.logger.info(self.clipboardDict)
        else:
            self.clipboardDict = {}
            self.clipboardDict["clipboard"] = []

            
    #take the text that copy to clipboard and insert him to DB only when he get changed. alwayes listen to changes by loop
    def copyFromClipBoard(self):
        tempCopy = "a"
        pasteboardString = self.pasteboard.stringForType_(AppKit.NSStringPboardType)
        while True:
            try:
                pasteboardString = self.pasteboard.stringForType_(AppKit.NSStringPboardType)
                if(pasteboardString != tempCopy):
                    tempCopy = pasteboardString
                    self.insertToDict(pasteboardString)
                    self.updatreDBValues()
            except Exception as error:
                self.logger.error(error)

    #insert the new data to the dict
    def insertToDict(self,pasteboardString):
        previousData = self.r.getValue(self.dateManager.getDate())
        self.clipboardDict = previousData
        self.logger.warning("!!!!!!!!!!!!!!!!!previousData :", self.clipboardDict )
        self.logger.warning(self.clipboardDict )
        self.clipboardDict["clipboard"].append(pasteboardString)

    #insert and update the dict object on DB where the key is date.
    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.clipboardDict)
        self.logger.info("on ClipBoard ->updatreDBValues-> self.clipboardDict: ")
        self.logger.info(self.clipboardDict)



                                
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
