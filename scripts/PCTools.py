import pathlib
import threading
from logConfig import Log
from clipboard import ClipBoard
from keysListner import KeysListnerObject
from sensorTemp import temperature
from DateManager import DateManager
from redisDB import redisDB
from elastic import Elastic
from mongoDB import mongoDB
import queue
# from .Project import keyboardMouseListener






def main():
    logger = Log.configureLogger() 
    q = queue.Queue()

    # absPath = pathlib.Path().absolute()
    # print(absPath)
    dateManager = DateManager()
    r = redisDB()
    e = Elastic(logger)
    m = mongoDB(logger)
    klo = KeysListnerObject(logger,dateManager,r,q,e,m)
    t = temperature(logger,dateManager,r,q,e)
    cb = ClipBoard(logger,dateManager,r,q,e,m)

    threading.Thread(target=klo.run, args=[]).start()
    threading.Thread(target=t.cpuTemp, args=[]).start()
    threading.Thread(target=cb.copyFromClipBoard, args=[]).start()

main()
