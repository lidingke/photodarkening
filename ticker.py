from PyQt5.QtWidgets import (QVBoxLayout,QLineEdit,QLCDNumber,QPushButton,QWidget)
from    PyQt5.QtCore        import QObject, QTime, QDateTime, pyqtSignal
import threading
import time

class Ticker(QLCDNumber,threading.Thread):
    """docstring for Ticker"""

    timeOut = pyqtSignal()

    def __init__(self,):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        super(Ticker, self).__init__()
        # self.arg = arg
        self.daemon = True
        self.setNumDigits(10)
        self.display('00:00:00')
        self.startStatus = False
        self.startTime = 0
        self.timeLimit = -1

    def run(self):
        while True:
            time.sleep(0.3)
            # print(time.clock())
            if self.startStatus:
                timeStep = time.clock() -self.startTime
                gmTimeStep = time.gmtime(timeStep)
                timestr = time.strftime('%H:%M:%S', gmTimeStep)
                self.display(timestr)
                if self.timeLimit != -1:
                    if timeStep > self.timeLimit:
                        self.timeOut.emit()
                        self.startStatus = False
            # else:
            #     pass


    def startTick(self, sec ):
        self.startStatus = True
        self.startTime = time.clock()
        self.timeLimit = sec

    def stopTick(self):
        self.startStatus = False


class Record(QWidget):
    """docstring for Record"""
    def __init__(self):
        super(Record, self).__init__()
        # self.arg = arg
        self.seButton = QPushButton('begin')
        self.seButton.buttonState = 'begin'
        self.seButton.clicked.connect(self.beginOendTime)
        self.ticker = Ticker()
        self.ticker.start()
        self.lineedit = QLineEdit()
        buttonarea = QVBoxLayout()
        buttonarea.addWidget(self.seButton)
        buttonarea.addWidget(self.ticker)
        buttonarea.addWidget(self.lineedit)
        self.setLayout(buttonarea)

    def beginOendTime(self):
        # self.ticker.run()
        if self.seButton.buttonState == 'begin':
            # pass
            self.ticker.startTick()
            self.seButton.setText('stop')
            self.seButton.buttonState = 'stop'
        elif self.seButton.buttonState == 'stop':
            self.ticker.stopTick()
            self.seButton.setText('begin')
            self.seButton.buttonState = 'begin'


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = Record()
    addressBook.show()

    sys.exit(app.exec_())
