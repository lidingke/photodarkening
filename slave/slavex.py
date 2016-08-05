from frame.serialmodel import SerialModel
import time
import threading
import random

class SlaveX(SerialModel):
    """docstring for SlaveX"""

    def __init__(self, ):
        super(SlaveX, self).__init__()
        # self.arg = arg
        self.status = 'open'
        self.currentIndex = 0
        self.port = 'com13'
        threading.Thread(target = self._sendCurrent, daemon = True)

    def run(self):
        while True:
            if self.ser:
                data = self._analysisbit()
                if data :
                    self._coreMsgProcess(data)


    def _sendCurrent(self):
        while True:
            if self.status == 'open':
                self._write(b'open')
                time.sleep(1)
            else:
                time.sleep(1)


    def _analysisbit(self):
        bitlist = list()
        while True:
            databit = self._readbit(self.ser)
            if databit == b'\xeb':
                databit = self._readbit(self.ser)
                if databit == b'\x90':
                    while True:
                        databit = self._readbit(self.ser)
                        if databit == b'\x90':
                            databit = self._readbit(self.ser)
                            data = b''.join(bitlist)
                            return data
                        bitlist.append(databit)
            elif databit == b'\x9A':
                while True:
                    databit = self._readbit(self.ser)
                    if databit == b'\xA9':
                        data = b''.join(bitlist)
                        return b'\x9A' + data +b'\xA9'
                    else:
                        return b'0'
                    bitlist.append(databit)

    def _coreMsgProcess(self, data):
        #todo
        #open platform
        #close platform
        #'opensecondpump':                   ' EB 90 02 00 0B 00 01 90 EB',
        #'closesecondpump':                  ' EB 90 02 00 0B 00 00 90 EB',
        #set current
        #'setsecondcurrent':                    ' EB 90 02 01 0B FF FF 90 EB',
        if data[0:1] == b'\x02':
            if data[1:2] == b'\x01':
                if data[4:5] == b'\x01':
                    self.status = 'open'
                elif data[4:5] == b'\x01':
                    self.status = 'close'
                # self.status = False
            elif data[1:2] == b'\x02':
                self.current =  int().from_bytes(data[3:5],'little')
                #current

        pass

    def _currentMsg(self):
        tp = self._randomCurrent()
        return b'\x9A' + b''.join(tp) +b'\xA9'

    def _randomCurrent(self):
        temp1 = int(100*(23 + random.uniform(2,10))).to_bytes(2, 'little')
        temp2 = int(100*(24 + random.uniform(2,10))).to_bytes(2, 'little')
        power1 =  int(100*(self.current * random.uniform(2,10))).to_bytes(2, 'little')
        power2 =  int(100*(self.current * random.uniform(2,10))).to_bytes(2, 'little')
        return (temp1, temp2, power1, power2)

if __name__ == '__main__':
    s = SlaveX()
    s.start()
