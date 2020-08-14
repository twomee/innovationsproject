import subprocess
import time
import json

class temperature():

    def __init__(self,logger,dateManager,redis):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.refreshDataFromRedisDB()


    def cpuTemp(self):
        while True:
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            result = subprocess.run(['osx-cpu-temp'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\u00b0C\n", "")
            self.logger.info("CPU temperature is " + result)
            self.insertToDict(result)
            print(self.tempDict)
            self.updatreDBValues()


    def insertToDict(self,result):
        self.tempDict['cpu'].append(result)

    def refreshDataFromRedisDB(self):
        result =  self.r.getValue(self.dateManager.getDateAndTime())
        if(result is None):
            self.tempDict = {"cpu":[]}
        else:
            self.tempDict = result
            self.tempDict["cpu"] = []


    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDateAndTime(),
                                self.tempDict)
# t = temperature()
# t.cpuTemp()