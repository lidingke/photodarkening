import threading
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
import time

class MSG(QObject):
    """docstring for MSG"""
    signal = pyqtSignal(object)
    def __init__(self):
        super(MSG, self).__init__()
        QObject.__init__(self)

    def emit_MSG(self):
        print('emit')
        self.signal.emit('1')

    def run(self):
        while True:
            time.sleep(2)
            self.emit_MSG()

def pp(get):
    print('sc',get)


if __name__ == '__main__':
    s = MSG()
    # g = get()
    s.signal.connect(pp)
    s.run()
    # t = threading.Thread(target = s.run)
    # t.start()
