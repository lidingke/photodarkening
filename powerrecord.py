from PyQt5.QtWidgets import (QTimeEdit,QDateTimeEdit , QGridLayout, QHBoxLayout, QPushButton,
    QVBoxLayout,QWidget,QLCDNumber,QListWidget,QListWidgetItem)
from PyQt5.QtCore import (QTime, QDateTime, QDate ,pyqtSignal)

from reportDialog import ReportDialog
import time
import threading
import pickle
import pdb
import queue
from pdfcreater import PdfCreater
from ticker import Ticker
from toolkit import WRpickle



class PowerRecord(QWidget):
    """docstring for PowerRecord"""
    '''在这里加个pick process'''
    beginTimeSignal = pyqtSignal(object)
    sqlTableName = pyqtSignal(object)
    stopSavePower = pyqtSignal(object)
    timeStateSignal = pyqtSignal(object)
    logStateSignal = pyqtSignal(object)

    def __init__(self):
        super(PowerRecord, self).__init__()
        self.wrpick = WRpickle('data\\reportLast.pickle')
        # self.pickContext = self.wrpick.loadPick()
        self.startTime = 0
        self.stopTime = time.time()
        self.userID = ''
        self.powerData = queue.Queue()
        self.pick = list()
        self.itemShowNum = 4
        self.itemChangeStatus = False
        self.timeStepPause = False
        self.pdfItem = dict()
        self.figGet = None
        self.timebegin = True
        self.loadFile()
        self.UI_init()
        self.plantlist()
        # with open('template.qss') as t:
        #     self.setStyleSheet(t.read())
        # self.initItemText()
        # self.arg = arg
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update())
        # self.timer.start(100)

    def UI_init(self):
        self.seButton = QPushButton('begin')
        self.seButton.buttonState = 'begin'
        self.seButton.clicked.connect(self.beginOendTime)
        self.timeEdit = QDateTimeEdit()
        self.timeEdit.setDisplayFormat(' s : hh : mm')
        # self.timeEdit.setDate(QDate(2000,10,10))
        # print(self.timeEdit.text())
        self.ticker = Ticker()
        self.ticker.start()
        self.ticker.timeOut.connect(self.tickerTimeOut)
        # self.ticker.setNumDigits(10)
        # self.ticker.display('00:00:00')
        self.historylist = QListWidget()
        self.historylist.setCurrentRow(1)
        for x in range(0,self.itemShowNum):
            item = QListWidgetItem()
            self.historylist.addItem(item)
        self.historylist.itemSelectionChanged.connect(self.itemSelect)
        buttonarea = QVBoxLayout()
        self.printbutton = QPushButton('print')
        self.printbutton.clicked.connect(self.printPDF)
        buttonarea.addWidget(self.seButton)
        buttonarea.addWidget(self.timeEdit)
        buttonarea.addWidget(self.printbutton)
        buttonarea.addStretch()
        buttonarea.addWidget(self.ticker)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.historylist, 0,1)
        mainLayout.addLayout(buttonarea, 0, 0)
        self.setLayout(mainLayout)




###

