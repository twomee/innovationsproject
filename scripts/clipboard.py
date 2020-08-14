import keyboard
import AppKit

class ClipBoard():

    def __init__(self,logger):
        self.logger = logger

    def copyFromClipBoard(self):
        tempCopy = "a"
        pb = AppKit.NSPasteboard.generalPasteboard()
        pbstring = pb.stringForType_(AppKit.NSStringPboardType)
        while True:
            try:
                pbstring = pb.stringForType_(AppKit.NSStringPboardType)
                if(pbstring != tempCopy):
                    tempCopy = pbstring
                    self.logger.info("Pastboard string:" + pbstring)
            except Exception as error:
                self.logger.error(error)


# if __name__ == '__main__':
#     cb = ClipBoard()
#     cb.copyFromClipBoard()
