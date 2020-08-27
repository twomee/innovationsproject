import os
import subprocess

class AudoModuleInstaller:

    def __init__(self,logger,propertiesLoader):
        self.logger = logger
        self.propertiesLoader = propertiesLoader
        self.initalizeProperties()

    def initalizeProperties(self):
        self.AUTO_MODULE_INSTALL_LINUX_COMMAND = self.propertiesLoader.getProperty("AUTO_MODULE_INSTALL_LINUX_COMMAND")
        self.logger.info("on AudoModuleInstaller -> properties initalized")

    def installMissingModules(self):
        result = subprocess.run([self.AUTO_MODULE_INSTALL_LINUX_COMMAND], stdout=subprocess.PIPE).stdout.decode(self.DECODE_TYPE).replace("\u00b0C\n", "")
        self.logger.info("installed all missing modules: ", result)