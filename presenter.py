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

        # self.__view.startButton.clicked.connect(self.modelBegin)
        self.__view.startModel.connect(self.modelBegin)

        # self.modelBegin()
        # self.__view.closePortButton.clicked.connect(self.closeModel)
        self.__view.setPortButton.clicked.connect(self.setPort)
        self.__view.closePortButton.clicked.connect(self.closePort)
        #sleep(30)
        #self.modelBegin()
        # Run communication and start thread

        self.__view.update_gui()

    def end_cmd(self):
        self.__model.stop()
        self.__view.lastLogSave()

    def modelBegin(self,started):
        if started == True:
            return
        self.__model = Model()
        # self.__model.initPort(self.__view.getPort(),self.__view.getBaudrate())
        print('===openPort===')
        self.__model.begin()

        self.__view.set_queue(self.__model.get_queue())
        # self.__view.setCurrentValue(self.__model.getcurrentValueList(),self.__model.getcurrentTimeList())
        self.__view.set_end_cmd(self.end_cmd)
        # self.__view.set_port(self.__model.get_port())

        self.__model.start()
        self.setSignals()
        self.__view.enablePortSet()


    def setSignals(self):
        #signals between view and model
        # startButton\setPortButton\closePortButton\openSeedButton
        #self.__view.setPortButton.

        # Signal connection
        # self.__view.baudrate_changed.connect(self.__model.set_br)
        # self.__view.port_changed.connect(self.__model.set_port)
        self.__view.send_data.connect(self.__model.write)
        self.__view.powerRecord.beginTimeSignal.connect(self.__model.setStartTime)
        self.__view.powerRecord.seButton.clicked.connect(self.__model.setBeginPlotTime)
        self.__view.powerRecord.sqlTableName.connect(self.__model.creatPlot)
        self.__model.error.connect(self.__view.show_error)

        self.__model.plotPower.connect(self.__view.updataFigure)

        self.__model.seedCurrentSignal.connect(self.__view.seedCurrentSet)
        self.__model.seedPulseSignal.connect(self.__view.seedPulseSet)
        self.__model.seedFrequeceSignal.connect(self.__view.seedFrequeceSet)
        self.__model.firstCurrentSignal.connect(self.__view.firstCurrentSet)
        self.__model.secondCurrentSignal.connect(self.__view.secondCurrentSet)

        # self.__view.seedPulseChanged.connect(self.__model.writeSeedPulse)
        # self.__view.seedFreValueChanged.connect(self.__model.writeSeedFre)
        self.__view.seedPulseFreChanged.connect(self.__model.writeSeedPulseAndFre)
        self.__view.openAll.clicked.connect(self.__model.openAllThread)
        self.__view.firstPumpChanged.connect(self.__model.writeFirstPumpCurrent)
        self.__view.secondPumpChanged.connect(self.__model.writesecondPumpCurrent)
        self.__view.closeAll.clicked.connect(self.__model.closeAll)


    # def closeModel(self):
    #     self.end_cmd()

    def setPort(self):
        newPort = self.__view.getPort()
        newBaud = self.__view.getBaudrate()
        oldPort = self.__model.get_port()
        oldBaud = self.__model.get_br()
        #isPortOpen = self.__model.isPortOpen()
        if newPort != oldPort:
            print('portnewold:',newPort,oldPort)
            self.__model.set_port(newPort)
        # if newBaud is not oldBaud:
            self.__model.set_br(newBaud)
            self.__model.reSetPort()
        if self.__model.isPortOpen():
            self.__view.afterOpenPort()
        else:
            print('reopenport')
            self.__model.set_port(newPort)
        # if newBaud is not oldBaud:
            self.__model.set_br(newBaud)
            self.__model.reSetPort()
            if self.__model.isPortOpen():
                self.__view.afterOpenPort()

    def closePort(self):
        # canState = self.__view.enableClosePort()
        canState = True
        if canState:
            self.__model.closePort()
            self.__view.afterClosePort()
        else:
            print('未成功关闭')






