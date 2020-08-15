from pynput import keyboard

class KeysListnerObject():

    #init the vars, will contain dict which count the nubmers of times every char was pressed:
    #{'a':1,'b':2,'c':10,'d':0}
    def __init__(self,logger,dateManager,redis,queue):
        self.logger = logger
        self.dateManager =  dateManager
        self.r = redis
        self.queue = queue
        self.refreshDataFromRedisDB()

    #check if there is data in DB. if so, take the data and append the new data to the object. else, start new dict
    def refreshDataFromRedisDB(self):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            result = self.r.getValue(self.dateManager.getDate())
            self.alphabet = result
            self.logger.info("on KeyListener ->refreshDataFromRedisDB-> self.alphabet: ", self.alphabet)
            self.logger.info(self.alphabet)
        else:
            self.alphabet = {}

    #take every key that presses and insert him to dict object which mapping the chars.
    def on_press(self,key):
        try:
            self.logger.info('alphanumeric key {0} pressed'.format(
                key.char))
            self.insertToDict(key)

            self.updateDBValues()

        except AttributeError:
            self.logger.error('special key {0} pressed'.format(
                key))
    
    #check which key was released after he pressed. not recorded on DB.
    def on_release(self,key):
        self.logger.info('{0} released'.format(key))
        # if key == keyboard.Key.esc:
        #     # Stop listener
        #     return False

    #run the listener of the keys
    def run(self):
        with keyboard.Listener( 
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    #insert the new data to the dict
    def insertToDict(self,key):
        if(self.r.isKeyExists(self.dateManager.getDate())):
            previousData = self.r.getValue(self.dateManager.getDate())
            self.alphabet = previousData
            self.logger.warning("!!!!!!!!!!!!!!!!!previousData :", self.alphabet )
            self.logger.warning(self.alphabet )
            if(key.char in self.alphabet):
                self.alphabet[key.char] = self.alphabet[key.char] + 1
            else:
                self.alphabet[key.char] = 1
            self.queue.put(self.alphabet)
        else:
            self.alphabet = {}
        

    #insert and update the dict object on DB where the key is date.
    def updateDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDate(),
                                self.queue)
        self.logger.info("on KeyListener ->updateDBValues-> self.alphabet: ", self.alphabet)
        self.logger.info(self.alphabet)


# Collect events until released
# if __name__ == '__main__':
#     klo = KeysListnerObject()
#     klo.run()