#!/usr/bin/env python
# coding=utf-8

# Library imports
from PyQt5.QtWidgets    import QWidget
from PyQt5.QtWidgets    import QLabel
from PyQt5.QtWidgets    import QLineEdit
from PyQt5.QtWidgets    import QPushButton
from PyQt5.QtWidgets    import QPlainTextEdit
from PyQt5.QtWidgets    import QCheckBox
from PyQt5.QtWidgets    import QVBoxLayout
from PyQt5.QtWidgets    import QHBoxLayout
from PyQt5.QtWidgets    import QGridLayout
from PyQt5.QtWidgets    import QComboBox
from PyQt5.QtWidgets    import QMessageBox
from PyQt5.QtWidgets    import QSpinBox
from PyQt5.QtWidgets    import QSpacerItem
from PyQt5.QtWidgets    import QTabWidget
from PyQt5.QtWidgets    import QGroupBox
from PyQt5.QtWidgets    import QAction


from PyQt5.QtCore       import QTimer
from PyQt5.QtCore       import QObject
from PyQt5.QtCore       import pyqtSignal
from PyQt5.QtCore       import Qt
from PyQt5.QtCore       import QSize
from PyQt5.QtCore       import QEvent
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QLineF
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtGui       import QPixmap


#plot PaintArea class


from queue              import Queue
from functools        import partial
import time
import pdb

from matplotlibPyQt5 import MyDynamicMplCanvas

from powerrecord import PowerRecord
from user import UserView
from user import User
from lastlog import LastLog

class View(QWidget):

    send_data           = pyqtSignal(object)
    baudrate_changed    = pyqtSignal(object)
    #eol_changed         = pyqtSignal(object)
    port_changed        = pyqtSignal(object)
    seedPulseChanged = pyqtSignal(object)
    seedFreValueChanged = pyqtSignal(object)
    seedPulseFreChanged = pyqtSignal(object)
    firstPumpChanged = pyqtSignal(object)
    secondPumpChanged = pyqtSignal(object)
    startModel = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)

        self.queue      = Queue()
        self.end_cmd    = None
        self.autoscroll = True
        self.msg_sent   = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)
        self.currentValueList =list()
        self.currentTimeList = list()
        self.buttonMinimumWidth = 100
        self.topSeedCurrent = 700
        self.topPumpCurrent = 1000
        self.canClosePort = True

        self.initSeedPulse = 0
        self.initSeedFre = 0
        self.init1stCurrent = 0
        self.init2stCurrent = 0
        self.initSeedCurrent =0
        self.last = LastLog()
        self.lastpick = self.last.loadLast()
        uslast = self.lastpick.get('user',False)
        if uslast is False:
            self.user = User()
        else:
            self.user = uslast
        self.__init__slaveStatus()
        self.__initUI()


    def __init__slaveStatus(self):
        self.isSeedOpen = False
        self.seedcurrentre = False
        self.seedpulsere = False
        self.seedfrequecere = False
        self.seedcurrent = 0
        self.seedpulse = 0
        self.seedfrequece = 0
        self.firstcurrent = 0
        self.secondcurrent = 0
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False
        self.isLEDOpen = False


    def __initUI(self):
        #main box
        self.mainBox = QVBoxLayout(self)#使用垂直布局类

        self.showBox = QHBoxLayout()
        # show area
        self.cmd_edit = QLineEdit()

        cmd_btn = QPushButton('Send Command (ctrl+Q)')
        cmd_btn.setMinimumWidth(self.buttonMinimumWidth)
        cmd_btn.clicked.connect(self.emit_send_data)
        #import cmd strl+enter
        cmdEnterAction = QAction(self)
        cmdEnterAction.setShortcut('ctrl+Q')
        cmdEnterAction.setStatusTip(' press ctrl+Q to send command')
        cmdEnterAction.triggered.connect(self.emit_send_data)
        self.cmd_edit.addAction(cmdEnterAction)
        self.editer = QPlainTextEdit()
        self.editer.setReadOnly(True)
        cmdBox = QVBoxLayout()
        cmdBox.addWidget(self.cmd_edit)
        cmdBox.addWidget(cmd_btn)
        cmdBox.addWidget(self.editer)
        self.editer.setMaximumSize(300,1000)
        cmd_btn.setMaximumSize(300,400)
        self.cmd_edit.setMaximumSize(300,100)
        #painter plot
        # self.painter = PaintArea()
        self.paintwidget = QWidget(self)
        self.painter = MyDynamicMplCanvas(self.paintwidget, width=5, height=4, dpi=100)
        self.showBox.addLayout(cmdBox)
        self.showBox.addWidget(self.painter)

        # setSeedPlot = QPushButton('plot')
        # setSeedPlot.clicked.connect(self.Button2Plot)
        # seedBox.addWidget(setSeedPlot)
        self.toolBoxUI()
        self.mainBox.addWidget(self.toolBox)
        self.mainBox.addLayout(self.showBox)

        self.setLayout(self.mainBox)
        self.setWindowTitle("光子暗化平台软件")

    def toolBoxUI(self):
        gbox1 = QGroupBox()
        gbox1.setStyleSheet("QGroupBox{border:None;}")
        gbox2 = QGroupBox()
        gbox2.setStyleSheet("QGroupBox{border:None;}")
        gbox3 = QGroupBox()
        gbox3.setStyleSheet("QGroupBox{border:None;}")
        gbox4 = QGroupBox()
        gbox4.setStyleSheet("QGroupBox{border:None;}")
        gbox5 = QGroupBox()
        gbox5.setStyleSheet("QGroupBox{border:None;}")
        #self.menuBox = QHBoxLayout()
        self.useBox = QHBoxLayout(gbox1)
        self.setBox = QHBoxLayout(gbox2)
        self.pumpBox = QHBoxLayout(gbox3)
        self.powerRecordBox = QHBoxLayout(gbox4)
        self.toolBox = QTabWidget()
        # self.toolBox.setStyleSheet("QTabWidget.pane{background: transparent;}\
        #     ")
        self.toolBox.addTab(gbox1,'用户登录')
        self.toolBox.addTab(gbox2,'串口设置')
        self.toolBox.addTab(gbox3,'泵浦开关')
        self.toolBox.addTab(gbox4,'功率计')
        self.toolBox.addTab(gbox5,'帮助')
        # self.toolBox.
        self.toolBox.setTabEnabled(1,False)
        self.toolBox.setTabEnabled(2,False)
        self.toolBox.setTabEnabled(3,False)
        self.toolBox.setMaximumSize(10000,200)
        self.toolBox.resize(1200,200)
        userbox = UserView()
        userbox.usersignal.connect(self.setUser)
        self.useBox.addWidget(userbox)
        self.useBox.addStretch()
        self.powerRecord = PowerRecord()
        self.powerRecordBox.addWidget(self.powerRecord)
