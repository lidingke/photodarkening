#!/usr/bin/env python
# coding=utf-8

# Library imports
from PyQt5.QtWidgets    import (QWidget, QLabel, QLineEdit,
    QPushButton, QPlainTextEdit, QCheckBox, QVBoxLayout,
    QHBoxLayout, QGridLayout, QComboBox, QMessageBox,
    QSpinBox, QSpacerItem, QTabWidget, QGroupBox, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtCore       import (QTimer, pyqtSignal, Qt, QPointF,QRect)

# from PyQt5.QtGui import (QColor, QFont, QPainter, QPalette, QPen, QBrush)

#plot PaintArea class
from queue              import Queue
from functools        import partial
import time
import pdb
from UI.portGBUI import Ui_GroupBox as PortGBUI
from UI.pumpUI import Ui_GroupBox as PumpUI
# from UI.powerUI import Ui_Form as PowerUI
# from portGBUI import Ui_GroupBox as PortGBUI
from matplotlibPyQt5 import MyDynamicMplCanvas

from powershow import PowerShow
from powerrecord import PowerRecord
from user import UserView
from user import User
from lastlog import LastLog

class View(QWidget):

    send_data           = pyqtSignal(object)
    baudrate_src_changed    = pyqtSignal(object)
    baudrate_pump_changed    = pyqtSignal(object)
    baudrate_temp_changed    = pyqtSignal(object)
    port_changed        = pyqtSignal(object)
    seedPulseChanged = pyqtSignal(object)
    seedFreValueChanged = pyqtSignal(object)
    seedPulseFreChanged = pyqtSignal(object)
    firstPumpChanged = pyqtSignal(object)
    secondPumpChanged = pyqtSignal(object)
    startSrcModel = pyqtSignal(object)
    startPumpModel = pyqtSignal(object)
    startTempModel = pyqtSignal(object)
    beginTime = pyqtSignal(object)
    emitUsername = pyqtSignal(object)

    def __init__(self):
        super(QWidget,self).__init__()
        QWidget.__init__(self)


        self.queue      = Queue()
        self.end_cmd    = None
        self.autoscroll = True
        self.msg_sent   = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)
        self.srcModelstarted = False
        self.pumpModelstarted = False
        self.tempModelstarted = False
        self.currentValueList =list()
        self.currentTimeList = list()
        self.buttonMinimumWidth = 100
        # self.topSeedCurrent = 700
        # self.topPumpCurrent = 1000
        self.canClosePort = True

        self.initSeedPulse = 0
        self.initSeedFre = 0
        self.init1stCurrent = 0
        self.init2stCurrent = 0
        self.initSeedCurrent =0
        # get the lastsave record
        self.last = LastLog()
        self.lastpick = self.last.loadLast()
        uslast = self.lastpick.get('user',False)
        if uslast is False:
            self.user = User()
        else:
            self.user = uslast
        #init down machine status
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
        '''main window box'''

        self.mainBox = QVBoxLayout(self)#使用垂直布局类
        self.showBox = QHBoxLayout()
        self.setWindowState(Qt.WindowMaximized)
###
#command area: push button, plain text edit and line edit
###
        cmd_btn = QPushButton('Send Command (ctrl+Q)')
        cmd_btn.setMinimumWidth(self.buttonMinimumWidth)
        cmd_btn.clicked.connect(self.emit_send_data)
        #import cmd strl+enter
        cmdEnterAction = QAction(self)
        cmdEnterAction.setShortcut('ctrl+Q')
        cmdEnterAction.setStatusTip(' press ctrl+Q to send command')
        cmdEnterAction.triggered.connect(self.emit_send_data)
        self.cmd_edit = QLineEdit()
        self.cmd_edit.addAction(cmdEnterAction)
        cmdBox = QVBoxLayout()
        # cmdBox.addWidget(self.cmd_edit)
        # cmdBox.addWidget(cmd_btn)
        # self.powerShow = PowerUI()
        # self.powerShow.setupUi(QWidget())
        # print('type',type(self.powerShow))
        # cmdBox.addWidget(self.powerShow.widget)

