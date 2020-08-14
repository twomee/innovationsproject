import keyboard
import AppKit

class ClipBoard():

    def __init__(self,logger,dateManager,redis):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.refreshDataFromRedisDB()
        self.pasteboard = AppKit.NSPasteboard.generalPasteboard()


    def refreshDataFromRedisDB(self):
        result =  self.r.getValue(self.dateManager.getDateAndTime())
        if(result is None):
            self.clipboardDict = {"clipboard":[]}
        else:
            self.clipboardDict = result
            self.clipboardDict["clipboard"] = []
            
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

    def insertToDict(self,pasteboardString):
        self.clipboardDict['clipboard'].append(pasteboardString)

    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDateAndTime(),
                                self.clipboardDict)

                                
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
