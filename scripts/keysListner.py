from pynput import keyboard

class KeysListnerObject():

    def __init__(self,logger,dateManager,redis):
        self.logger = logger
        self.dateManager =  dateManager
        self.r = redis
        self.refreshDataFromRedisDB()


    def on_press(self,key):
        try:
            self.logger.info('alphanumeric key {0} pressed'.format(
                key.char))
            self.insertToDict(key)
            self.updatreDBValues()

        except AttributeError:
            self.logger.error('special key {0} pressed'.format(
                key))

    def on_release(self,key):
        self.logger.info('{0} released'.format(key))
        # if key == keyboard.Key.esc:
        #     # Stop listener
        #     return False

    def run(self):
        with keyboard.Listener( 
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def insertToDict(self,key):
        if(key.char in self.alphabet):
            self.alphabet[key.char] = self.alphabet[key.char] + 1
        else:
            self.alphabet[key.char] = 1
        
    def refreshDataFromRedisDB(self):
        result = self.r.getValue(self.dateManager.getDateAndTime())
        if(result is None):
            self.alphabet = {}
        else:
            self.alphabet = result

    def updatreDBValues(self):
        self.r.setTransactionalValue(self.dateManager.getDateAndTime(),
                                self.alphabet)

# Collect events until released
# if __name__ == '__main__':
#     klo = KeysListnerObject()
#     klo.run()