#message box
        self.editer = QPlainTextEdit()
        self.editer.setReadOnly(True)
# <<<<<<< HEAD
        self.editer.setMaximumSize(300,2000)
# =======
        cmdBox = QVBoxLayout()
        # cmdBox.addWidget(self.cmd_edit)
        # cmdBox.addWidget(cmd_btn)
        self.powerShow = PowerShow()
        cmdBox.addWidget(self.powerShow)
# >>>>>>> a45e80ec77a4a8729fa4205165faae001fd09cab
        cmdBox.addWidget(self.editer)
        # cmd_btn.setMaximumSize(300,400)
        # self.cmd_edit.setMaximumSize(300,100)

###
#paint area use matplotlib
###
        self.paintwidget = QWidget(self)
        self.painter = MyDynamicMplCanvas(self.paintwidget, width=5, height=4, dpi=100)
        # self.showBox.addLayout(self.powerShowUI())
        self.showBox.addLayout(cmdBox)
        self.showBox.addWidget(self.painter)
        self.toolBoxUI()
        self.mainBox.addWidget(self.toolBox)
        self.mainBox.addLayout(self.showBox)

        #painter plot
        # self.painter = PaintArea()
        # setSeedPlot = QPushButton('plot')
        # setSeedPlot.clicked.connect(self.Button2Plot)
        # seedBox.addWidget(setSeedPlot)

        self.setLayout(self.mainBox)
        self.setWindowTitle("光子暗化平台软件")

    def toolBoxUI(self):
        '''use a tab widget to organize set area
        '''
###
#QTabWidget() layout
###
        gbox1 = QGroupBox()
        gbox1.setStyleSheet("QGroupBox{border:None;}")
        self.useBox = QHBoxLayout(gbox1)
        self.useBox.setGeometry(QRect( 0, 0, 300,100))
        gbox2 = QGroupBox()
        gbox2.setStyleSheet("QGroupBox{border:None;}")
        self.portUI = PortGBUI()
        self.portUI.setupUi(gbox2)
        # self.portUI.widget.setGeometry(QRect( 0, 0, 450,200))
        gbox3 = QGroupBox()
        gbox3.setStyleSheet("QGroupBox{border:None;}")
        self.pumpUI = PumpUI()
        self.pumpUI.setupUi(gbox3)
        self.pumpUI.groupBox.setTitle(' ')
        # self.pumpUI.widget.setGeometry(QRect( 0, 0, 400,200))
        gbox4 = QGroupBox()
        gbox4.setStyleSheet("QGroupBox{border:None;}")
        gbox5 = QGroupBox()
        gbox5.setStyleSheet("QGroupBox{border:None;}")
        #self.menuBox = QHBoxLayout()

        # self.setBox = QHBoxLayout(gbox2)
        self.pumpBox = QGridLayout(gbox3)
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
        # self.toolBox.resize(1200,200)
        userbox = UserView()
        userbox.usersignal.connect(self.setUser)
        self.useBox.addWidget(userbox)
        # self.useBox.addStretch()
        self.powerRecord = PowerRecord()
        self.powerRecord.getNowFig(self.painter)
        self.powerRecord.timeStateSignal.connect(self.painter.getLogTimeState)
        self.powerRecord.logStateSignal.connect(self.painter.getStartLog)
        self.powerRecord.plotlist.connect(self.painter.XYaxitList)
        self.powerRecordBox.addWidget(self.powerRecord)
#
#port set
#
        menuItem = ['300 baud','1200 baud',
            '2400 baud','4800 baud','9600 baud',
            '19200 baud','38400 baud','57600 baud',
            '115200 baud','230400 baud','250000 baud']
        self.portUI.baundrateSource.addItems(menuItem)
        self.portUI.baundratePump.addItems(menuItem)
        # self.portUI.baundrateTemp.addItems(menuItem)
