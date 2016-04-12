from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QPushButton,
    QVBoxLayout,QWidget,QLCDNumber,QListWidget,QListWidgetItem)
import time
import threading
import pickle
import pdb

class PowerRecord(QWidget):
    """docstring for PowerRecord"""
    def __init__(self):
        super(PowerRecord, self).__init__()
        # self.arg = arg
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update())
        # self.timer.start(100)

        self.startTime = 0
        self.stopTime = time.time()
        self.userID = 'lidingke'
        self.pick = list()
        self.itemShowNum = 5
        self.itemChangeStatus = False
        self.loadFile()
        self.UI_init()
        self.plantlist()
        # self.initItemText()

    def UI_init(self):
        self.seButton = QPushButton('start')
        self.seButton.clicked.connect(self.startOrStop)
        # self.hourlabel = QLabel('时')
        # self.hourShow = QLCDNumber()
        # self.minlabel = QLabel('分')
        # self.minShow = QLCDNumber()
        # self.seclabel = QLabel('秒')
        self.secShow = QLCDNumber()
        self.secShow.setNumDigits(10)
        self.secShow.display('00:00:00')
        self.historylist = QListWidget()
        for x in range(0,self.itemShowNum):
            item = QListWidgetItem()
            self.historylist.addItem(item)
            # pdb.set_trace()
        self.historylist.itemSelectionChanged.connect(self.itemSelect)

        # item.setText('kklong')
        # item = QListWidgetItem()
        # self.historylist.addItem(item)
        # item = QListWidgetItem()
        # self.historylist.addItem(item)
        # self.historylist.setReadOnly(True)
        timebox = QHBoxLayout()

        # timebox.addWidget(self.hourlabel)
        # timebox.addWidget(self.hourShow)
        # timebox.addWidget(self.minlabel)
        # timebox.addWidget(self.minShow)
        # timebox.addWidget(self.seclabel)
        buttonarea = QVBoxLayout()

        self.printbutton = QPushButton('print')
        self.printbutton.clicked.connect(self.printPDF)
        buttonarea.addWidget(self.printbutton)
        buttonarea.addStretch()

        timebox.addWidget(self.secShow)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.seButton, 0, 0)
        mainLayout.addLayout(timebox, 0, 1)
        mainLayout.addWidget(self.historylist, 1,1)
        mainLayout.addLayout(buttonarea, 1, 0)
        # mainLayout.addLayout(buttonLayout2, 2, 1)
        # self.loadFile()
        self.setLayout(mainLayout)
        # self.setWindowTitle("Simple Address Book")

###

###

    def initItemText(self):
        self.itemText = self.historylist.item(0).text()

    def itemSelect(self):
        self.itemText = self.historylist.currentItem().text()
        self.itemChangeStatus = True
        print(self.itemText)

    def printPDF(self):
        if self.itemChangeStatus is False:
            self.itemText = self.historylist.item(0).text()
        print('print:',self.itemText)

    def loadFile(self):
        try:
            with open('usertask.pickle','rb') as f:
                self.pick = pickle.load(f)
                f.close()
        except FileNotFoundError:
            newfile = open('usertask.pickle','wb')
            self.pick = list()
            pickle.dump(self.pick,newfile)
            newfile.close()
            # self.loadFile()
        except EOFError :
            pass

        except Exception as e:
            raise e


    def saveFile(self):
        try:
            with open('usertask.pickle','wb') as f:
                pickle.dump(self.pick,f)
                f.close()
        except Exception as e:
            raise e

    def plantlist(self):
        if len(self.pick) < self.itemShowNum:
            textlist = self.pick
        else:
            textlist = self.pick[-self.itemShowNum:]
        # pdb.set_trace()
        # self.historylist.clear()
        for i,x in enumerate(textlist):
            starttime = time.strftime('%H:%M:%S',time.gmtime(x.get('start')))
            stoptime = time.strftime('%H:%M:%S',time.gmtime(x.get('stop')))
            textstr = 'start:'+starttime+', stop:'+stoptime+', user:'+x.get('userID')
            # textstr = x['start']+':'+x['stop']+':'+x['userID']
            print(textstr)
            # for x in range(1,self.itemShowNum):
            #     pass
            # pdb.set_trace()
            if i < self.itemShowNum:
                item = self.historylist.item(self.itemShowNum-i-1)
                item.setText(textstr)
            # self.historylist.appendPlainText(textstr)
                # self.plaintlist.append(textstr)
            # if len(self.texlist) > 3:
            #     return

    def startOrStop(self):
        buttonState = self.seButton.text()
        if buttonState == 'start':
            print('start')
            self.startTime = time.time()
            self.seButton.setText('stop')
            threading.Thread(target=PowerRecord.timeStep,args=(self,)).start()

            # timeStep = time.clock() - self.startTime
        elif buttonState == 'stop':
            print('stop')
            self.pick.append({'start':self.startTime,
                'stop':self.stopTime,'userID':self.userID})
            self.saveFile()
            self.loadFile()
            self.plantlist()

            self.stopTime = time.time()
            self.seButton.setText('start')
            self.timebegin = False
            # print(timeStep)

    def timeStep(self):
        threadStartTime = time.clock()
        self.timebegin = True
        while self.timebegin:
            timeStep = time.clock() - threadStartTime
            # print(timeStep)
            timestr = time.strftime('%H:%M:%S',time.gmtime(timeStep))
            # print(timestr)
            self.secShow.display(timestr)
            self.update_GUI()
            time.sleep(1)

    def update_GUI(self):
        self.update()


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = PowerRecord()
    addressBook.show()

    sys.exit(app.exec_())
