#!/usr/bin/env python
# coding=utf-8

from time import sleep
from model import Model

class Presenter:

    def __init__(self, view):
# 线程只能start一次。
# 为了避免多次start新线程，在初始化时就开好线程，程序结束时关闭

        self.__view = view
        self.__view.show()

        self.__view.openPortButton.clicked.connect(self.modelBegin)
        self.__view.closePortButton.clicked.connect(self.closeModel)
        self.__view.setPortButton.clicked.connect(self.setPort)
        #sleep(30)
        #self.modelBegin()
        # Run communication and start thread

        self.__view.update_gui()

    def end_cmd(self):
        self.__model.stop()

    def modelBegin(self):
        self.__model = Model()
        print('===openPort===')
        self.__model.begin()

        self.__view.set_queue(self.__model.get_queue())
        self.__view.set_end_cmd(self.end_cmd)
        self.__view.set_port(self.__model.get_port())

        self.__model.start()
        self.setSignals()
        self.__view.setPortButton.setEnabled(True)
        self.__view.closePortButton.setEnabled(True)
        self.__view.baundrateMenu.setEnabled(True)
        self.__view.portEdit.setEnabled(True)
        self.__view.openPortButton.setEnabled(False)


    def setSignals(self):
        #signals between view and model
        # openPortButton\setPortButton\closePortButton\openSeedButton
        #self.__view.setPortButton.

        # Signal connection
        # self.__view.baudrate_changed.connect(self.__model.set_br)
        # self.__view.port_changed.connect(self.__model.set_port)
        self.__view.send_data.connect(self.__model.write)
        self.__model.error.connect(self.__view.show_error)
        self.__model.cValue.connect(self.__view.setCurrentValue)
        # self.__view.seedPulseChanged.connect(self.__model.writeSeedPulse)
        # self.__view.seedFreValueChanged.connect(self.__model.writeSeedFre)
        self.__view.seedPulseFreChanged.connect(self.__model.writeSeedPulseAndFre)
        self.__view.openAll.clicked.connect(self.__model.openpaltform)
        self.__view.firstPumpChanged.connect(self.__model.writeFirstPumpCurrent)
        self.__view.secondPumpChanged.connect(self.__model.writesecondPumpCurrent)

    def closeModel(self):
        pass

    def setPort(self):
        newPort = self.__view.getPort()
        newBaud = self.__view.getBaudrate()
        oldPort = self.__model.get_port()
        oldBaud = self.__model.get_br()
        if newPort != oldPort:
            print('portnewold:',newPort,oldPort)
            self.__model.set_port(newPort)
        # if newBaud is not oldBaud:
            self.__model.set_br(newBaud)
            self.__model.reSetPort()
        if self.__model.isPortOpen():
            self.__view.afterOpenPort()