#source port set
        #source
        portItem = ['com1','com2','com3','com4',
            'com5','com6','com7','com8','com9',
            'com10','com11','com12','com13',
            'com14','com15','com16','com17',
            'com18','com19','com20']
        self.portUI.portSource.addItems(portItem)
        self.portUI.portPump.addItems(portItem)
        self.setPortButton = self.portUI.openportSource
        self.closePortButton = self.portUI.closeportSource
        self.baundrateMenu = self.portUI.baundrateSource
        self.portEdit = self.portUI.portSource
        self.baundrateMenu.currentIndexChanged.connect(self.emit_br_src_changed)
        baudindex = self.lastpick.get('srcBaud',False)
        if baudindex is not False :
            self.baundrateMenu.setCurrentIndex(baudindex)
        else:
            self.baundrateMenu.setCurrentIndex(4)
        portindex = self.lastpick.get('srcPort',False)
        if baudindex is not False :
            self.portEdit.setCurrentIndex(portindex)
        else:
            self.portEdit.setCurrentIndex(1)

        baudindex = self.lastpick.get('pumpBaud',False)
        if baudindex is not False :
            self.portUI.baundratePump.setCurrentIndex(baudindex)
        else:
            self.portUI.baundratePump.setCurrentIndex(4)
        portindex = self.lastpick.get('pumpPort',False)
        if baudindex is not False :
            self.portUI.portPump.setCurrentIndex(portindex)
        else:
            self.portUI.portPump.setCurrentIndex(2)

        # baudindex = self.lastpick.get('tempBaud',False)
        # if baudindex is not False :
        #     self.portUI.baundrateTemp.setCurrentIndex(baudindex)
        # else:
        #     self.portUI.baundrateTemp.setCurrentIndex(4)
        # portindex = self.lastpick.get('tempPort',False)
        # if baudindex is not False :
        #     self.portUI.portTemp.setText(portindex)

    # def powerShowUI(self):
    #     self.powerText = QLabel()
    #     powerTextBox = QGroupBox()
    #     powerTextBox.setStyleSheet("QGroupBox{background:blue;}")
    #     # self.powe
    #     layout = QGridLayout(powerTextBox)
    #     layout.addWidget(self.powerText)
    #     return layout



        # ptUI = PortWidget()
        # PtUI = PortUI()
        # PtUI.setupUi(QWidget)
        # print(dir(ptUI))
        # self.setBox.addWidget(ptUI)
        # print(ptUI.openportSource())
        # pdb.set_trace()
        # portBox = QGridLayout()
        # self.baundrateMenu.addItems(self.menuItem)
        # self.startButton = QPushButton('Start')
        # self.menuItem = ['300 baud','1200 baud',
        #     '2400 baud','4800 baud','9600 baud',
        #     '19200 baud','38400 baud','57600 baud',
        #     '115200 baud','230400 baud','250000 baud']
        # self.portEdit.setEnabled(False)
        # self.baundrateMenu.setEnabled(False)
        # Set default baudrate 9600        # - Baudrate select
        # self.closePortButton.setEnabled(False)
        # # portBox.addWidget(self.setPortButton, 0, 0)
        # # portBox.addWidget(self.closePortButton, 0, 1)
        # self.startButton.setEnabled(True)
        # self.setPortButton.setEnabled(False)
        # baudLabel = QLabel('baud: ')
        # # portBox.addWidget(baudLabel,1,0)
        # # portBox.addWidget(self.baundrateMenu, 1, 1)
        # #port select
        # portLabel = QLabel('Port: ')
        # portBox.addWidget(portLabel, 2, 0)
        # portBox.addWidget(self.portEdit, 2, 1)

        # self.startButton.setMinimumWidth(self.buttonMinimumWidth)
        # self.setPortButton.setMinimumWidth(self.buttonMinimumWidth)
        # self.closePortButton.setMinimumWidth(self.buttonMinimumWidth)
        #self.portEdit.editingFinished.connect(self.changePort)
        # portLB = QHBoxLayout()
        # print(self.baundrateMenu.setCurrentIndex())
        # pdb.set_trace()
        # seedBox = QVBoxLayout()
        # firstPumpBox = QVBoxLayout()
        # secondPumpBox = QVBoxLayout()
        # Command box
        # self.pumpBox.addLayout(seedBox)
        # self.pumpBox.addLayout(firstPumpBox)
        # self.pumpBox.addLayout(secondPumpBox)
        # self.pumpBox.addStretch()
        #
        # self.showBox.addLayout(cmdBox)
        #self.startButton.setCheckable(True)
        #self.startButton.clicked.connect(partial(self.emit_send_command,'openport'))
        # portBox.addWidget(self.startButton, 0, 0)

        #portBox.addLayout(portLB, 2, 1)
        #portBox.addStretch()
        #portSetBox.addLayout(stng_hbox)
        #self.setBox.addLayout(portBox)
        # cmd_btncr = QPushButton('sendcurrentcmd')
        # cmd_btncr.clicked.connect(partial(self.emit_send_command,'sendcurrent'))
        # cmdButtonBox.addWidget(cmd_btncr)
        #seedBox项目
        #self.openSeedButton.setDisabled(True)
        # seedBox.addWidget(self.openSeedButton)
        #self.etSeedPulseButton.clicked.connect(partial(self.emit_send_command,'setseed'))
        # seedPluseBox.addWidget(self.seedPluseLabel)
