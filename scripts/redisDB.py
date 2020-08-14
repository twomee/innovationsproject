import redis


class redisDB:

    r = redis.Redis()

    def actionTransactionalValue(self,obj,action):
        with r.pipeline() as pipe:
            error_count = 0
            while True:
                try:
                    # Get available inventory, watching for changes
                    # related to this itemid before the transaction
                    pipe.watch(itemid)
                    pipe.multi()
                    if(action == "set"):
                        pipe.hmset(h_id, hat)
                    if(action == "get"):
                        pipe.hgetall(h_id)
                    pipe.execute()
                except redis.WatchError:
                    # Log total num. of errors by this user to buy this item,
                    # then try the same process again of WATCH/HGET/MULTI/EXEC
                    error_count += 1
                    logging.warning(
                        "WatchError #%d: %s; retrying",
                        error_count, itemid
                        )
        return None





