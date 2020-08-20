import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json

# model:
# index: 18/8/2020 
# type : date
# data: {a:1,b:2,c:3}
# data: {cpu:[60,70,10]}
# data: {clipboard: [some,text,copied,here]} 

class Elastic:
    HOST = 'localhost'
    PORT = 9200

    def __init__(self,logger):
        self.es = Elasticsearch([{'host': Elastic.HOST, 'port': Elastic.PORT}])
        self.logger = logger
        self.searchObject = None

    def putDataOnIndex(self,indexValue,obj,docId):
        index_exists = self.es.indices.exists(index=indexValue)
        # if(index_exists == False):
        self.logger.info("updating document in index")
        res = self.es.index(index=indexValue,body=json.dumps(obj),id = docId)
        print(res)
        res =self.getData(indexValue,docId)
        # else:
        #     res = self.getData(indexValue)
        #     self.logger.info("!!!!!!!!!!!!res: " , res)
        #     self.logger.info("index exist, update index")
        #     self.es.update(index=indexValue,body=json.dumps(obj),id)
    
    def getData(self,indexValue,docId):
        # self.searchObject = Search(using=self.es, index=indexValue)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # for hit in self.searchObject:
        #     print(hit)

        # for index in self.es.indices.get('*'):
        #     print (index)
        #     r = requests.get('http://localhost:9200/'+ index)
        #     print(r.content)

        res = self.es.search(index=indexValue,body={"query":{ "ids":{ "values": [ docId ] } } })
        print(res)
        


        # curl -X DELETE 'http://localhost:9200/_all'