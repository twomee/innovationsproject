import requests
from elasticsearch import Elasticsearch
import json

# res = requests.get('http://localhost:9200')
# print(res.content)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200') 
i = 1
while r.status_code == 200:
    r = requests.get('http://swapi.co/api/people/'+ str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i=i+1
 
print(i)


#ping
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


# search
elastic_client.search(index="some_index", body=some_query)

# get
es.get(index='sw', doc_type='people', id=5)

# index
es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))

# first use:
#  es.indices.create(index='my-index', ignore=400) -> check if index exist
# to  create index and then fill him with value with:
# es.index(index="my-index", id=42, body={"any": "data", "timestamp": datetime.now()})