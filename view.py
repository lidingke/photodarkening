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

from PyQt5.QtGui       import QPixmap

from queue              import Queue
from functools        import partial
import time

#plot PaintArea class
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QLineF
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush

class View(QWidget):

    send_data           = pyqtSignal(object)
    baudrate_changed    = pyqtSignal(object)
    #eol_changed         = pyqtSignal(object)
    port_changed        = pyqtSignal(object)
    seedPulseChanged = pyqtSignal(object)
    seedFreValueChanged = pyqtSignal(object)
    seedPulseFreChanged = pyqtSignal(object)

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
        self.buttonMinimumWidth = 100
        self.__initUI()




    def __initUI(self):
        #main box
        self.mainBox = QVBoxLayout(self)#使用垂直布局类
        gbox1 = QGroupBox()
        gbox2 = QGroupBox('启动顺序：\
            （串口）——（激光器）——（一级泵浦）——（二级泵浦）')
        gbox3 = QGroupBox()
        gbox4 = QGroupBox()
        gbox5 = QGroupBox()
        #self.menuBox = QHBoxLayout()
        self.setBox = QHBoxLayout(gbox2)
        self.toolBox = QTabWidget()
        self.toolBox.addTab(gbox1,'用户登录')
        self.toolBox.addTab(gbox2,'启动设置')
        self.toolBox.addTab(gbox3,'系统设置')
        self.toolBox.addTab(gbox4,'数据导出')
        self.toolBox.addTab(gbox5,'帮助')
        self.toolBox.setMaximumSize(10000,200)
        self.toolBox.resize(1200,200)
        self.showBox = QHBoxLayout()

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
        self.setBox.addLayout(seedBox)
        self.setBox.addLayout(firstPumpBox)
        self.setBox.addLayout(secondPumpBox)
        self.setBox.addStretch()
        #
        # self.showBox.addLayout(cmdBox)

        self.openPortButton = QPushButton('openPortButton')
        self.openPortButton.setEnabled(True)
        self.openPortButton.setMinimumWidth(self.buttonMinimumWidth)
        self.setPortButton = QPushButton('setPortButton')
        self.setPortButton.setMinimumWidth(self.buttonMinimumWidth)
        self.setPortButton.setEnabled(False)

        self.closePortButton = QPushButton('closePortButton')
        self.closePortButton.setMinimumWidth(self.buttonMinimumWidth)
        self.closePortButton.setEnabled(False)

        #self.openPortButton.setCheckable(True)
        #self.openPortButton.clicked.connect(partial(self.emit_send_command,'openport'))
        portBox.addWidget(self.openPortButton, 0, 0)
        portBox.addWidget(self.setPortButton, 1, 0)
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
        self.baundrateMenu.setCurrentIndex(4)
        portBox.addWidget(self.baundrateMenu, 1, 1)
        #port select
        portLabel = QLabel('Port: ')
        portLB = QHBoxLayout()
        portBox.addWidget(portLabel, 2, 0)
        self.portEdit = QLineEdit()
        self.portEdit.setEnabled(False)
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
        #self.setSeedFreValue.valueChanged.connect(self.emitWriteSeedFre)
        seedFreBox.addWidget(self.setSeedFreValue)
        seedBox.addLayout(seedPluseBox)
        seedBox.addLayout(seedFreBox)
        #seedBox.addStretch()

        # amp select
        self.openFirstPump = QPushButton('openall')
        self.openFirstPump.setMinimumWidth(self.buttonMinimumWidth)
        self.openFirstPump.setEnabled(False)
        #.setEnabled(True)
        #self.openFirstPump.clicked.connect(partial(self.emit_send_command,'openfirstpump'))
        firstPumpBox.addWidget(self.openFirstPump)
        self.openSecondPump = QPushButton('opensecondpump')
        self.openSecondPump.setMinimumWidth(self.buttonMinimumWidth)
        self.openSecondPump.setEnabled(False)
        self.openSecondPump.clicked.connect(partial(self.emit_send_command,'opensecondpump'))
        secondPumpBox.addWidget(self.openSecondPump)

        firstPumpLabel=QLabel('一级泵浦调节')
        secPumpLabel=QLabel('二级泵浦调节')
        self.firstpumpSet = QSpinBox(self)
        self.secondpumpSet = QSpinBox(self)
        self.firstpumpSet.setEnabled(False)
        self.secondpumpSet.setEnabled(False)
        firstPumpBox.addWidget(firstPumpLabel)
        secondPumpBox.addWidget(secPumpLabel)
        firstPumpBox.addWidget(self.firstpumpSet)
        secondPumpBox.addWidget(self.secondpumpSet)
        firstPumpBox.addStretch()
        secondPumpBox.addStretch()
        #self.resize(250, 150)
        #tool init
        widget1=QWidget()
        widget2=QWidget()


        #vboxMenu.addWidget(painter)
        #空出部分以供后面补充
        vboxMenu = QHBoxLayout(gbox1)
        vboxMenu.addWidget(widget1)
        vboxShow = QHBoxLayout(gbox3)
        vboxShow.addWidget(widget2)



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
        self.editer.setMaximumSize(300,400)
        cmd_btn.setMaximumSize(300,400)
        self.cmd_edit.setMaximumSize(300,400)
        #painter plot
        self.painter = PaintArea()
        self.showBox.addLayout(cmdBox)
        self.showBox.addWidget(self.painter)

        # setSeedPlot = QPushButton('plot')
        # setSeedPlot.clicked.connect(self.Button2Plot)
        # seedBox.addWidget(setSeedPlot)

        self.mainBox.addWidget(self.toolBox)
        self.mainBox.addLayout(self.showBox)



        self.setLayout(self.mainBox)
        self.setWindowTitle("光子暗化平台软件")

    def show_error(self, value):
        msg = QMessageBox(
                QMessageBox.NoIcon, 'Error occured.', value, QMessageBox.Ok)
        msg.exec()

    def afterOpenModel(self):
        self.openPortButton.setEnabled(False)
        self.setPortButton.setEnabled(True)
        self.closePortButton.setEnabled(True)
        self.baundrateMenu.setEnabled(True)
        self.portEdit.setEnabled(True)

    def afterOpenPort(self):

        self.openSeedButton.setEnabled(True)
        self.setSeedPulse.setEnabled(True)
        self.setSeedFreValue.setEnabled(True)
        self.firstpumpSet.setEnabled(True)
        self.secondpumpSet.setEnabled(True)
        self.openFirstPump.setEnabled(True)
        self.openSecondPump.setEnabled(True)


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
        return self.portEdit.text()

    def getBaudrate(self):
        return self.baundrateMenu.currentText()[:-5]

    def get_cmd(self):
        return self.cmd_edit.text()



    # def plotListGet(self):
    #     return self.currentValueList

    def setCurrentValue(self, currentValue):
        if currentValue is not None:
            self.currentValueList.append(currentValue)
            self.painter.getpList(self.currentValueList)
            self.painter.plotupdate()

    def Button2Plot(self):
        self.painter.plotupdate()

    def closeEvent(self, event):
        self.end_cmd()
        QWidget.closeEvent(self, event)
        print('exit')

    def beginGui(self):
        self.update()

    def update_gui(self):
        self.process_incoming()
        self.update()

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
        self.seedPulseChanged.emit(self.setSeedPulse.text())

    def emitWriteSeedFre(self):
        self.seedFreValueChanged.emit(self.setSeedFreValue.text())

    def emitSeedPulseAndFre(self):
        seedPulseAndFre = [self.setSeedPulse.text(),self.setSeedFreValue.text()]
        self.seedPulseFreChanged.emit(seedPulseAndFre)



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
