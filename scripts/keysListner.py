from pynput import keyboard


class KeysListnerObject():

    #init the vars, will contain dict which count the nubmers of times every char was pressed:
    #{'a':1,'b':2,'c':10,'d':0}
    def __init__(self,logger,dateManager,redis,queue,elastic,mongo,propertiesLoader):
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()
        self.dateManager =  dateManager
        self.r = redis
        self.queue = queue
        self.e = elastic
        self.m = mongo
        self.NoSqlDocId =  self.KEYLISTENER_KEY # id of the class for elastic
        self.keyListenerElasticIndexAndMongoDocId = self.dateManager.getDateWithoutSpecialCharsForElastic() + self.NoSqlDocId #index of elastic for this class
        self.refreshAndUpdateDataFromElastic()
        self.refreshAndUpdateDataFromMongoDB()

    def initalizeProperties(self):
        self.MONGO_OBJECT_ID_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_ID_KEY")
        self.MONGO_OBJECT_DATA_KEY = self.propertiesLoader.getProperty("MONGO_OBJECT_DATA_KEY")
        self.KEYLISTENER_KEY = self.propertiesLoader.getProperty("KEYLISTENER_KEY")
        self.logger.info("on KeysListnerObject -> properties initalized")

    #take every key that presses and insert him to dict object which mapping the chars.
    def on_press(self,key):
        try:
            self.logger.info('alphanumeric key {0} pressed'.format(
                key.char))
            self.refreshAndUpdateDataFromRedisDB(key)
            self.updateDBValues()
            if(key.char != "."): #unknown error happen when inserting dot to the dict
                self.updateElasticDictObject(key)
                self.updateElasticIndexes()
            self.updateMongoDictObject(key)
            self.updateMongoDBValues()


        except AttributeError:
            self.logger.error('special key {0} pressed'.format(
                key))
    
    #check which key was released after he pressed. not recorded on DB.
    def on_release(self,key):
        self.logger.info('{0} released'.format(key))
        # if key == keyboard.Key.esc:
        #     # Stop listener
        #     return False

    #run the listener of the keys
    def run(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromRedisDB(self,key):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result = self.r.getValue(self.dateManager.getDate())
            self.alphabet = result
            if(key.char in self.alphabet):
                self.alphabet[key.char] = self.alphabet[key.char] + 1
            else:
                self.alphabet[key.char] = 1
                self.logger.info("REDISDB ==> initalize alphabet: " + str(self.alphabet))
        else:
            self.alphabet = {}
            self.logger.info("REDISDB ==> initalize alphabet: " + str(self.alphabet))
        self.queue.put(self.alphabet)
        self.logger.info("REDISDB ==> update self.alphabet: " + str(self.alphabet))


    #insert and update the dict object on DB where the key is date.
    def updateDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on KeyListener ->updateDBValues-> self.alphabet: ")
        self.logger.info(self.alphabet)
    
    # get the data from elastic to this object when the code is loading to continue the consisntent of the data
    def refreshAndUpdateDataFromElastic(self):
        result = self.e.getData(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.alphabetElastic = result
        else:
            self.alphabetElastic = {}
            self.logger.info("ELASTIC ==> initalize alphabetElastic: " + str(self.alphabetElastic))


    # update the elastic object with the current values 
    def updateElasticDictObject(self,key):
        if(key.char in self.alphabetElastic):
            self.alphabetElastic[key.char] = self.alphabetElastic[key.char] + 1
        else:
            self.alphabetElastic[key.char] = 1
        self.logger.info("ELASTIC ==> update alphabetElastic: " + str(self.alphabetElastic))

    # update the elastic index document with the object details of this class
    def updateElasticIndexes(self):
        self.e.putDataOnIndex(self.keyListenerElasticIndexAndMongoDocId,self.alphabetElastic,self.NoSqlDocId)

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshAndUpdateDataFromMongoDB(self):
        result = self.m.retrieveDocument(self.keyListenerElasticIndexAndMongoDocId, self.NoSqlDocId)
        if(result != None):
            self.alphabetMognoDB = result
        else:
            self.alphabetMognoDB = {self.MONGO_OBJECT_ID_KEY : self.NoSqlDocId, self.MONGO_OBJECT_DATA_KEY : {} }
            self.logger.info("MONGODB ==> initalize alphabetMognoDB: " + str(self.alphabetMognoDB))

    def updateMongoDictObject(self,key):
        if(key.char in self.alphabetMognoDB[self.MONGO_OBJECT_DATA_KEY]):
            self.alphabetMognoDB[self.MONGO_OBJECT_DATA_KEY][key.char] = self.alphabetMognoDB[self.MONGO_OBJECT_DATA_KEY][key.char] + 1
        else:
            self.alphabetMognoDB[self.MONGO_OBJECT_DATA_KEY][key.char] = 1
        self.logger.info("MONGODB ==> update alphabetMognoDB: " + str(self.alphabetMognoDB))

    #insert and update the dict object on DB.
    def updateMongoDBValues(self):
        self.m.updateNewOrExistDocument(self.keyListenerElasticIndexAndMongoDocId,self.NoSqlDocId,self.alphabetMognoDB[self.MONGO_OBJECT_DATA_KEY])

# Collect events until released
# if __name__ == '__main__':
#     klo = KeysListnerObject()
#     klo.run()