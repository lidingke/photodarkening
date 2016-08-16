
from frame.serialmodel import SerialModel
from model.lastlog import MsgSet
import time

class SlaveMode(SerialModel):
    """docstring for SlaveMode"""
    initPower = 0

    def __init__(self, ):
        super(SlaveMode, self).__init__()
        # self.arg = arg
        msgset = MsgSet()
        self.msgStr = msgset.msgDictStr

    def run(self):
        '''
        thread start function
        '''
        while self.running:
            if self.ser:
                data = self._decodeHeader()
                if data:
                    self._taskDistribution(data)
            time.sleep(self.timeout)

    def _decodeHeader(self):
        '''
                return without package
                input bit data analysis
        '''
        bitlist = list()
        while self.running:
            databit = self._readbit()
            if databit == b'\xeb':
                databit = self._readbit()
                if databit == b'\x90':
                    while True:
                        databit = self._readbit()
                        if databit == b'\x90':
                            databit = self._readbit()
                            data = b''.join(bitlist)
                            return data
                        bitlist.append(databit)

class Source(SlaveMode):
    """docstring for Source"""

    def __init__(self, ):
        super(Source, self).__init__()
        #seed
        self.pulseWidth = 0.1
        self.frequance = 0.1
        self.current = 0.1
        #isopen
        self.isSeedOpen = False
        self.isSeedLEDOpen = False

    def __powerMethod(self):
        self.initPower = self.initPower + \
            self.pulseWidth * self.frequance * self.current * 0.00001

    @_onoff
    def _taskDistribution(self, data):
        # decode and distribute task from decode data
        if self.isSeedOpen:
            if data[0:1] == b'\x01':
                # if data[1:2] == b'\x00':
                #     if data[3:4] == b'\x01':
                #         self.isSeedOpen = True
                #         msg = self.msgStr.get('openseedreturn')
                #         self._write(b''.fromhex(msg))
                #     elif data[3:4] == b'\x00':
                #         self.isSeedOpen = False
                #         msg = self.msgStr.get('closeseedreturn')
                #         self._write(b''.fromhex(msg))
                if data[1:2] == b'\x01':
                    valuebit = data[2:4]
                    self.current = int().from_bytes(valuebit, 'big')
                    print('self.current ',self.current)
                    returnvalue = self.msgStr.get('seedcurrentvaluesetreturn')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x02':
                    valuebit = data[2:4]
                    self.pulseWidth = int().from_bytes(valuebit, 'big')
                    print('self.pulseWidth ',self.current)
                    returnvalue = self.msgStr.get('seedpulsesetreturn')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x03':
                    valuebit = data[2:4]
                    self.frequance = int().from_bytes(valuebit, 'big')
                    print('self.frequance ',self.current)
                    returnvalue = self.msgStr.get('seedfreset')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x04':
                    returnvalue = self.msgStr.get('seedcurrentvaluegetreturn')
                    valuebit = self.current.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x05':
                    returnvalue = self.msgStr.get('seedpulsereadreturn')
                    valuebit = self.pulse.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
                elif data[1:2] == b'\x06':
                    returnvalue = self.msgStr.get('seedfrereadreturn')
                    valuebit = self.frequance.to_bytes(2, 'big')
                    returnvalue = returnvalue[0:3] + valuebit + returnvalue[5:8]
                    self._write(returnvalue)
            elif data[0:1] == b'\x02':
                if data[2:3] == b'\x05':
                    if data[4:5] == b'\x01':
                        self.isSeedLEDOpen = True
                    elif data[4:5] == b'\x00':
                        self.isSeedLEDOpen = False

    def _onoff(self, func):
        def check(self, data):
            if data[0:1] == b'\x01':
                if data[1:2] == b'\x00':
                    if data[3:4] == b'\x01':
                        self.isSeedOpen = True
                        msg = self.msgStr.get('openseedreturn')
                        self._write(b''.fromhex(msg))
                    elif data[3:4] == b'\x00':
                        self.isSeedOpen = False
                        msg = self.msgStr.get('closeseedreturn')
                        self._write(b''.fromhex(msg))
            return func(self, data)
        return checker
