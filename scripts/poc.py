import random
import redis
import logging

random.seed(444)
hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
}

r = redis.Redis(db=0)
# with r.pipeline() as pipe:
#     for h_id, hat in hats.items():
#         pipe.hmset(h_id, hat)
#     pipe.execute()
# r.bgsave()

keys = r.keys()
# print(keys)
data = {}
for key in keys:
    try:
        key = key.decode("utf-8")
        print(key)
        data[key] = r.hgetall(key)
        print(data)
    except Exception:
        logging.error("the type of the key: " + key + " is not hash type")

data = {}


# data = {
#     "10/8/2020":
#     a:1,
#     b:2,
#     cpu:60,
#     clipboard:{some,text,that,copied}
# }


