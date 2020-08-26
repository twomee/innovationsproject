from datetime import datetime



class DateManager:

    def __init__(self,logger,propertiesLoader):
        self.now = None
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()


    def initalizeProperties(self):
        self.GET_DATE_FORMAT = self.propertiesLoader.getProperty("GET_DATE_FORMAT")
        self.GET_DATE_WITHOUT_SPECIAL_CHARS_FORMAT = self.propertiesLoader.getProperty("GET_DATE_WITHOUT_SPECIAL_CHARS_FORMAT")
        self.logger.info("on DateManager -> properties initalized")

    #get the date of current moment
    def getDate(self):
        self.now = datetime.now()
        self.now  = self.now.strftime(self.GET_DATE_FORMAT)
        return self.now

    def getDateWithoutSpecialCharsForElastic(self):
        self.now = datetime.now()
        self.now  = self.now.strftime(self.GET_DATE_WITHOUT_SPECIAL_CHARS_FORMAT)
        return self.now

    #check if the date we got from DB is valid as date which is the key for the data
    def validateIsDate(self,date):
        try:
            datetime.datetime.strptime(date, self.GET_DATE_FORMAT)
            return True
        except ValueError:
            return False

    #check if the date we got from DB is valid as date which is the key for the data
    def validateIsDateWithoutSpecialCharsForElastic(self,date):
        try:
            datetime.datetime.strptime(date, self.GET_DATE_WITHOUT_SPECIAL_CHARS_FORMAT)
            return True
        except ValueError:
            return False