#
#启动设置tabbox栏目，包含于setBox
#

# 按下初始化按钮，启动串口线程，该线程开始循环直至程序结束
# 设置串口，设置成功后，串口线程可以开始读取数据
# 开始后续设置
# 关闭串口，并将ser设为none

        portBox = QGridLayout()
        seedBox = QVBoxLayout()
        firstPumpBox = QVBoxLayout()
        secondPumpBox = QVBoxLayout()
        # Command box
        self.setBox.addLayout(portBox)
        self.pumpBox.addLayout(seedBox)
        self.pumpBox.addLayout(firstPumpBox)
        self.pumpBox.addLayout(secondPumpBox)
        self.setBox.addStretch()
        self.pumpBox.addStretch()
        #
        # self.showBox.addLayout(cmdBox)

        self.startButton = QPushButton('Start')
        self.startButton.setEnabled(True)
        self.startButton.setMinimumWidth(self.buttonMinimumWidth)
        self.setPortButton = QPushButton('openport')
        self.setPortButton.setMinimumWidth(self.buttonMinimumWidth)
        self.setPortButton.setEnabled(False)

        self.closePortButton = QPushButton('closePort')
        self.closePortButton.setMinimumWidth(self.buttonMinimumWidth)
        self.closePortButton.setEnabled(False)


        #self.startButton.setCheckable(True)
        #self.startButton.clicked.connect(partial(self.emit_send_command,'openport'))
        # portBox.addWidget(self.startButton, 0, 0)
        portBox.addWidget(self.setPortButton, 0, 0)
        portBox.addWidget(self.closePortButton, 0, 1)

        # - Baudrate select
        self.baundrateMenu = QComboBox()
        self.menuItem = ['300 baud','1200 baud',
            '2400 baud','4800 baud','9600 baud',
            '19200 baud','38400 baud','57600 baud',
            '115200 baud','230400 baud','250000 baud']
        self.baundrateMenu.addItems(self.menuItem)
        self.baundrateMenu.currentIndexChanged.connect(self.emit_br_changed)
        self.baundrateMenu.setEnabled(False)
        # Set default baudrate 9600
        baudindex = self.lastpick.get('baud',False)
        if baudindex is not False :
            self.baundrateMenu.setCurrentIndex(baudindex)
        else:
            self.baundrateMenu.setCurrentIndex(4)
        # print(self.baundrateMenu.setCurrentIndex())
        # pdb.set_trace()
        baudLabel = QLabel('baud: ')
        portBox.addWidget(baudLabel,1,0)
        portBox.addWidget(self.baundrateMenu, 1, 1)
        #port select
        portLabel = QLabel('Port: ')
        # portLB = QHBoxLayout()
        portBox.addWidget(portLabel, 2, 0)
        self.portEdit = QLineEdit()
        self.portEdit.setEnabled(False)
        portindex = self.lastpick.get('port',False)
        if baudindex is not False :
            self.portEdit.setText(portindex)
        #self.portEdit.editingFinished.connect(self.changePort)
        portBox.addWidget(self.portEdit, 2, 1)
        #portBox.addLayout(portLB, 2, 1)
        #portBox.addStretch()
        #portSetBox.addLayout(stng_hbox)
        #self.setBox.addLayout(portBox)


        # cmd_btncr = QPushButton('sendcurrentcmd')
        # cmd_btncr.clicked.connect(partial(self.emit_send_command,'sendcurrent'))
        # cmdButtonBox.addWidget(cmd_btncr)
        #seedBox项目

        self.openSeedButton = QPushButton('setSeedButton')
        self.openSeedButton.setMinimumWidth(self.buttonMinimumWidth)

        #self.openSeedButton.setDisabled(True)
        self.openSeedButton.setEnabled(False)
        self.openSeedButton.clicked.connect(self.emitSeedPulseAndFre)
        seedBox.addWidget(self.openSeedButton)
        seedPluseBox = QHBoxLayout()
        self.seedPluseLabel = QLabel('setSeedPulse:')
        #self.etSeedPulseButton.clicked.connect(partial(self.emit_send_command,'setseed'))
        seedPluseBox.addWidget(self.seedPluseLabel)

        self.setSeedPulse = QSpinBox(self)
        self.setSeedPulse.setMaximum(500)
        self.setSeedPulse.setEnabled(False)
        self.setSeedPulse.setSingleStep(50)
        self.setSeedPulse.setValue(self.initSeedPulse)
        self.setSeedPulse.setSuffix('ms')
        #self.setSeedPulse.setReadOnly(True)
        #self.setSeedPulse.valueChanged.connect(self.emitWriteSeedPulse)
        #seedBox.addWidget(self.setSeedPulse)
        seedPluseBox.addWidget(self.setSeedPulse)

        seedFreBox = QHBoxLayout()
        self.seedFreLabel = QLabel('setSeedFre:    ')
        #self.setSeedButton.clicked.connect(partial(self.emit_send_command,'setSeedFre'))
        seedFreBox.addWidget(self.seedFreLabel)

        self.setSeedFreValue = QSpinBox(self)
        self.setSeedFreValue.setMaximum(500)
        self.setSeedFreValue.setEnabled(False)
        self.setSeedFreValue.setSingleStep(50)
        self.setSeedFreValue.setValue(self.initSeedFre)
        self.setSeedFreValue.setSuffix('kHz')
        #self.setSeedFreValue.valueChanged.connect(self.emitWriteSeedFre)
        seedFreBox.addWidget(self.setSeedFreValue)

        seedcurrBox = QHBoxLayout()
        self.setSeedCurrentLabel = QLabel('setSeedCurrent:')
        self.setSeedCurrent = QSpinBox()

        self.setSeedCurrent.setMaximum(self.topSeedCurrent)
        self.setSeedCurrent.setEnabled(False)
        self.setSeedCurrent.setSingleStep(50)
        self.setSeedCurrent.setValue(self.initSeedCurrent)
        self.setSeedCurrent.setSuffix('mA')
        seedcurrBox.addWidget(self.setSeedCurrentLabel)
        seedcurrBox.addWidget(self.setSeedCurrent)
        # seedcurrBox.addWidget(self.setSeedCurrent)

        seedBox.addLayout(seedPluseBox)
        seedBox.addLayout(seedFreBox)
        seedBox.addLayout(seedcurrBox)
        #seedBox.addStretch()

        # amp select
        self.openAll = QPushButton('openall')
        self.openAll.setMinimumWidth(self.buttonMinimumWidth)
        self.openAll.setEnabled(False)
        #.setEnabled(True)
        #self.openAll.clicked.connect(partial(self.emit_send_command,'openAll'))
        firstPumpBox.addWidget(self.openAll)
        self.setSeedCurrentLabel = QLabel('setSeedCurrent:')
        self.openSecondPump = QPushButton('opensecondpump')
        self.openSecondPump.setMinimumWidth(self.buttonMinimumWidth)
        self.openSecondPump.setEnabled(False)
        self.openSecondPump.clicked.connect(partial(self.emit_send_command,'opensecondpump'))


        # firstPumpLabel=QLabel('一级泵浦调节')
        # secPumpLabel=QLabel('二级泵浦调节')
        self.sendfirst = QPushButton('setfirst')
        self.sendfirst.setEnabled(False)
        self.sendfirst.clicked.connect(self.emitFirstPumpCurrent)
        self.sendsecond = QPushButton('setsecond')
        self.sendsecond.setEnabled(False)
        self.sendsecond.clicked.connect(self.emitSecondPumpCurrent)
        self.setFirstpump = QSpinBox(self)
        self.setFirstpump.setMaximum(self.topPumpCurrent)
        self.setFirstpump.setEnabled(False)
        self.setFirstpump.setSingleStep(50)
        self.setFirstpump.setValue(self.init1stCurrent)
        self.setFirstpump.setSuffix('mA')
        self.setSecondpump = QSpinBox(self)
        self.setSecondpump.setMaximum(self.topPumpCurrent)
        self.setSecondpump.setEnabled(False)
        self.setSecondpump.setSingleStep(50)
        self.setSecondpump.setValue(self.init2stCurrent)
        self.setSecondpump.setSuffix('mA')
        # self.setFirstpump.valueChanged.connect(self.emitFirstPumpCurrent)
        # self.setSecondpump.valueChanged.connect(self.emitSecondPumpCurrent)
        self.closeAll = QPushButton('closeAll')
        # self.closeAll = QPushButton('setsecond')
        self.closeAll.setEnabled(False)
        # self.closeAll.clicked.connect(self.emitSecondPumpCurrent)
        self.setFirstpump.setEnabled(False)
        self.setSecondpump.setEnabled(False)

        firstPumpBox.addWidget(self.sendfirst)
        secondPumpBox.addWidget(self.closeAll)
        secondPumpBox.addWidget(self.sendsecond)
        firstPumpBox.addWidget(self.setFirstpump)
        secondPumpBox.addWidget(self.setSecondpump)

        firstPumpBox.addStretch()
        secondPumpBox.addStretch()
        #self.resize(250, 150)
        #tool init
        # widget1=QWidget()
        # widget2=QWidget()


        # #vboxMenu.addWidget(painter)
        # #空出部分以供后面补充
        # vboxMenu = QHBoxLayout(gbox1)
        # vboxMenu.addWidget(widget1)
        # vboxShow = QHBoxLayout(gbox3)
        # vboxShow.addWidget(widget2)

    def show_error(self, value):
        msg = QMessageBox(
                QMessageBox.NoIcon, 'Error occured.', value, QMessageBox.Ok)
        msg.exec()

    def afterOpenModel(self):
        self.startButton.setEnabled(False)
        self.setPortButton.setEnabled(True)
        self.closePortButton.setEnabled(True)
        self.baundrateMenu.setEnabled(True)
        self.portEdit.setEnabled(True)

    def afterOpenPort(self):
        self.startButton.setEnabled(False)
        self.setPortButton.setEnabled(False)
        self.closePortButton.setEnabled(True)
        self.baundrateMenu.setEnabled(False)
        self.portEdit.setEnabled(False)
        self.openSeedButton.setEnabled(True)
        self.setSeedPulse.setEnabled(True)
        self.setSeedFreValue.setEnabled(True)
        self.setFirstpump.setEnabled(True)
        self.setSecondpump.setEnabled(True)
        self.sendfirst.setEnabled(True)
        self.sendsecond.setEnabled(True)
        self.closeAll.setEnabled(True)
        self.openAll.setEnabled(True)
        self.openSecondPump.setEnabled(True)
        self.setSeedCurrent.setEnabled(True)

    def afterClosePort(self):
        self.startButton.setEnabled(False)
        self.setPortButton.setEnabled(True)
        self.closePortButton.setEnabled(False)
        self.baundrateMenu.setEnabled(True)
        self.portEdit.setEnabled(True)
        self.openSeedButton.setEnabled(False)
        self.setSeedPulse.setEnabled(False)
        self.setSeedFreValue.setEnabled(False)
        self.setFirstpump.setEnabled(False)
        self.setSecondpump.setEnabled(False)
        self.sendfirst.setEnabled(False)
        self.sendsecond.setEnabled(False)
        self.closeAll.setEnabled(False)
        self.openAll.setEnabled(False)
        self.openSecondPump.setEnabled(False)
        self.setSeedCurrent.setEnabled(False)

    def enablePortSet(self):
        self.setPortButton.setEnabled(True)
        self.closePortButton.setEnabled(False)
        self.baundrateMenu.setEnabled(True)
        self.portEdit.setEnabled(True)
        self.startButton.setEnabled(False)


    def enableClosePort(self):
        if self.setSeedPulse.text()[:-2] > self.initSeedPulse :
            self.canClosePort = False
        print(self.canClosePort)
        if self.setSeedFreValue.texttext()[:-3] > self.initSeedFre :
            self.canClosePort = False
        print(self.canClosePort)
        if self.setSeedCurrent.text()[:-2] > self.initSeedCurrent:
            self.canClosePort = False
        print(self.canClosePort)
        if self.setFirstpump.text()[:-2] > self.init1stCurrent :
            self.canClosePort = False
        print(self.canClosePort)
        if self.setSecondpump.text()[:-2] > self.init2stCurrent :
            self.canClosePort = False
        print(self.canClosePort)

    def seedCurrentSet(self,value):
        self.seedcurrent = value
        # pdb.set_trace()
        self.setSeedCurrent.setValue(self.seedcurrent)

    def seedPulseSet(self,value):
        self.seedpulse = value
        self.setSeedPulse.setValue(self.seedpulse)

    def seedFrequeceSet(self,value):
        self.seedfrequece = value
        self.setSeedFreValue.setValue(self.seedfrequece)

    def firstCurrentSet(self,value):
        self.firstcurrent = value
        self.setFirstpump.setValue(self.firstcurrent)

    def secondCurrentSet(self,value):
        self.secondcurrent = value
        self.setSecondpump.setValue(self.secondcurrent)

