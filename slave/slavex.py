

from frame.serialmodel import SerialModel
import time
import threading

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
                data = self.analysisbit()
                if data :
                    self._coreMsgProcess(data)


    def _sendCurrent(self):
        while True:
            if self.status == 'open':
                self._write(b'open')
                time.sleep(1)
            else:
                time.sleep(1)


    def analysisbit(self):
        bitlist = list()
        while True:
            databit = self._readBit()
            if databit == b'\x9A':
                tick = 1
                while True:
                    tick = tick + 1
                    databit = self.readbit(self.ser)
                    if databit == b'\xA9':
                        if tick == 12:
                            data = b''.join(bitlist)
                            return b'\x9A' + data +b'\xA9'
                        else:
                            print('位数errror')
                            return b'0'
                    bitlist.append(databit)

    def _coreMsgProcess(self):
        pass

if __name__ == '__main__':
    s = SlaveX()
    s.start()
