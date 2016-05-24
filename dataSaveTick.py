import threading
import time
# from modelpump import TempDetector
from PyQt5.QtCore import pyqtSignal

class DataSaveTick(threading.Thread):
    """docstring for DataSaveTick
    need a input dict which hold the dataqueue,
    pass the list to process and return a new list to get new data
    """
    result = pyqtSignal(object)
    def __init__(self,ticktime,dataGetDict):
        super(DataSaveTick, self).__init__()
        # self.arg = arg
        self.tick = ticktime
        self.dataGet = dataGetDict
        self.detector = TempDetector()

    def run(self):
        '''rewrite this run() for a clock
        pass datalist to proccess per steptime
        '''
        getlist = self.dataGet['dataGet']
        self.dataGet['dataGet'] = []
        if getlist:
            # powerdata = []
            self.factory(getlist)
        time.sleep(self.tick)

    def factory(self,getlist):
        datalist = []
        for x in getlist:
            # pass
            power = self.detector.hex2power(x[1])
            datalist.append([power,x[0],x[1]])
        datalist.sort()
        dataLen = len(datalist)
        powerresult = sum(datalist[1:dataLen-1])/(dataLen - 2)
        self.result.emit(powerresult)



