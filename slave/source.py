
from frame.serialmodel import SerialModel
from model.lastlog import MsgSet
from slave.set import SourcePowerPara
import time
import pdb

class SlaveMode(SerialModel):
    """docstring for SlaveMode"""
    # sharedPower = 0

    def __init__(self, ):
        super(SlaveMode, self).__init__()
        # self.arg = arg
        msgset = MsgSet()
        self.msgHex = msgset.msgDictHex
        # self.initPower = 0
        self.timeout = 0.1
        self.outPutPower = 0
        self.SETSPP = SourcePowerPara()
        # self.SETSPP.POWER = sp.POWER

    def run(self):
        '''
        thread start function
        '''
        # print('is source self running', self.running, self.ser)
        while self.running:
            try:
                if self.ser:
                    data = self._decodeHeader()
                    # print('get data', data)
                    if data:
                        self._taskDistribution(data)
                        self._powerMethod()
                        # print('power', self.initPower)
                    # print(' after data')
                        # print('sharedpower', id(self.SETSPP.POWER),self.SETSPP.POWER)
                time.sleep(self.timeout)
            except Exception as e:
                raise e

        # print('is source self running', self.running, self.ser)

    def _taskDistribution(self,data):
        pass

    def _decodeHeader(self):
        '''
                return without package
                input bit data analysis
        '''
        bitlist = list()
        while self.running:
            databit = self._readBit()
            if databit == b'\xeb':
                databit = self._readBit()
                if databit == b'\x90':
                    while True:
                        databit = self._readBit()
                        if databit == b'\x90':
                            databit = self._readBit()
                            data = b''.join(bitlist)
                            return data
                        bitlist.append(databit)

    def _powerMethod(self):
        pass

    def writeDataWithHead(self, data):
        self._write(b'\xeb\x90' + data + b'\x90\xeb')

def _onoff(func):
    def check(self, data):
        if data[0:1] == b'\x01':
            if data[1:2] == b'\x00':
                if data[2:4] == b'\x00\x01':
                    self.isSeedOpen = True
                    msg = self.msgHex.get('openseedreturn')

                    self._write(msg)
                elif data[2:4] == b'\x00\x00':
                    self.isSeedOpen = False
                    # self.SETSPP.POWER = 0
                    msg = self.msgHex.get('closeseedreturn')
                    self._write(msg)
                print('seed open', self.isSeedOpen)
        result = func(self, data)
        print('source power', self.SETSPP.POWER)
        return result
    return check

class Source(SlaveMode):
    """docstring for Source"""

    def __init__(self, ):

        super(Source, self).__init__()
        #seed
        self.port = 'com16'
        self.running = True
        self.baundrate = 9600
        self.pulseWidth = 0.1
        self.frequance = 0.1
        self.current = 0.1
        #isopen
        self.isSeedOpen = False
        self.isSeedLEDOpen = False
        # self.daemon = False
        # self.timeout = 120
        self.powerMethodList = []
        self.initPower = 0
        # self.outPutPower = self.SETSPP.POWER
        self.setPort(self.port, self.baundrate)


    def _powerMethod(self,):
        # pdb.set_trace()
        if self.isSeedOpen == True:
            powerMethodList = [self.initPower, \
                self.pulseWidth, self.frequance, self.current]
            if self.powerMethodList != powerMethodList:
                self.powerMethodList = powerMethodList
                self.SETSPP.POWER = self.initPower + \
                    self.pulseWidth * self.frequance * self.current * 0.000000001
                print('SLAVE_POWERS:', self.initPower, \
                    self.pulseWidth, self.frequance, self.current, self.SETSPP.POWER)
                # print(self.SETSPP.POWER)
        else:
            print('seed close set power zero',self.isSeedOpen)
            self.initPower = 0
            self.pulseWidth = 0
            self.frequance = 0
            self.current = 0
            self.SETSPP.POWER = 0

    # def setSourceOutputPower(self, power):



    @_onoff
    def _taskDistribution(self, data):
        # decode and distribute task from decode data
        if self.isSeedOpen:
            if data[0:1] == b'\x01':
                if data[1:2] == b'\x01':
                    valuebit = data[2:4]
                    self.current = int().from_bytes(valuebit, 'big')
                    print('self.current ',self.current)
                    returnvalue = self.msgHex.get('seedcurrentvaluesetreturn')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x02':
                    valuebit = data[2:4]
                    self.pulseWidth = int().from_bytes(valuebit, 'big')
                    print('self.pulseWidth ',self.pulseWidth)
                    returnvalue = self.msgHex.get('seedpulsesetreturn')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x03':
                    valuebit = data[2:4]
                    self.frequance = int().from_bytes(valuebit, 'big')
                    print('self.frequance ',self.frequance)
                    returnvalue = self.msgHex.get('seedfreset')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x04':
                    returnvalue = self.msgHex.get('seedcurrentvaluegetreturn')
                    valuebit = self.current.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x05':
                    returnvalue = self.msgHex.get('seedpulsereadreturn')
                    valuebit = self.pulseWidth.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x06':
                    returnvalue = self.msgHex.get('seedfrereadreturn')
                    valuebit = self.frequance.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:4] + valuebit + returnvalue[6:8]
                    self._write(returnvalue)
            elif data[0:1] == b'\x02':
                if data[2:3] == b'\x05':
                    if data[4:5] == b'\x01':
                        self.isSeedLEDOpen = True
                    elif data[4:5] == b'\x00':
                        self.isSeedLEDOpen = False


