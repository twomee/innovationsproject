import pathlib
import threading
from logConfig import Log
from clipboard import ClipBoard
from keysListner import KeysListnerObject
from sensorTemp import temperature
from DateManager import DateManager
from redisDB import redisDB
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
    dateManager = DateManager()
    r = redisDB()
    cb = ClipBoard(logger,dateManager,r)
    klo = KeysListnerObject(logger,dateManager,r)
    t = temperature(logger,dateManager,r)


    t1 = threading.Thread(target=t.cpuTemp, args=[])
    t2 = threading.Thread(target=klo.run, args=[])
    t3 = threading.Thread(target=cb.copyFromClipBoard, args=[])
    t1.start()
    t2.start()
    t3.start()

main()
