import keyboard
import AppKit

class ClipBoard():

    def __init__(self,logger,dateManager,redis):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.refreshDataFromRedisDB()

    def copyFromClipBoard(self):
        tempCopy = "a"
        pb = AppKit.NSPasteboard.generalPasteboard()
        pbstring = pb.stringForType_(AppKit.NSStringPboardType)
        while True:
            try:
                pbstring = pb.stringForType_(AppKit.NSStringPboardType)
                if(pbstring != tempCopy):
                    tempCopy = pbstring
                    self.insertToDict(pbstring)
                    self.updatreDBValues()
            except Exception as error:
                self.logger.error(error)

    def insertToDict(self,pbstring):
        self.clipboardDict['clipboard'].append(pbstring)

    def refreshDataFromRedisDB(self):
        result =  self.r.getValue(self.dateManager.getDateAndTime())
        if(result is None):
            self.clipboardDict = {"clipboard":[]}
        else:
            self.clipboardDict = result
            self.clipboardDict["clipboard"] = []


    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDateAndTime(),
                                self.clipboardDict)

                                
# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
