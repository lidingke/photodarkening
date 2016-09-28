#!/usr/bin/env python
# coding=utf-8

# from time import sleep
# from model import Model
from model.modelsource import ModelSource
from model.modelpump import ModelPump
# from modeltemp import ModelTemp
from functools        import partial
from model.toolkit import portGard

class Presenter:

    def __init__(self, view):
        self.srcModel = False
        self.pumpModel = False
        self.__view = view
        self.__view.show()
        self.guard = portGard()
        self.__view.set_queue(self.guard.getQueue())
        self.__view.startSrcModel.connect(self.startSrcModel)
        self.__view.startPumpModel.connect(self.startPumpModel)
        # self.__view.startTempModel.connect(self.startTempModel)
        self.__view.update_gui()
        self.__view.set_end_cmd(self.end_cmd)

        # self.guard.getmodels(self.)

        #sleep(30)
        #self.modelBegin()
        # Run communication and start thread
        # self.__view.startButton.clicked.connect(self.modelBegin)
        # self.modelBegin()
        # self.__view.closePortButton.clicked.connect(self.closeModel)



    def startSrcModel(self,started):
        if started == True:
            return
        self.srcModel = ModelSource()
        self.guard.getmodels(self.srcModel)
        self.srcModel.set_queue(self.guard.getQueue())
        self.srcModel.begin()
        self.srcModel.start()
        self.setSourceSignals()


    def startPumpModel(self,started):
        if started == True:
            return
        self.pumpModel = ModelPump()
        self.guard.getmodels(self.pumpModel)
        self.pumpModel.set_queue(self.guard.getQueue())
        self.pumpModel.begin()
        self.pumpModel.start()
        self.setPumpSignals()


    def setSourceSignals(self):
        self.__view.portUI.openportSource.clicked.connect(partial(self.setSrcPort, self.srcModel))
        self.__view.portUI.closeportSource.clicked.connect(partial(self.closePort, self.srcModel))
        self.srcModel.seedSignal.connect(self.__view.seedSignalSet)
        self.__view.seedPulseFreChanged.connect(self.srcModel.setSeed)
        self.__view.openAll.clicked.connect(self.srcModel.openAllThread)
        self.__view.closeAll.clicked.connect(self.srcModel.closeAll)

    def setPumpSignals(self):
        self.__view.portUI.openportPump.clicked.connect(partial(self.setPumpPort,self.pumpModel))
        self.__view.portUI.closeportPump.clicked.connect(partial(self.closePort,self.pumpModel))
        self.pumpModel.firstCurrentSignal.connect(self.__view.firstCurrentSet)
        self.pumpModel.secondCurrentSignal.connect(self.__view.secondCurrentSet)
        self.__view.firstPumpChanged.connect(self.pumpModel.writeFirstPumpCurrent)
        self.__view.secondPumpChanged.connect(self.pumpModel.writesecondPumpCurrent)
        self.__view.openAll.clicked.connect(self.pumpModel.openAllThread)
        self.__view.closeAll.clicked.connect(self.pumpModel.closeAll)
        # self.__view.portUI.openportTemp.clicked.connect(partial(self.setPumpPort,self.pumpModel))
        # self.__view.portUI.closeportTemp.clicked.connect(partial(self.closePort,self.pumpModel))
        self.pumpModel.plotPower.connect(self.__view.updataFigure)
        self.__view.powerRecord.beginTimeSignal.connect(self.pumpModel.setStartTime)
        self.__view.powerRecord.seButton.clicked.connect(self.pumpModel.setBeginPlotTime)
        self.__view.powerRecord.sqlTableName.connect(self.pumpModel.creatPlot)
        self.__view.powerRecord.stopSavePower.connect(self.pumpModel.setSaveStop)
        self.pumpModel.beginPlot.connect(self.__view.painter.clearPlotList)

        self.__view.emitUsername.connect(self.pumpModel.setUsername)
        self.pumpModel.updatePowerShow.connect(self.__view.setPowerShowList)


    def setSrcPort(self,model):
        newPort = self.__view.getSrcPort()
        newBaud = self.__view.getSrcBaudrate()
        oldPort = model.get_port()
        oldBaud = model.get_br()
        #isPortOpen = self.srcModel.isPortOpen()
        if newPort != oldPort:
            print('portnewold:',newPort,oldPort)
            model.set_port(newPort)
        # if newBaud is not oldBaud:
            model.set_br(newBaud)
            model.reSetPort()
        # if model.isPortOpen():
        #     self.__view.afterOpenPort()
        else:
            print('reopenport')
            model.set_port(newPort)
        # if newBaud is not oldBaud:
            model.set_br(newBaud)
            model.reSetPort()
            # if model.isPortOpen():
            #     self.__view.afterOpenPort()

    def setPumpPort(self,model):
        newPort = self.__view.getPumpPort()
        newBaud = self.__view.getPumpBaudrate()
        oldPort = model.get_port()
        oldBaud = model.get_br()
        #isPortOpen = self.srcModel.isPortOpen()
        if newPort != oldPort:
            print('portnewold:',newPort,oldPort)
            model.set_port(newPort)
        # if newBaud is not oldBaud:
            model.set_br(newBaud)
            model.reSetPort()
        # if model.isPortOpen():
        #     self.__view.afterOpenPort()
        else:
            print('reopenport')
            model.set_port(newPort)
        # if newBaud is not oldBaud:
            model.set_br(newBaud)
            model.reSetPort()
            # if model.isPortOpen():
            #     self.__view.afterOpenPort()

    def closePort(self,model):
        # canState = self.__view.enableClosePort()
        canState = True
        if canState:
            model.closePort()
        else:
            print('未成功关闭')

    def end_cmd(self):
        if self.srcModel:
            self.srcModel.stop()
        # self.tempModel.stop()
        if self.pumpModel:
            self.pumpModel.stop()
        self.__view.lastLogSave()




