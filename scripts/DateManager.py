from datetime import datetime



class DateManager:
    def __init__(self):
        self.now = None

    def getDateAndTime(self):
        self.now = datetime.now()
        self.now  = self.now.strftime("%d/%m/%Y")
        return self.now

    def validateIsDate(self,date):
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            return True
        except ValueError:
            return False




