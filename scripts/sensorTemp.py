import subprocess
import time

class temperature():


    #init the vars, will contain dict with key of cpu and values of list with temperature of the cpu:
    #{'cpu':[60,50.5,70.3]}
    def __init__(self,logger,dateManager,redis,queue,elastic,mongo,propertiesLoader):
        self.propertiesLoader = propertiesLoader
        self.logger = logger
        self.initalizeProperties()
        self.dateManager = dateManager
        self.r = redis
        self.queue = queue
        self.e = elastic
        self.m = mongo
        self.NoSqlDocId = self.TEMPERATURE_KEY # id of the class for elastic
        self.keyListenerElasticIndexAndMongoDocId = self.dateManager.getDateWithoutSpecialCharsForElastic() + self.NoSqlDocId #index of elastic for this class
        self.refreshAndUpdateDataFromElastic()
        self.refreshAndUpdateDataFromMongoDB()


    def initalizeProperties(self):
        self.TEMPERATURE_KEY = self.propertiesLoader.getProperty("TEMPERATURE_KEY")
        self.DECODE_TYPE = self.propertiesLoader.getProperty("DECODE_TYPE")
        self.LINUX_COMMAND = self.propertiesLoader.getProperty("LINUX_COMMAND")
        self.MONGO_OBJECT_ID_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_ID_KEY")
        self.MONGO_OBJECT_DATA_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_DATA_KEY")
        self.logger.info("on temperature -> properties initalized")

    #call to subprocess and do linux command. taking the output and insert it to the dict object. this occurs every 1 minute
    def cpuTemp(self):
        while True:
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            result = subprocess.run([self.LINUX_COMMAND], stdout=subprocess.PIPE).stdout.decode(self.DECODE_TYPE).replace("\u00b0C\n", "")
            # self.logger.info("CPU temperature is " + result)
            # self.insertToDict(result)
            self.refreshAndUpdateDataFromRedisDB(result)
            self.updateDBValues()
            self.updateElasticIndexes(result)
            self.updateMongoDBValues(result)


    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromRedisDB(self,data):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result = self.r.getValue(self.dateManager.getDate())
            self.tempDict = result
            if(self.tempDict.get(self.NoSqlDocId) is None):
                self.tempDict[self.NoSqlDocId] = [data]
            else:
                self.tempDict[self.NoSqlDocId].append(data)
        else:
            self.tempDict = {}
            self.tempDict[self.NoSqlDocId] = [data]
            self.logger.info("REDISDB ==> initalize tempDict: " + str(self.tempDict))
        self.queue.put(self.tempDict)
        self.logger.info("REDISDB ==> update self.tempDict: " + str(self.tempDict))

    #insert and update the dict object on DB where the key is date.
    def updateDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on temperature ->updateDBValues-> self.tempDict: ")
        self.logger.info(self.tempDict)

    # get the data from elastic to this object when the code is loading to continue the consisntent of the data
    def refreshAndUpdateDataFromElastic(self):
        result = self.e.getData(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.tempDictElastic = result
        else:
            self.tempDictElastic = {}
            self.tempDictElastic[self.NoSqlDocId] = []
            self.logger.info("ELASTIC ==> initalize tempDictElastic: " + str(self.tempDictElastic))

    # update the elastic index document with the object details of this class
    def updateElasticIndexes(self,result):
        self.tempDictElastic[self.NoSqlDocId].append(result)
        self.logger.info("ELASTIC ==> update tempDictElastic: " + str(self.tempDictElastic))
        self.e.putDataOnIndex(self.keyListenerElasticIndexAndMongoDocId,self.tempDictElastic,self.NoSqlDocId)


    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromMongoDB(self):
        result = self.m.retrieveDocument(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.tempDictMongo = result
        else:
            self.tempDictMongo = {self.MONGO_OBJECT_ID_KEY : self.NoSqlDocId, self.MONGO_OBJECT_DATA_KEY : [] }
            self.logger.info("MONGODB ==> initalize tempDictMongo: " + str(self.tempDictMongo))


    #insert and update the dict object on DB.
    def updateMongoDBValues(self,result):
        self.tempDictMongo[self.MONGO_OBJECT_DATA_KEY].append(result)
        self.logger.info("MONGODB ==> update tempDictMongo: " + str(self.tempDictMongo))
        self.m.updateNewOrExistDocument(self.keyListenerElasticIndexAndMongoDocId,self.NoSqlDocId,self.tempDictMongo[self.MONGO_OBJECT_DATA_KEY])

# t = temperature()
# t.cpuTemp()