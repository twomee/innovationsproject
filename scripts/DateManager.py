from datetime import datetime



class DateManager:
    def __init__(self):
        self.now = None

    #get the date of current moment
    def getDate(self):
        self.now = datetime.now()
        self.now  = self.now.strftime("%d/%m/%Y")
        return self.now

    def getDateWithoutSpecialCharsForElastic(self):
        self.now = datetime.now()
        self.now  = self.now.strftime("%d%m%Y")
        return self.now

    #check if the date we got from DB is valid as date which is the key for the data
    def validateIsDate(self,date):
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            return True
        except ValueError:
            return False




