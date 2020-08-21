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
    ELASTIC_DATA_HEADER_NAME = '_source'

    def __init__(self,logger):
        self.es = Elasticsearch([{'host': Elastic.HOST, 'port': Elastic.PORT}])
        self.logger = logger
        self.searchObject = None

    def putDataOnIndex(self,indexValue,obj,docId):
        self.logger.info("updating document in index")
        res = self.es.index(index=indexValue,body=json.dumps(obj),id = docId)
        res =self.getData(indexValue,docId)

    
    def getData(self,indexValue,docId):
        result = None
        index_exists = self.es.indices.exists(index=indexValue)
        if(index_exists == True):
            res = self.es.get(index=indexValue,id = docId) 
            #equal to:
            # self.es.search(index=indexValue,body={"query":{ "ids":{ "values": [ docId ] } } })
            self.logger.info("elastic data of index: " + indexValue + " with id: " + docId + " is: " + str(res))
            result = res[Elastic.ELASTIC_DATA_HEADER_NAME]
        return result
        


# options to search:
# search for all data:
    # self.searchObject = Search(using=self.es, index=indexValue)
    # for hit in self.searchObject:
    #     print(hit)
# search for indexes:
    # for index in self.es.indices.get('*'):
    #     print (index)
    #     r = requests.get('http://localhost:9200/'+ index)
    #     print(r.content)


#option to delete:
#via curl:
    # curl -X DELETE 'http://localhost:9200/_all'

#check if index exists:
    #index_exists = self.es.indices.exists(index=indexValue)

#update index with existing values(not worked for me):
    #self.es.update(index=indexValue,body=json.dumps(obj),id = docId)