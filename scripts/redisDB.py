import redis
import logging
import json

class redisDB:

    def __init__(self):
        self.r = redis.Redis()

    def setTransactionalValue(self,date,obj):
        with self.r.pipeline() as pipe:
            error_count = 0
            while error_count != -1:
                try:
                    logging.info("started redis insert")
                    # Get available inventory, watching for changes
                    # related to this itemid before the transaction
                    pipe.watch(date)
                    logging.info("started watch")
                    pipe.multi()
                    pipe.set(date,json.dumps(obj))
                    logging.info("setted values on db")
                    # if(action == "get"):
                    #     pipe.hgetall(h_id)
                    pipe.execute()
                    error_count = -1
                    logging.info("executeed insert")
                except redis.WatchError:
                    # Log total num. of errors by this user to buy this item,
                    # then try the same process again of WATCH/HGET/MULTI/EXEC
                    error_count += 1
                    logging.warning(
                        "WatchError #%d: %s; retrying",
                        error_count, date
                        )
        return None


    def getValue(self,key):
        result = json.loads(self.r.get(key))
        return result





