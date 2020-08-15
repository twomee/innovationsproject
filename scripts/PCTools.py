import pathlib
import threading
from logConfig import Log
from clipboard import ClipBoard
from keysListner import KeysListnerObject
from sensorTemp import temperature
from DateManager import DateManager
from redisDB import redisDB
# from .Project import keyboardMouseListener






def main():
    logger = Log.configureLogger() 

    # absPath = pathlib.Path().absolute()
    # print(absPath)
    dateManager = DateManager()
    r = redisDB()
    klo = KeysListnerObject(logger,dateManager,r)
    t = temperature(logger,dateManager,r)
    cb = ClipBoard(logger,dateManager,r)

    threading.Thread(target=klo.run, args=[]).start()
    threading.Thread(target=t.cpuTemp, args=[]).start()
    # threading.Thread(target=cb.copyFromClipBoard, args=[]).start()

main()