#==============================================================================
# Get, set
#==============================================================================

    def set_queue(self, queue):
        self.queue = queue

    def set_end_cmd(self, end_cmd):
        self.end_cmd = end_cmd

    def set_autoscroll(self, value):
        self.autoscroll = value

    def set_port(self, value):
        self.portEdit.clear()
        self.portEdit.insert(value)

    def getPort(self):
        self.lastpick['port'] = self.portEdit.text()
        return self.portEdit.text()

    def getBaudrate(self):
        self.lastpick['baud'] = self.baundrateMenu.currentIndex()
        return self.baundrateMenu.currentText()[:-5]


    def get_cmd(self):
        return self.cmd_edit.text()



    # def plotListGet(self):
    #     return self.currentValueList



    def setCurrentValue(self, currentValue,timeValue):
        if currentValue is not None:
            self.currentValueList = currentValue
            self.currentTimeList = timeValue


    def Button2Plot(self):
        self.painter.update_figure()

    def closeEvent(self, event):
        self.last.saveLast(self.lastpick)
        self.end_cmd()
        QWidget.closeEvent(self, event)
        print('exit')

    def beginGui(self):
        self.update()

    def update_gui(self):
        self.process_incoming()
        self.update()

    def updataFigure(self,valulist):
        # self.setCurrentValue(currentValue, timeValue)
        self.painter.XYaxit(valulist[0],valulist[1])
        self.painter.update_figure()
        # self.update()

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.editer.appendPlainText(str(msg))
                #show to the textplain?
                #if self.autoscroll:
                self.editer.ensureCursorVisible()
                self.scroll_down()
            except Queue.empty:
                print('=== empty queue ===')

    def scroll_down(self):
        sb = self.editer.verticalScrollBar()
        sb.setValue(sb.maximum())


    def changePort(self):
        if not self.msg_sent:
            self.msg_sent = True
            self.emit_port_changed()
        else:
            self.msg_sent = False
            return None

