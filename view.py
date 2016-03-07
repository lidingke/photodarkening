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
from PyQt5.QtWidgets    import QComboBox
from PyQt5.QtWidgets    import QMessageBox
from PyQt5.QtWidgets    import QLCDNumber
from PyQt5.QtWidgets    import QSpinBox
from PyQt5.QtCore       import QTimer
from PyQt5.QtCore       import QObject
from PyQt5.QtCore       import pyqtSignal
from PyQt5.QtCore       import Qt
from PyQt5.QtGui       import QPainter
from PyQt5.QtGui       import QPixmap
from queue              import Queue
from functools        import partial
from paintArea import PaintArea

class View(QWidget):

    send_data           = pyqtSignal(object)
    baudrate_changed    = pyqtSignal(object)
    #eol_changed         = pyqtSignal(object)
    port_changed        = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)

        self.queue      = None
        self.end_cmd    = None
        self.autoscroll = True
        self.msg_sent   = False
        self.currentbaud = '9600 baud'
        self.currentport = 'com12'
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

        self.__initUI()

    def __initUI(self):
        #main box
        mainBox = QVBoxLayout(self)#使用垂直布局类
        menuBox = QHBoxLayout()
        setBox = QHBoxLayout()
        showBox = QHBoxLayout()

        #edit box
        cmdBox = QVBoxLayout()
        #cmd_hbox = QHBoxLayout()#使用水平布局类
        #lcdSliderBox = QHBoxLayout()
        stng_hbox = QHBoxLayout()
        port_hbox = QHBoxLayout()

        portSetBox = QVBoxLayout()
        cmdButtonBox = QVBoxLayout()
        valuelabelBox = QVBoxLayout()
        valueSetBox = QVBoxLayout()

        # Command box
        setBox.addLayout(portSetBox)
        setBox.addLayout(cmdButtonBox)
        setBox.addLayout(valuelabelBox)
        setBox.addLayout(valueSetBox)
        showBox.addLayout(cmdBox)

        mainBox.addLayout(menuBox)
        mainBox.addLayout(setBox)
        mainBox.addLayout(showBox)
        #mainBox.addLayout(port_hbox)
        #mainBox.addLayout(stng_hbox)

        userLabel = QLabel('用户')
        sysLabel = QLabel('系统')
        setbutLabel = QLabel('属性')
        menuBox.addWidget(userLabel)
        menuBox.addWidget(sysLabel)
        menuBox.addWidget(setbutLabel)

        cmd_btn = QPushButton('Send Command')
        cmd_btn.clicked.connect(self.emit_send_data)
        cmdButtonBox.addWidget(cmd_btn)
        cmd_btncr = QPushButton('sendcurrentcmd')
        cmd_btncr.clicked.connect(partial(self.emit_send_command,'sendcurrent'))
        cmdButtonBox.addWidget(cmd_btncr)

        # - Baudrate select
        self.br_menu = QComboBox()
        self.menuItem = ['300 baud','1200 baud',
            '2400 baud','4800 baud','9600 baud',
            '19200 baud','38400 baud','57600 baud',
            '115200 baud','230400 baud','250000 baud']
        self.br_menu.addItems(self.menuItem)
        self.br_menu.currentIndexChanged.connect(self.emit_br_changed)
        # Set default baudrate 9600
        self.br_menu.setCurrentIndex(4)
        stng_hbox.addWidget(self.br_menu)

        port_lbl = QLabel('Port: ')
        port_hbox.addWidget(port_lbl)
        self.port_edit = QLineEdit()

        self.port_edit.editingFinished.connect(self.changePort)
        port_hbox.addWidget(self.port_edit)
        portSetBox.addLayout(stng_hbox)
        portSetBox.addLayout(port_hbox)

        # lcd = QLCDNumber(self)
        firstLabel=QLabel('1st')
        secLabel=QLabel('2st')
        slider1 = QSpinBox(self)
        slider2 = QSpinBox(self)
        valuelabelBox.addWidget(firstLabel)
        valuelabelBox.addWidget(secLabel)
        valueSetBox.addWidget(slider1)
        valueSetBox.addWidget(slider2)
        # lcdSliderBox.addWidget(lcd)
        # lcdSliderBox.addWidget(slider)
        # slider.valueChanged.connect(lcd.display)
        #self.resize(250, 150)



        # Text edit area
        self.cmd_edit = QLineEdit()
        self.editer = QPlainTextEdit()
        cmdBox.addWidget(self.cmd_edit)
        cmdBox.addWidget(self.editer)
        #painter
        self.painter= PaintArea()
        showBox.addWidget(self.painter)


        # Settings area


        # - Autoscroll
        # chk_btn = QCheckBox('Autoscroll')
        # chk_btn.stateChanged.connect(self.set_autoscroll)
        # stng_hbox.addWidget(chk_btn)
        # stng_hbox.addStretch(1)




        self.setLayout(mainBox)

    def show_error(self, value):
        msg = QMessageBox(
                QMessageBox.NoIcon, 'Error occured.', value, QMessageBox.Ok)
        msg.exec()

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
        self.port_edit.insert(value)

    def get_cmd(self):
        return self.cmd_edit.text()

    # def set_eol(self, value):
    #     self.eol_menu.setCurrentIndex(value)

    def closeEvent(self, event):
        self.end_cmd()
        QWidget.closeEvent(self, event)
        print('exit')

    def update_gui(self):
        self.process_incoming()
        self.update()

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.editer.appendPlainText(str(msg))
                #if self.autoscroll:
                self.editer.ensureCursorVisible()
                self.scroll_down()
            except Queue.empty:
                pass

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

    # def emit_send_current(self):
    #     self.send_data.emit('sendcurrent')

    def emit_send_command(self,command):
        self.send_data.emit(command)
        self.cmd_edit.clear()

    def emit_br_changed(self, value):
        baudrate = self.br_menu.itemText(value)[:-5]
        self.baudrate_changed.emit(baudrate)

    # def emit_eol_changed(self, value):
    #     self.eol_changed.emit(value)

    def emit_port_changed(self):
        self.port_changed.emit(self.port_edit.text())
