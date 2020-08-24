import redis
import json



# the key will be the date of today.
# the data will be as below, every class that will save data will be inside of some data structure.
# the keys are the diffrents betweens the classes exclude the alphabet counter which conatin a alphabet key and value of int that count the time of presses.

# data = {
#     "10/8/2020": {
#     a:1,
#     b:2,
#     cpu:[60,50,30,20,50],
#     clipboard:[some,text,that,copied]
#    }
# }
class redisDB:

    #init redis DB
    def __init__(self,logger):
        self.logger = logger
        self.r = redis.Redis()

    # set value to object on redis DB with transactional action.
    # mean that if two modules trying to set same object,
    # one will be waiting to the first to finish update th object.
    def setTransactionalValue(self,date,queue):
        with self.r.pipeline() as pipe:
            error_count = 0
            while error_count != -1:
                try:
                    self.logger.info("REDISDB ==> started redis insert")
                    # Get available inventory, watching for changes
                    # related to this itemid before the transaction
                    pipe.watch(date)
                    self.logger.info("REDISDB ==> started watch")
                    pipe.multi()
                    #we inserting the data as json object to support complex structures
                    pipe.set(date,json.dumps(queue.get()))
                    self.logger.info("REDISDB ==> etted values on db")
                    pipe.execute()
                    error_count = -1
                    self.logger.info("REDISDB ==> executeed insert")
                except redis.WatchError:
                    # Log total num. of errors where trying to set a new value to existing key.
                    # if some module trying to update same key, the object is locked by watch
                    # then try the same process again of WATCH/SET/MULTI/EXEC
                    error_count += 1
                    self.logger.warning(
                        "REDISDB ==> WatchError #%d: %s; retrying",
                        error_count, date
                        )
        return None

    #get value from redis DB by key which is the date of today
    def getValue(self,key):
        #we loading the data with json module because maybe the structure is complex
        result = json.loads(self.r.get(key))
        #if there is no data from DB(new day)
        if(result is None):
            return None
        return result
        
    #check if key exists on redis DB
    def isKeyExists(self,key):
        return self.r.exists(key)