###
#pump set
###
        self.openSeedButton = self.pumpUI.sourceSet
        self.setSeedPulse = self.pumpUI.pulseSpin
        self.openSeedButton.clicked.connect(self.emitSeedPulseAndFre)
        self.setSeedPulse.setValue(self.initSeedPulse)
        self.setSeedFreValue = self.pumpUI.frequencySpin
        self.setSeedCurrent = self.pumpUI.currentSpin
        self.setSeedCurrent.setValue(self.initSeedCurrent)
        self.openAll = self.pumpUI.sourceOpen
        self.sendfirst = self.pumpUI.firstPumpSet
        self.sendfirst.clicked.connect(self.emitFirstPumpCurrent)
        self.sendsecond = self.pumpUI.secondPumpSet
        self.sendsecond.clicked.connect(self.emitSecondPumpCurrent)
        self.setFirstpump = self.pumpUI.firstpumpSpin
        self.setFirstpump.setValue(self.init1stCurrent)
        self.setSecondpump = self.pumpUI.secondpumpSpin
        self.setSecondpump.setValue(self.init2stCurrent)
        self.closeAll = self.pumpUI.sourceClose
        self.pumpUI.firstpumpSpin.setMaximum(1000)
        self.pumpUI.secondpumpSpin.setMaximum(10000)
        self.pumpUI.secondpumpSpin.setSingleStep(500)


        # self.pumpUI.firstPumpSet.setDisabled(True)
        # self.pumpUI.sourceSet.setDisabled(True)

        # self.setSecondpump.setSingleStep(50)
        # self.setFirstpump.setSingleStep(50)
        # self.setSeedCurrent.setSingleStep(50)
        # self.setSeedFreValue.setSingleStep(50)
        # self.setSeedPulse.setSingleStep(50)
        # self.openSeedButton.setMinimumWidth(self.buttonMinimumWidth)
        # self.openSeedButton.setEnabled(False)
        # seedPluseBox = QHBoxLayout()
        # self.seedPluseLabel = QLabel('setSeedPulse:')
        # self.setSeedPulse.setMaximum(500)
        # self.setSeedPulse.setEnabled(False)
        # self.setSeedPulse.setSuffix('ms')
        # seedPluseBox.addWidget(self.setSeedPulse)
        # seedFreBox = QHBoxLayout()
        # self.seedFreLabel = QLabel('setSeedFre:    ')
        #self.setSeedButton.clicked.connect(partial(self.emit_send_command,'setSeedFre'))
        # seedFreBox.addWidget(self.seedFreLabel)
        # self.setSeedFreValue.setSuffix('kHz')
        # self.setSeedFreValue.setMaximum(500)
        # self.setSeedFreValue.setEnabled(False)
        # seedcurrBox = QHBoxLayout()
        # self.setSeedCurrentLabel = QLabel('setSeedCurrent:')

        # self.openAll.setMinimumWidth(self.buttonMinimumWidth)
        # self.openAll.setEnabled(False)
        # self.openAll.hide(True)
        # self.setSeedCurrent.setSuffix('mA')
        # seedcurrBox.addWidget(self.setSeedCurrentLabel)
        # seedcurrBox.addWidget(self.setSeedCurrent)
        # amp select
        # self.openSecondPump = QPushButton('opensecondpump')
        # self.openSecondPump.setMinimumWidth(self.buttonMinimumWidth)
        # self.openSecondPump.setEnabled(False)
        # self.openSecondPump.clicked.connect(partial(self.emit_send_command,'opensecondpump'))

        # self.setSeedCurrent.setMaximum(self.topSeedCurrent)
        # self.setSeedCurrent.setEnabled(False)

        # self.setFirstpump.setMaximum(self.topPumpCurrent)
        # self.setFirstpump.setEnabled(False)
        # self.sendsecond.setEnabled(False)
        # self.setFirstpump.setSuffix('mA')
        # self.sendfirst.setEnabled(False)

        # self.setSecondpump.setSuffix('mA')


        # self.closeAll.setEnabled(False)
        # self.setFirstpump.setEnabled(False)
        # self.setSecondpump.setEnabled(False)
        # self.pumpBox.addWidget(self.openAll,0,0)
        # self.pumpBox.addWidget(self.closeAll,1,0)
        # self.pumpBox.addWidget(self.openSeedButton,2,0)
        # self.pumpBox.addWidget(self.seedPluseLabel,0,1)
        # self.pumpBox.addWidget(self.setSeedPulse,0,2)
        # self.pumpBox.addWidget(self.seedFreLabel,1,1)
        # self.pumpBox.addWidget(self.setSeedFreValue,1,2)
        # self.pumpBox.addWidget(self.setSeedCurrentLabel,2,1)
        # self.pumpBox.addWidget(self.setSeedCurrent,2,2)
        # self.pumpBox.addWidget(self.sendfirst,0,3)
        # self.pumpBox.addWidget(self.setFirstpump,0,4)
        # self.pumpBox.addWidget(self.sendsecond,1,3)
        # self.pumpBox.addWidget(self.setSecondpump,1,4)

        #self.setSeedFreValue.valueChanged.connect(self.emitWriteSeedFre)
        # seedFreBox.addWidget(self.setSeedFreValue)
        # self.setFirstpump.valueChanged.connect(self.emitFirstPumpCurrent)
        # self.setSecondpump.valueChanged.connect(self.emitSecondPumpCurrent)
        # self.closeAll = QPushButton('setsecond')
        # self.closeAll.clicked.connect(self.emitSecondPumpCurrent)
        # seedcurrBox.addWidget(self.setSeedCurrent)
        #self.setSeedPulse.setReadOnly(True)
        #self.setSeedPulse.valueChanged.connect(self.emitWriteSeedPulse)
        #seedBox.addWidget(self.setSeedPulse)
        # seedBox.addLayout(seedPluseBox)
        # seedBox.addLayout(seedFreBox)
        # seedBox.addLayout(seedcurrBox)
        #seedBox.addStretch()
        # firstPumpLabel=QLabel('一级泵浦调节')
        # secPumpLabel=QLabel('二级泵浦调节')
        #.setEnabled(True)
        #self.openAll.clicked.connect(partial(self.emit_send_command,'openAll'))
        # firstPumpBox.addWidget(self.openAll)
        # self.setSeedCurrentLabel = QLabel('setSeedCurrent:')
        # firstPumpBox.addWidget(self.sendfirst)
        # secondPumpBox.addWidget(self.closeAll)
        # secondPumpBox.addWidget(self.sendsecond)
        # firstPumpBox.addWidget(self.setFirstpump)
        # secondPumpBox.addWidget(self.setSecondpump)
        # allPumpBox = QGridLayout(QWidget)
        # self.pumpBox = allPumpBox
        # firstPumpBox.addStretch()
        # secondPumpBox.addStretch()
        #self.resize(250, 150)
        #tool init
        # widget1=QWidget()
        # widget2=QWidget()
        # #vboxMenu.addWidget(painter)
        # vboxMenu = QHBoxLayout(gbox1)
        # vboxMenu.addWidget(widget1)
        # vboxShow = QHBoxLayout(gbox3)
        # vboxShow.addWidget(widget2)

    # def show_error(self, value):
    #     msg = QMessageBox(
    #             QMessageBox.NoIcon, 'Error occured.', value, QMessageBox.Ok)
    #     msg.exec()

    def afterOpenModel(self):
        pass
        # self.startButton.setEnabled(False)
        # self.setPortButton.setEnabled(True)
        # self.closePortButton.setEnabled(True)
        # self.baundrateMenu.setEnabled(True)
        # self.portEdit.setEnabled(True)

    def afterOpenPort(self):
        pass
        # # self.startButton.setEnabled(False)
        # self.setPortButton.setEnabled(False)
        # self.closePortButton.setEnabled(True)
        # self.baundrateMenu.setEnabled(False)
        # self.portEdit.setEnabled(False)
        # self.openSeedButton.setEnabled(True)
        # self.setSeedPulse.setEnabled(True)
        # self.setSeedFreValue.setEnabled(True)
        # self.setFirstpump.setEnabled(True)
        # self.setSecondpump.setEnabled(True)
        # self.sendfirst.setEnabled(True)
        # self.sendsecond.setEnabled(True)
        # self.closeAll.setEnabled(True)
        # self.openAll.setEnabled(True)
        # self.openSecondPump.setEnabled(True)
        # self.setSeedCurrent.setEnabled(True)

    def afterClosePort(self):
        pass
        # # self.startButton.setEnabled(False)
        # self.setPortButton.setEnabled(True)
        # self.closePortButton.setEnabled(False)
        # self.baundrateMenu.setEnabled(True)
        # self.portEdit.setEnabled(True)
        # self.openSeedButton.setEnabled(False)
        # self.setSeedPulse.setEnabled(False)
        # self.setSeedFreValue.setEnabled(False)
        # self.setFirstpump.setEnabled(False)
        # self.setSecondpump.setEnabled(False)
        # self.sendfirst.setEnabled(False)
        # self.sendsecond.setEnabled(False)
        # self.closeAll.setEnabled(False)
        # self.openAll.setEnabled(False)
        # # self.openSecondPump.setEnabled(False)
        # self.setSeedCurrent.setEnabled(False)

    def enablePortSet(self):
        pass
        # self.setPortButton.setEnabled(True)
        # self.closePortButton.setEnabled(False)
        # self.baundrateMenu.setEnabled(True)
        # self.portEdit.setEnabled(True)
        # # self.startButton.setEnabled(False)


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

    def setPowerShowList(self,lst):
        self.powerShow.powerList = lst
        self.powerShow.updateFigure()

    def set_queue(self, queue):
        self.queue = queue

    def set_end_cmd(self, end_cmd):
        self.end_cmd = end_cmd

    # def set_autoscroll(self, value):
    #     self.autoscroll = value

    def set_port(self, value):
        self.portEdit.clear()
        self.portEdit.insert(value)

    def getSrcPort(self):
        self.lastpick['srcPort'] = self.portEdit.currentIndex()
        return self.portEdit.currentText()

    def getSrcBaudrate(self):
        self.lastpick['srcBaud'] = self.baundrateMenu.currentIndex()
        return self.baundrateMenu.currentText()[:-5]

    def getPumpPort(self):
        self.lastpick['pumpPort'] = self.portUI.portPump.currentIndex()
        return self.portUI.portPump.currentText()

    def getPumpBaudrate(self):
        self.lastpick['pumpBaud'] = self.portUI.baundratePump.currentIndex()
        return self.portUI.baundratePump.currentText()[:-5]

    # def getTempPort(self):
    #     self.lastpick['tempPort'] = self.portUI.portTemp.text()
    #     return self.portUI.portTemp.text()

    # def getTempBaudrate(self):
    #     self.lastpick['tempBaud'] = self.portUI.portTemp.currentIndex()
    #     return self.portUI.portTemp.currentText()[:-5]

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

    def updataFigure(self,newtime,power):
        # self.setCurrentValue(currentValue, timeValue)
        self.painter.XYaxit(newtime,power)
        self.painter.update_figure()

        # print('update?')
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

    def emit_br_src_changed(self, value):
        baudrate = self.baundrateMenu.itemText(value)[:-5]
        self.baudrate_src_changed.emit(baudrate)

    def emit_br_pump_changed(self, value):
        baudrate = self.baundrateMenu.itemText(value)[:-5]
        self.baudrate_pump_changed.emit(baudrate)

    # def emit_br_temp_changed(self, value):
    #     baudrate = self.baundrateMenu.itemText(value)[:-5]
    #     self.baudrate_temp_changed.emit(baudrate)

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
            self.startSrcModel.emit(self.srcModelstarted)
            self.srcModelstarted = True
            self.startPumpModel.emit(self.pumpModelstarted)
            self.pumpModelstarted = True
            # self.startTempModel.emit(self.tempModelstarted)
            # self.tempModelstarted = True
            self.emitUsername.emit(self.user.getName())
            print('emit username:',self.user.getName())
        else:
            self.toolBox.setTabEnabled(1,False)
            self.toolBox.setTabEnabled(2,False)
            self.toolBox.setTabEnabled(3,False)
            self.powerRecord.setUserID('NoneUser')
        print('use in view:',self.user.getName())

    def lastLogSave(self):
        self.last.saveLast(self.lastpick)

