import subprocess
import time

class temperature():

    #init the vars, will contain dict with key of cpu and values of list with temperature of the cpu:
    #{'cpu':[60,50.5,70.3]}
    def __init__(self,logger,dateManager,redis,queue):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.refreshDataFromRedisDB()

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshDataFromRedisDB(self):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result = self.r.getValue(self.dateManager.getDate())
            self.tempDict = result
            if(self.tempDict.get("cpu") is None):
                self.tempDict["cpu"] = []
            self.logger.info("on temperature ->refreshDataFromRedisDB-> self.tempDict: ")
            self.logger.info(self.tempDict)
        else:
            self.tempDict = {}
            self.tempDict["cpu"] = []

    #call to subprocess and do linux command. taking the output and insert it to the dict object. this occurs every 1 minute
    def cpuTemp(self):
        while True:
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            result = subprocess.run(['osx-cpu-temp'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\u00b0C\n", "")
            self.logger.info("CPU temperature is " + result)
            self.insertToDict(result)
            print(self.tempDict)
            self.updateDBValues()

    #insert the new data to the dict
    def insertToDict(self,result):
        previousData = self.r.getValue(self.dateManager.getDate())
        self.tempDict = previousData
        self.logger.warning("!!!!!!!!!!!!!!!!!previousData :", self.tempDict )
        self.logger.warning(self.tempDict )
        if("cpu" not in self.tempDict):
            self.tempDict["cpu"] = [result]
        else:
            self.tempDict["cpu"].append(result)
        self.queue.put(self.tempDict)

    #insert and update the dict object on DB where the key is date.
    def updateDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on temperature ->updateDBValues-> self.tempDict: ", self.tempDict)
        self.logger.info(self.tempDict)


# t = temperature()
# t.cpuTemp()