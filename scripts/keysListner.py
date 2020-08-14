from pynput import keyboard


class KeysListnerObject():

    def __init__(self,logger):
        self.logger = logger

    def on_press(self,key):
        try:
            self.logger.info('alphanumeric key {0} pressed'.format(
                key.char))
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

# Collect events until released
# if __name__ == '__main__':
#     klo = KeysListnerObject()
#     klo.run()