# class PortWidget(QWidget):
#     """docstring for PortWidget"""
#     def __init__(self):
#         super(PortWidget, self).__init__()
#         # self.ui = (self)
#         ui = PortUI()
#         ui.setupUi(self)
#         menuItem = ['300 baud','1200 baud',
#             '2400 baud','4800 baud','9600 baud',
#             '19200 baud','38400 baud','57600 baud',
#             '115200 baud','230400 baud','250000 baud']
#         ui.baundrateSource.addItems(menuItem)
#         ui.baundratePump.addItems(menuItem)
#         ui.baundrateTemp.addItems(menuItem)
#         self.ui = ui




# class PaintArea(QWidget):
#     """docstring for PaintArea"""
#     def __init__(self):
#         super(PaintArea, self).__init__()
#         self.setPalette(QPalette(Qt.white))
#         self.setAutoFillBackground(True)
#         self.setMinimumSize(500,400)
#         self.text = u'这个地方是绘图区域'
#         self.pen = QPen(Qt.black,1)
#         self.brush = QBrush()
#         self.font = QFont('arial', 15)
#         self.pList = list()
#         self.initTime = time.time()
#         #print('self.pList:',self.pList)

#     def paintEvent(self,event):
#         #pList = [int().from_bytes(x,'big') for x in self.pList]
#         pList =self.pList
#         #print('调用paintEvent:',len(pList),',event:',event)
#         p = QPainter(self)
#         #print('p=',p)
#         if len(pList) > 1:
#             p.translate(180,180)
#             p.setWindow(-10,-10,50,10)
#             qPointList = [QPointF(c[0] - self.initTime,c[1]) for c in pList]
#             #需要判断一下绘图范围
#             print(qPointList)
#             p.setPen(self.pen)
#             p.setBrush(self.brush)
#             qPointlast = QPointF(0,0)
#             for qpPoint in qPointList:
#                 #print('point:',qpPoint,qPointlast)
#                 p.drawLine(qpPoint,qPointlast)
#                 qPointlast = qpPoint

#         else:
#             self.drawText(event,p)

#     def plotupdate(self):
#         self.update()

#     def drawText(self,event,qp):
#         qp.setPen(QColor(168, 34, 3))
#         qp.setFont(QFont('微软雅黑', 20))
#         qp.drawText(event.rect(), Qt.AlignCenter, self.text)

#     def getpList(self, pList):
#         self.pList = pList
#         self.text = u'开始缓存电流数据'
#         #return self.pList
