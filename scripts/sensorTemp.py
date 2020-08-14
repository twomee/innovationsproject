import subprocess
import time

class temperature():

    def __init__(self,logger):
        self.logger = logger

    def cpuTemp(self):
        while True:
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            result = subprocess.run(['osx-cpu-temp'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\n", "")
            self.logger.info("CPU temperature is " + result)


# t = temperature()
# t.cpuTemp()