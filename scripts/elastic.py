from elasticsearch import Elasticsearch
import json

# models:
# keyListner:
# index: 1882020keyListner(date + class name) 
# data: {a:1,b:2,c:3}
# temperature:
# index: 1882020cpu(date + class name) 
# data: {cpu:[60,70,10]}
# clipboard:
# index: 1882020clipboard(date + class name) 
# data: {clipboard: [some,text,copied,here]} 

# every index have id and type. if we insert without id and type, the module will generate them.
# its important to give our id to be able to search by this id and update by this id.
# if we indexing same data with diffrent id, it will create a new doc sequnece and cause a mess.
# every calss that called to elastic have its own id that give when call to the function on this class.
class Elastic:

    #init the variables of elasic
    def __init__(self,logger,propertiesLoader):
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()
        try:
            self.es = Elasticsearch([{'host': self.ELASTIC_HOST, 'port': self.ELASTIC_PORT}])
        except Exception as e:
            self.logger.error("error on connect to elastic")

    def initalizeProperties(self):
        self.ELASTIC_HOST = self.propertiesLoader.getProperty("ELASTIC_HOST")
        self.ELASTIC_PORT = self.propertiesLoader.getProperty("ELASTIC_PORT")
        self.ELASTIC_DATA_HEADER_NAME = self.propertiesLoader.getProperty("ELASTIC_DATA_HEADER_NAME")
        self.logger.info("on Elastic -> properties initalized")

    # insert/update index in elastic with index and id values
    def putDataOnIndex(self,indexValue,obj,docId):
        try:
            self.logger.info("ELASTIC ==> updating document in index")
            print(json.dumps(obj))
            res = self.es.index(index=indexValue,body=json.dumps(obj),id = docId)
        except Exception as e:
            self.logger.error("ELASTIC ==> There was an error on inserting to index==>",e)
            res =self.getData(indexValue,docId)
            res = self.es.index(index=indexValue,body=json.dumps(res),id = docId)


    #check if the index exist and then get the doc with same id(which identify to which class its belong) and the index we want.
    # then we take the speicific part of the json which is the body to our model.
    def getData(self,indexValue,docId):
        result = None
        try:
            index_exists = self.es.indices.exists(index=indexValue)
            if(index_exists == True):
                res = self.es.get(index=indexValue,id = docId) 
                #equal to:
                # self.es.search(index=indexValue,body={"query":{ "ids":{ "values": [ docId ] } } })
                self.logger.info("ELASTIC ==> data of index: " + indexValue + " with id: " + docId + " is: " + str(res))
                result = res[self.ELASTIC_DATA_HEADER_NAME]
        except Exception as e:
            self.logger.error("ELASTIC ==> error on getting index data from Elastic")
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