#==============================================================================
# Signals
#==============================================================================

    def emit_send_data(self):
        self.send_data.emit(self.get_cmd())
        self.cmd_edit.clear()

    def emit_send_command(self,command):
        self.send_data.emit(command)
        self.cmd_edit.clear()



    def emit_br_changed(self, value):
        baudrate = self.baundrateMenu.itemText(value)[:-5]
        self.baudrate_changed.emit(baudrate)

    def emit_port_changed(self):
        self.port_changed.emit(self.portEdit.text())
        self.portEdit.clear()

    def emitWriteSeedPulse(self):
        self.seedPulseChanged.emit(self.setSeedPulse.text()[:-2])

    def emitWriteSeedFre(self):
        self.seedFreValueChanged.emit(self.setSeedFreValue.text()[:-3])

    def emitFirstPumpCurrent(self):
        self.firstPumpChanged.emit(self.setFirstpump.text()[:-2])

    def emitSecondPumpCurrent(self):
        self.secondPumpChanged.emit(self.setSecondpump.text()[:-2])


    def emitSeedPulseAndFre(self):
        seedPulseAndFre = [self.setSeedPulse.text()[:-2],
            self.setSeedFreValue.text()[:-3],self.setSeedCurrent.text()[:-2]]
        # print(self.setSeedPulse.text()[:-2],
        #     self.setSeedFreValue.text()[:-2],self.setSeedCurrent.text()[:-2])
        self.seedPulseFreChanged.emit(seedPulseAndFre)

    def setUser(self,value):
        self.user = value
        if value.getName() is not False:
            self.toolBox.setTabEnabled(1,True)
            self.toolBox.setTabEnabled(2,True)
            self.toolBox.setTabEnabled(3,True)
            self.powerRecord.setUserID(self.user.getName())
            # self.startModel.emit()
        else:
            self.toolBox.setTabEnabled(1,False)
            self.toolBox.setTabEnabled(2,False)
            self.toolBox.setTabEnabled(3,False)
            self.powerRecord.setUserID('NoneUser')
        print('use in view:',self.user.getName())