###

    def initItemText(self):
        self.itemText = self.historylist.item(0).text()

    def itemSelect(self):
        self.itemText = self.historylist.currentItem().text()
        self.itemNum = self.historylist.currentRow()
        # print(self.itemNum)
        pickget = self.pick[-self.itemNum-1]
        self.startTimetic = pickget.get('begin')
        self.printUserID = pickget.get('userID')
        print('itemSelect:',self.itemNum, self.startTimetic,self.printUserID)
        self.itemChangeStatus = True
        # print(self.itemText)

    def printPDF(self):
        self.getDbdata()
        if self.figGet:
            self.figGet.savePlotFig()
        rep = ReportDialog()
        rep.exec_()

        printer = PdfCreater(self,)
        printer.saveToFile()
        printer.savePdf()

        # if self.itemChangeStatus is False:
        #     self.itemText = self.historylist.item(0).text()
        # print('print:',self.itemText)
        # self.pdfItem['']

    def getNowFig(self,fig):
        self.figGet = fig


    def NowContextGet(self):
        #get last log
        self.pickContext = self.wrpick.loadPick()
        #get username
        self.pickContext['worker'] = self.userID
        #get plot from db
        #get calc report
        pass


    def beginOendTime(self):
        # self.ticker.run()
        if self.seButton.buttonState == 'begin':
            #记录起始时间
            self.beginTime = time.time()
            print('beginTime:',self.beginTime)
            self.beginTimeSignal.emit(self.beginTime)
            self.stopSavePower.emit(True)
            #begin ticker
            self.timeLong = self.timeEdit2time()
            #send to plot
            self.ticker.startTick(self.timeLong)
            self.timeStateSignal.emit(self.timeLong)
            self.logStateSignal.emit(True)
            self.seButton.setText('stop')
            self.seButton.buttonState = 'stop'
        elif self.seButton.buttonState == 'stop':
            self.ticker.stopTick()
            self.seButton.setText('begin')
            self.seButton.buttonState = 'begin'
            self.stopSavePower.emit(False)

    def tickerTimeOut(self):
        print('time out')
        self.seButton.setText('begin')
        self.seButton.buttonState = 'begin'
        self.stopSavePower.emit(False)

    def timerSave(self):
        beginTime =self.beginTime
        continueTime = self.editTime
        self.pick.append({'begin':beginTime,
            'continue':continueTime,'userID':self.userID})
        self.saveFile()
        self.loadFile()
        self.plantlist()

        self.stopTime = time.time()
        self.seButton.setEnabled(True)
        self.stopSavePower.emit(False)
        # self.seButton.setText('start')
        # self.timebegin = False
    def timeEdit2time(self):
        timeStr = self.timeEdit.text()
        timeSplit = timeStr.split(':')
        date = int(timeSplit[0].strip())
        hour = int(timeSplit[1].strip())
        minute = int(timeSplit[2].strip())
        return ((date*24+hour)*60+minute)*60

    def update_GUI(self):
        self.update()

