
from model.lastlog import MsgSet
from slave.source import SlaveMode
import random
import threading

class Pump(SlaveMode):
    """docstring for Pump"""
    def __init__(self, ):
        super(Pump, self).__init__()
        self.power1st = 0.1
        self.power2st = 0.1
        self.pumpPower1Set = 0.1
        self.pumpPower2Set = 0.1
        self.resultPower = 0
        #isopen
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False
        threading.Thread(target=self._current2Send, daemon=True, ).start()

    def __powerMethod(self):
        self.power1st = self.initPower * self.pumpPower1
        self.power2st = self.power1st * self.pumpPower2
        self.resultPower = self.power2st + random.random(0,10)
        return self.resultPower

    @_onoff
    def _taskDistribution(self, data):
        if self.isFirstPumpOpen:
            if data[0:1] == b'\x02':
                if data[2:3] == b'\x0A':
                    self.pumpPower1Set = data[3:5].to_bytes(2, 'big')
        if self.isSecondPumpOpen:
            if data[0:1] == b'\x02':
                if data[2:3] == b'\x0B':
                    self.pumpPower2Set = data[3:5].to_bytes(2, 'big')

    def _onoff(self, func):
        def checker(self, data):
            if data[0:1] == b'\x02':
                if data[2:3] == b'\x0A':
                    if data[3:5] == b'\x00\x01':
                        self.isFirstPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        self.isFirstPumpOpen = False
                elif data[2:3] == b'\x0B':
                    if data[3:5] == b'\x00\x01':
                        self.isSecondPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        self.isSecondPumpOpen = False
            return func(self, data)
        return checker

    def sendCurrent(self):
        while True:
            if self.isSecondPumpOpen:
                self._write(self._current2Send())

    def _current2Send(self):
        power = self.__powerMethod()
        temp = random.randint(20,30).to_bytes(2, 'little')*100
        power = int(power).to_bytes(2, 'little')
        currentmsg = b'\x9A'+ temp +'\x01\x02' + power +b'\x05\x06\xFF\xFF'+b'\xA9'
        return currentmsg
