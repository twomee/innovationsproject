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
from PropertiesLoader import PropertiesLoader
from AudoModuleInstaller import AudoModuleInstaller
# from .Project import keyboardMouseListener

PROPERTIES_FILE_NAME = "scripts/appconfig.ini"




def main():
    logger = Log.configureLogger() 
    propertiesLoader = PropertiesLoader(logger)
    propertiesLoader.loadProperties(PROPERTIES_FILE_NAME)
    moduleInstaller = AudoModuleInstaller(logger,propertiesLoader)
    moduleInstaller.installMissingModules()
    q = queue.Queue()


    # absPath = pathlib.Path().absolute()
    # print(absPath)
    dateManager = DateManager(logger,propertiesLoader)
    r = redisDB(logger)
    e = Elastic(logger,propertiesLoader)
    m = mongoDB(logger,propertiesLoader)
    klo = KeysListnerObject(logger,dateManager,r,q,e,m,propertiesLoader)
    t = temperature(logger,dateManager,r,q,e,m,propertiesLoader)
    cb = ClipBoard(logger,dateManager,r,q,e,m,propertiesLoader)

    threading.Thread(target=klo.run, args=[]).start()
    threading.Thread(target=t.cpuTemp, args=[]).start()
    threading.Thread(target=cb.copyFromClipBoard, args=[]).start()

main()