###
# interface
###

    def getUserID(self):
        return self.userID

    def setUserID(self,userid):
        self.userID = userid

    def getPowerData(self):
        return self.powerData

    def setPowerData(self,data):
        self.powerData.put(data)



    def getDbdata(self):
        if self.itemChangeStatus is False:
            self.itemText = self.historylist.item(0).text()
            self.itemNum = 0
            pickget = self.pick[-self.itemNum-1]
            self.startTimetic = pickget.get('begin')
            self.printUserID = pickget.get('userID')
            print('num,pick:',self.itemNum, self.startTimetic)
            print('print:',self.itemText)
        localTime = self.startTimetic
        username = self.userID
        localTime = str(int(localTime))
        tableName='TM'+localTime+'US'+username
        self.sqlTableName.emit(tableName)


    def loadFile(self):
        try:
            with open('data\\usertask.pickle','rb') as f:
                self.pick = pickle.load(f)
                f.close()
        except FileNotFoundError:
            newfile = open('data\\usertask.pickle','wb')
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
            with open('data\\usertask.pickle','wb') as f:
                pickle.dump(self.pick,f)
                f.close()
        except Exception as e:
            raise e

    def plantlist(self):
        if len(self.pick) < self.itemShowNum:
            textlist = self.pick
        else:
            textlist = self.pick[-self.itemShowNum:]
        for i,x in enumerate(textlist):
            if x.get('start',False) is not False:
                pass
                starttime = time.strftime('%H:%M:%S',time.gmtime(x.get('start')))
                stoptime = time.strftime('%H:%M:%S',time.gmtime(x.get('stop')))
                textstr = 'start:'+starttime+', stop:'+stoptime+', user:'+x.get('userID')
            elif x.get('begin',False) is not False:
                begin = time.strftime('%H:%M:%S',time.gmtime(x.get('begin')))
                con = x.get('continue').toString()
                textstr = 'begin:' + begin + ', cont:' + con + ', user:'+x.get('userID')
            if i < self.itemShowNum:
                item = self.historylist.item(self.itemShowNum-i-1)
                item.setText(textstr)

        # pdb.set_trace()
        # self.itemSelect()
        # self.timeEdit.setMaximumTime()
        # self.hourlabel = QLabel('时')
        # self.hourShow = QLCDNumber()
        # self.minlabel = QLabel('分')
        # self.minShow = QLCDNumber()
        # self.seclabel = QLabel('秒')

        # item.setText('kklong')
        # item = QListWidgetItem()
        # self.historylist.addItem(item)
        # item = QListWidgetItem()
        # self.historylist.addItem(item)
        # self.historylist.setReadOnly(True)
        # timebox = QHBoxLayout()

        # timebox.addWidget(self.hourlabel)
        # timebox.addWidget(self.hourShow)
        # timebox.addWidget(self.minlabel)
        # timebox.addWidget(self.minShow)
        # timebox.addWidget(self.seclabel)

        # self.printbutton.clicked.connect(self.getDbdata)

        # timebox.addWidget()

        # mainLayout.addWidget(, 0, 0)
        # mainLayout.addLayout(timebox, 2, 0)

        # mainLayout.addLayout(buttonLayout2, 2, 1)
        # self.loadFile()

        # self.setWindowTitle("Simple Address Book")

    # def timerStep(self):
    #     threadStartTime = time.clock()
    #     while self.timebegin:
    #         timeStep = time.clock() - threadStartTime
    #         gmTimeStep = time.gmtime(timeStep)
    #         # print(timeStep)
    #         timestr = time.strftime('%H:%M:%S', gmTimeStep)
    #         # print(timestr)
    #         if self.editTime:
    #             # pdb.set_trace()
    #             nowQtime = QTime(gmTimeStep.tm_hour,gmTimeStep.tm_min)
    #             if (self.editTime.minute() == nowQtime.minute())\
    #                 and (self.editTime.hour() == nowQtime.hour()):
    #                 print('timeget')
    #                 self.timerSave()
    #                 self.timeStepPause = True
    #             if self.timeStepPause is True:
    #                 threadStartTime = time.clock()
    #             # print('st:',self.editTime,':',nowQtime)
    #         self.ticker.display(timestr)
    #         self.update_GUI()
    #         time.sleep(0.3)




    # def startOrStop(self):
    #     buttonState = self.seButton.text()
    #     if buttonState == 'start':
    #         print('start')
    #         self.startTime = time.time()
    #         self.seButton.setText('stop')
    #         threading.Thread(target=PowerRecord.timeStep,args=(self,)).start()

    #         # timeStep = time.clock() - self.startTime
    #     elif buttonState == 'stop':
    #         print('stop')
    #         self.pick.append({'start':self.startTime,
    #             'stop':self.stopTime,'userID':self.userID})
    #         self.saveFile()
    #         self.loadFile()
    #         self.plantlist()

    #         self.stopTime = time.time()
    #         self.seButton.setText('start')
    #         self.timebegin = False
    #         # print(timeStep)
        # beginTime = time.strftime('%H:%M:%S', time.gmtime(self.beginTime) )

        # pdb.set_trace()
        # continueTime = 1
        # pdb.set_trace()
        # print(continueTime)
        # self.pick.append({'start:':beginTime,
        #     'stop':continueTime,'userID':self.userID,})




    # def timeStep(self):
    #     threadStartTime = time.clock()
    #     # self.timebegin = True
    #     while self.timebegin:
    #         timeStep = time.clock() - threadStartTime
    #         # print(timeStep)
    #         timestr = time.strftime('%H:%M:%S',time.gmtime(timeStep))
    #         # print(timestr)
    #         self.ticker.display(timestr)
    #         self.update_GUI()
    #         time.sleep(1)
        # pdb.set_trace()
        # self.historylist.clear()
                # textstr.startTime = self.startTime
            # textstr = x['start']+':'+x['stop']+':'+x['userID']
            # print(textstr)
            # for x in range(1,self.itemShowNum):
            #     pass
            # pdb.set_trace()
            # self.historylist.appendPlainText(textstr)
                # self.plaintlist.append(textstr)
            # if len(self.texlist) > 3:
            #     return
    '''
    def beginOendTime(self):
        timeState = self.timeEdit.text()
        if self.seButton.buttonState == 'begin' and timeState != '0:00':
            #记录起始时间
            self.beginTime = time.time()
            print('beginTime:',self.beginTime)
            self.beginTimeSignal.emit(self.beginTime)
            # self.emitBeginTime()
            #设置时长
            self.editTime = self.timeEdit.time()
            self.timeStateSignal.emit(self.editTime.toPyTime())
            self.logStateSignal.emit(True)
            print('editTime:',self.editTime,'toPyTime',self.editTime.toPyTime())
            self.timebegin = True
            threading.Thread(target=self.timerStep,daemon = True).start()
            self.ledStartTime = time.clock()
            self.seButton.setText('stop')
            self.seButton.buttonState = 'stop'
            self.timeStepPause = False
            time.sleep(0.3)
        elif self.seButton.buttonState == 'stop':
            self.timebegin = False
            self.seButton.setText('begin')
            self.seButton.buttonState = 'begin'
    '''





###
#emit
###
    # def emitBeginTime(self):
    #     self.beginTime.emit(self.beginTime)


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = PowerRecord()
    addressBook.show()

    sys.exit(app.exec_())
