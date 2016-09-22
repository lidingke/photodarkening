
from model.lastlog import MsgSet
from slave.source import SlaveMode
import random
import threading

def _onoff(func):
    def checker(self, data):
        if data[0:1] == b'\x02':
            if data[2:3] == b'\x0A':
                if data[3:5] == b'\x00\x01':
                    self.isFirstPumpOpen = True
                    print('first pump open')
                elif data[3:5] == b'\x00\x00':
                    self.isFirstPumpOpen = False
                    print('first pump close')
            elif data[2:3] == b'\x0B':
                if data[3:5] == b'\x00\x01':
                    self.isSecondPumpOpen = True
                    print('second pump open')
                elif data[3:5] == b'\x00\x00':
                    self.isSecondPumpOpen = False
                    print('second pump close')
        reselt = func(self, data)
        print('pump power', self.initPower)
        return reselt
    return checker


class Pump(SlaveMode):
    """docstring for Pump"""
    def __init__(self, ):

        super(Pump, self).__init__()
        self.port = 'com18'
        self.baundrate = 9600
        self.running = True
        # self.timeout = 120
        self.power1st = 0.1
        self.power2st = 0.1
        self.pumpPower1Set = 0.1
        self.pumpPower2Set = 0.1
        self.resultPower = 0
        #isopen
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False
        # self.daemon = False
        self.setPort(self.port, self.baundrate)
        threading.Thread(target=self._current2Send, daemon=True, ).start()

    def __powerMethod(self):
        self.power1st = self.initPower * self.pumpPower1Set
        self.power2st = self.power1st * self.pumpPower2Set
        self.resultPower = self.power2st + random.randint(0,10)
        return self.resultPower

    @_onoff
    def _taskDistribution(self, data):
        if self.isFirstPumpOpen:
            if data[0:1] == b'\x02':
                if data[2:3] == b'\x0A':
                    self.pumpPower1Set = int.from_bytes(data[3:5], 'big')# data[3:5].from_bytes(2, 'big')
                    # self.writeDataWithHead(data)
                    print('pumpPower1Set ', self.pumpPower1Set)
        if self.isSecondPumpOpen:
            if data[0:1] == b'\x02':
                if data[2:3] == b'\x0B':
                    self.pumpPower2Set = int.from_bytes(data[3:5], 'big')# data[3:5].to_bytes(2, 'big')
                    # self.writeDataWithHead(data)
                    print('pumpPower2Set ', self.pumpPower2Set)



    def sendCurrent(self):
        print('start sendCurrent')
        while True:
            if self.isSecondPumpOpen:
                self._write(self._current2Send())

    def _current2Send(self):
        power = self.__powerMethod()
        temp = (random.randint(20, 30) * 100).to_bytes(2, 'little')
        power = int(power).to_bytes(2, 'little')
        currentmsg = b'\x9A' + temp + b'\x01\x02' + power + b'\x05\x06\xFF\xFF\xA9'
        return currentmsg
