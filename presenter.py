#!/usr/bin/env python
# coding=utf-8

# from time import sleep
# from model import Model
from PyQt5.QtCore import QObject
from model.modelsource import ModelSource
from model.modelpump import ModelPump
# from modeltemp import ModelTemp
from functools        import partial
from model.toolkit import portGard
from queue import Queue

class Presenter(QObject):

    def __init__(self, view):
        super(Presenter, self).__init__()
        self.__view = view
        self.__view.show()
        self.lineTextQueue = Queue()
        self.startPumpModel()
        self.__view.set_queue(self.lineTextQueue)
        self.__view.update_gui()
        self.__view.set_end_cmd(self.end_cmd)
        self.baundratPort = ()


    def startPumpModel(self):
        # if self.pumpModel == False and self.pumpModel.is_alive() == False:
        self.pumpModel = ModelPump()
        # self.guard.getmodels(self.pumpModel)
        self.pumpModel.set_queue(self.lineTextQueue)
        self.pumpModel.begin()
        self.pumpModel.start()
        self.setPumpSignals()

    def setPumpSignals(self):
        #Port part
        self.__view.tabBoxUI.openPort.clicked.connect(self.openPump)
        self.__view.setBaundratePortSignal.connect(self.setBaundratePort)
        self.__view.tabBoxUI.closePort.clicked.connect(self.pumpModel.closePort)
        self.__view.tabBoxUI.openPlatform.clicked.connect(self.pumpModel.openPlatform)
        self.__view.tabBoxUI.closePlatform.clicked.connect(self.pumpModel.closePlatform)
        self.__view.tabBoxUI.setCurrent.clicked.connect(self.setCurrent)
        #plot signal
        self.pumpModel.updatePowerShow.connect(self.__view.setPowerShowDict)
        self.pumpModel.emitPlot.connect(self.__view.updataFigure)
        self.pumpModel.beginPlot.connect(self.__view.painter.clearPlotList)
        self.__view.powerLog.beginTimeSignal.connect(self.pumpModel.setStartTime)
        self.__view.tabBoxUI.logButton.clicked.connect(self.pumpModel.setBeginPlotTime)
        self.__view.powerLog.sqlTableName.connect(self.pumpModel.creatPlot)
        self.__view.powerLog.stopSavePower.connect(self.pumpModel.setSaveStop)
        # self.__view.emitUsername.connect(self.pumpModel.setUsername)
        # self.__view.setbaundratePump.connect(self.pumpModel.baundrateIndexChange)
        # self.__view.setportPump.connect(self.pumpModel.portPump)

    def openPump(self):

        port , baudrate = self.__view.getBaundratePort()
        print('openPump', port , baudrate )
        self.pumpModel.setBaundratePort(port, baudrate)


    def setBaundratePort(self, port, baundrate):
        if self.baundratPort != (port, baundrate):
            self.pumpModel.setBaundratePort(port,baundrate)
            self.baundratPort = (port, baundrate)
            # self.pumpModel.set_br(baudrate)

    def setCurrent(self):
        current = self.__view.tabBoxUI.currentSpin.value()
        self.pumpModel.setCurrent(current)


    def closePort(self,model):
        # canState = self.__view.enableClosePort()
        canState = True
        if canState:
            model.closePort()
            self.__view.afterClosePort()
        else:
            print('未成功关闭')

    def end_cmd(self):
        if self.pumpModel:
            self.pumpModel.stop()
        self.__view.lastLogSave()




