from jproperties import Properties

class PropertiesLoader:
    def __init__(self,logger):
        self.configs = Properties()
        self.logger = logger

    def loadProperties(self,propertiesFileName):
        with open(propertiesFileName, 'rb') as config_file:
            self.configs.load(config_file)
            self.logger.info("Properties file " + str(propertiesFileName) + "has been loaded to the code")

    #get the property name. return structure of tuple, getting the property name from data field
    def getProperty(self,propertyName):
        try:
            result = self.configs.get(propertyName).data
            return result
        except KeyError as ke:
            self.logger.error("the property has not found: ",ke)