class PaintArea(QWidget):
    """docstring for PaintArea"""
    def __init__(self):
        super(PaintArea, self).__init__()
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(500,400)
        self.text = u'这个地方是绘图区域'
        self.pen = QPen(Qt.black,1)
        self.brush = QBrush()
        self.font = QFont('arial', 15)
        self.pList = list()
        self.initTime = time.time()
        #print('self.pList:',self.pList)

    def paintEvent(self,event):

        #pList = [int().from_bytes(x,'big') for x in self.pList]
        pList =self.pList
        #print('调用paintEvent:',len(pList),',event:',event)
        p = QPainter(self)
        #print('p=',p)
        if len(pList) > 1:
            p.translate(180,180)
            p.setWindow(-10,-10,50,10)

            qPointList = [QPointF(c[0] - self.initTime,c[1]) for c in pList]
            #需要判断一下绘图范围
            print(qPointList)
            p.setPen(self.pen)
            p.setBrush(self.brush)
            qPointlast = QPointF(0,0)
            for qpPoint in qPointList:
                #print('point:',qpPoint,qPointlast)
                p.drawLine(qpPoint,qPointlast)
                qPointlast = qpPoint

        else:
            self.drawText(event,p)

    def plotupdate(self):
        self.update()

    def drawText(self,event,qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('微软雅黑', 20))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def getpList(self, pList):
        self.pList = pList
        self.text = u'开始缓存电流数据'
        #return self.pList
