# PyQt lib
from PyQt5.QtCore import (pyqtSignal, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox)

#py lib
import time
import pickle
import queue
import numpy
# view
from view.pdfcreater import PdfCreater
from view.reportDialog import ReportDialog
from view.ticker import Ticker
from view.historylist import HistoryList
#UI
from UI.recordUI import Ui_Form as RecodUI
#model
from frame.singleton import PickContext
from model.database import DataHand


class PowerRecord(QWidget,RecodUI):
    """docstring for PowerRecord"""

    beginTimeSignal = pyqtSignal(object,object)
    sqlTableName = pyqtSignal(object)
    stopSavePower = pyqtSignal(object)
    timeStateSignal = pyqtSignal(object)
    logStateSignal = pyqtSignal(object)
    plotlist = pyqtSignal(object,object,object)
    # plotlistbegin = pyqtSignal(object)

    def __init__(self):
        super(PowerRecord, self).__init__()
        # self.wrpick = WRpickle('data\\reportLast.pickle')
        # self.pickContext = self.wrpick.loadPick()
        self.pickContext = PickContext()
        self.datahand = DataHand()
        self.startTime = 0
        self.stopTime = time.time()
        self.userID = ''
        self.powerData = queue.Queue()
        self.pick = list()
        self.itemShowNum = 4
        self.itemChangeStatus = False
        self.timeStepPause = False
        # self.pdfItem = dict()
        self.figGet = None
        self.timebegin = True
        # self.loadFile()
        self.UI_init()
        # self.plantlist()
        # with open('template.qss') as t:
        #     self.setStyleSheet(t.read())
        # self.initItemText()
        # self.arg = arg
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update())
        # self.timer.start(100)

    def _setupUi(self):
        self.setupUi(self)

    def UI_init(self):
        self._setupUi()
        self.seButton = self.logButton
        self.seButton.buttonState = 'begin'
        self.seButton.clicked.connect(self.beginOendTime)
        # self.timeEdit = self.timeEdit
        self.timeEdit.setDisplayFormat(' s : hh : mm')
        # self.timeEdit.setDate(QDate(2000,10,10))
        # print(self.timeEdit.text())
        self.ticker.hide()
        self.ticker = Ticker()
        self.gridLayout.addWidget(self.ticker, 3, 1, 1, 1)
        # self.formLayout.setWidget(3, QFormLayout.FieldRole, self.ticker)
        self.ticker.start()
        self.ticker.timeOut.connect(self.tickerTimeOut)
        # self.ticker.setNumDigits(10)
        # self.ticker.display('00:00:00')
        self.historyEdit = HistoryList()
        self.gridLayout_2.addWidget(self.historyEdit, 1, 0, 1, 2)
        self.historyEdit.itemSelectedEmit.connect(self.itemSelectionChanged)
        self.historyEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.printButton.clicked.connect(self.printReport)
        # self.stepEdit.setValidator(QValidator(0.01,1000))
        # self.historyEdit.setCurrentRow(1)
        # for x in range(0,self.itemShowNum):
        #     item = QListWidgetItem()
        #     self.historyEdit.addItem(item)
        # self.historyEdit.itemSelectionChanged.connect(self.itemSelect)
        # buttonarea = QVBoxLayout()
        # self.printButton = self.printButton

        # buttonarea.addWidget(self.seButton)
        # buttonarea.addWidget(self.timeEdit)
        # buttonarea.addWidget(self.printButton)
        # buttonarea.addStretch()
        # buttonarea.addWidget(self.ticker)
        # mainLayout = QGridLayout()
        # mainLayout.addWidget(self.historyEdit, 0,1)
        # mainLayout.addLayout(buttonarea, 0, 0)
        # self.setLayout(mainLayout)
        # self.setLayout(self)


    # def itemSelect(self):
    #     self.itemText = self.historyEdit.currentItem().text()
    #     self.itemNum = self.historyEdit.currentRow()
    #     # print(self.itemNum)
    #     pickget = self.pick[-self.itemNum-1]
    #     self.startTimetic = pickget.get('begin')
    #     self.printUserID = pickget.get('userID')
    #     print('itemSelect:',self.itemNum, self.startTimetic,self.printUserID)
    #     self.itemChangeStatus = True
    #     # print(self.itemText)

    def itemSelectionChanged(self,item):
        print('getitem',item)
        #get nowtable
        self.tableName = item
        self.sqlTableName.emit(self.tableName)
        temp = item.split('US')
        self.userID = temp[1]
        self.timeTick = temp[2:]
        # self.NowContextGet()
        #get last log
        self.pickContext = PickContext()
        #get username
        self.pickContext['worker'] = self.userID
        #get plot from db
        plotdata = self.datahand.getTableData(self.tableName)
        time_ = []
        power = []
        for x in plotdata:
            time_.append(x[0])
            power.append(x[1])
        self.plotlist.emit(False,time_,power)
        #get calc report
        if time_:
            self.pickContext['timelong'] = str(int(time_[-1]-time_[0]))+'秒'
            self.pickContext['maxsignalpower'] = self.__Power2str(max(power))
            self.pickContext['minsingalpower'] = self.__Power2str(min(power))
            self.pickContext['averagesingalepower'] = self.__Power2str(numpy.mean(power))
            self.pickContext['powerstable'] = self.__Power2str(numpy.std(power))
        else:
            self.pickContext['timelong'] = '0'
            self.pickContext['maxsignalpower'] = '0'
            self.pickContext['minsingalpower'] = '0'
            self.pickContext['averagesingalepower'] = '0'
            self.pickContext['powerstable'] = '0'
        print('PowerRecord change')
        self.pickContext.save_pick_file()

    def printReport(self):
        # self.getDbdata()
        if self.figGet:
            self.figGet.savePlotFig()
        rep = ReportDialog(self)
        # print('rep',rep)
        rep.exec_()
        if rep.saveOrcancel == 'save':
            print('pickContext',self.pickContext.pickContext)
            printer = PdfCreater(self,)
            self.sqlTableName.connect(printer.getDBData)
            printer.saveToFile()
        # printer.savePdf()

        # if self.itemChangeStatus is False:
        #     self.itemText = self.historyEdit.item(0).text()
        # print('print:',self.itemText)
        # self.pdfItem['']

    def getNowFig(self,fig):
        self.figGet = fig


    # def NowContextGet(self):


    # # def plotTable():
    #     pass


    def beginOendTime(self):
        # self.ticker.run()
        if self.seButton.buttonState == 'begin':
            self.timeLong = self.timeEdit2time()
            # pdb.set_trace()
            print('stepEdit',self.stepEdit.text()[:-1])
            self.timeStep = int(self.stepEdit.text()[:-1])
            if self.timeLong < self.timeStep:
                QMessageBox.information(self, "设置错误","记录时长要比记录步长大")
                return
            else:
            #记录起始时间
                self.beginTime = time.time()
                print('beginTime:',self.beginTime)
                self.beginTimeSignal.emit(self.beginTime, self.timeStep)
                self.stopSavePower.emit(True)
                self.ticker.startTick(self.timeLong)
                self.timeStateSignal.emit(self.timeLong)
                self.logStateSignal.emit(True)

                self.seButton.setText('停止')
                self.seButton.buttonState = 'stop'
        elif self.seButton.buttonState == 'stop':
            self.ticker.stopTick()
            self.seButton.setText('开始')
            self.seButton.buttonState = 'begin'
            self.stopSavePower.emit(False)

    # def isStartSave(self,):
    #     if self.timeLong < int(self.stepEdit.text())
    #         QMessageBox.information(self, "设置错误",
    #         "记录时长要比记录步长大")
    #     return False
    # return True

    def tickerTimeOut(self):
        print('time out')
        self.seButton.setText('开始')
        self.seButton.buttonState = 'begin'
        self.stopSavePower.emit(False)


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
            self.itemText = self.historyEdit.item(0).text()
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
                starttime = time.strftime('%H:%M:%S',time.localtime(x.get('start')))
                stoptime = time.strftime('%H:%M:%S',time.localtime(x.get('stop')))
                textstr = 'start:'+starttime+', stop:'+stoptime+', user:'+x.get('userID')
            elif x.get('begin',False) is not False:
                begin = time.strftime('%H:%M:%S',time.localtime(x.get('begin')))
                con = x.get('continue').toString()
                textstr = 'begin:' + begin + ', cont:' + con + ', user:'+x.get('userID')
            if i < self.itemShowNum:
                item = self.historyEdit.item(self.itemShowNum-i-1)
                item.setText(textstr)

    def __Power2str(self,data):
        if data > 0.1:
            return str(round(data,2))+'W'
        else:
            return str(round(data*1000,2)) + 'mW'

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
        # self.historyEdit.addItem(item)
        # item = QListWidgetItem()
        # self.historyEdit.addItem(item)
        # self.historyEdit.setReadOnly(True)
        # timebox = QHBoxLayout()

        # timebox.addWidget(self.hourlabel)
        # timebox.addWidget(self.hourShow)
        # timebox.addWidget(self.minlabel)
        # timebox.addWidget(self.minShow)
        # timebox.addWidget(self.seclabel)

        # self.printButton.clicked.connect(self.getDbdata)

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
    #         gmTimeStep = time.localtime(timeStep)
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
        # beginTime = time.strftime('%H:%M:%S', time.localtime(self.beginTime) )

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
    #         timestr = time.strftime('%H:%M:%S',time.localtime(timeStep))
    #         # print(timestr)
    #         self.ticker.display(timestr)
    #         self.update_GUI()
    #         time.sleep(1)
        # pdb.set_trace()
        # self.historyEdit.clear()
                # textstr.startTime = self.startTime
            # textstr = x['start']+':'+x['stop']+':'+x['userID']
            # print(textstr)
            # for x in range(1,self.itemShowNum):
            #     pass
            # pdb.set_trace()
            # self.historyEdit.appendPlainText(textstr)
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
