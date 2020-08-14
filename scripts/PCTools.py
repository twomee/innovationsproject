import pathlib
import threading
from logConfig import Log
from clipboard import ClipBoard
from keysListner import KeysListnerObject
from sensorTemp import temperature
# from .Project import keyboardMouseListener
logger = Log.configureLogger()






def main():
    # Configure the logger
    # loggerConfigFileName: The name and path of your configuration file

    # Create the logger
    # Admin_Client: The name of a logger defined in the config file

    logger.info('This is an information message')

    absPath = pathlib.Path().absolute()
    print(absPath)
    cb = ClipBoard(logger)
    klo = KeysListnerObject(logger)
    t = temperature(logger)
    # result = t.cpuTemp()
    # klo.run()
    # cb.copyFromClipBoard()
    t1 = threading.Thread(target=t.cpuTemp, args=[])
    t2 = threading.Thread(target=klo.run, args=[])
    t3 = threading.Thread(target=cb.copyFromClipBoard, args=[])
    t1.start()
    t2.start()
    t3.start()

main()
