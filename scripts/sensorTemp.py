import subprocess
import time

class temperature():

    TEMPERATURE_KEY = "cpu"
    DECODE_TYPE = 'utf-8'
    LINUX_COMMAND = 'osx-cpu-temp'
    #init the vars, will contain dict with key of cpu and values of list with temperature of the cpu:
    #{'cpu':[60,50.5,70.3]}
    def __init__(self,logger,dateManager,redis,queue,elastic):
        self.logger = logger
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.e = elastic
        self.elasticDocId = "temperature"
        self.temperatureElasticIndex = self.dateManager.getDateWithoutSpecialCharsForElastic() + self.elasticDocId
        self.refreshAndUpdateDataFromElastic()



    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromRedisDB(self,data):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result = self.r.getValue(self.dateManager.getDate())
            self.tempDict = result
            if(self.tempDict.get(temperature.TEMPERATURE_KEY) is None):
                self.tempDict[temperature.TEMPERATURE_KEY] = [data]
            else:
                self.tempDict[temperature.TEMPERATURE_KEY].append(data)
        else:
            self.tempDict = {}
            self.tempDict[temperature.TEMPERATURE_KEY] = [data]
        self.queue.put(self.tempDict)

    def refreshAndUpdateDataFromElastic(self):
        result = self.e.getData(self.temperatureElasticIndex, self.elasticDocId)
        if(result != None):
            self.tempDictElastic = result
        else:
            self.tempDictElastic = {}
            self.tempDictElastic[temperature.TEMPERATURE_KEY] = []


    #call to subprocess and do linux command. taking the output and insert it to the dict object. this occurs every 1 minute
    def cpuTemp(self):
        while True:
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            result = subprocess.run([temperature.LINUX_COMMAND], stdout=subprocess.PIPE).stdout.decode(temperature.DECODE_TYPE).replace("\u00b0C\n", "")
            # self.logger.info("CPU temperature is " + result)
            # self.insertToDict(result)
            self.refreshAndUpdateDataFromRedisDB(result)
            self.updateDBValues()
            self.tempDictElastic.append(result)
            self.putDataOnElasticIndex()

    #insert and update the dict object on DB where the key is date.
    def updateDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on temperature ->updateDBValues-> self.tempDict: ")
        self.logger.info(self.tempDict)

    def putDataOnElasticIndex(self):
        self.e.putDataOnIndex(self.temperatureElasticIndex,self.tempDictElastic,self.elasticDocId)


# t = temperature()
# t.cpuTemp()