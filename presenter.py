#!/usr/bin/env python
# coding=utf-8

# from time import sleep
# from model import Model
<<<<<<< HEAD
# from modelsource import ModelSource
from modelpump import ModelPump
=======
from model.modelsource import ModelSource
from model.modelpump import ModelPump
>>>>>>> 147d7cd378f5938df49e817d03989076a4e8bb01
# from modeltemp import ModelTemp
from functools        import partial
from model.toolkit import portGard

class Presenter:

    def __init__(self, view):

        self.__view = view
        self.__view.show()
        self.guard = portGard()
        self.__view.set_queue(self.guard.getQueue())
        # self.__view.startSrcModel.connect(self.startSrcModel)
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



    # def startSrcModel(self,started):
    #     if started == True:
    #         return
    #     self.srcModel = ModelSource()
    #     self.guard.getmodels(self.srcModel)
    #     self.srcModel.set_queue(self.guard.getQueue())
    #     self.srcModel.begin()
    #     self.srcModel.start()
    #     self.setSourceSignals()
    #     # self.__view.set_queue(self.srcModel.get_queue())
    #     # self.__view.enablePortSet()
    #     # self.__view.setCurrentValue(self.srcModel.getcurrentValueList(),self.srcModel.getcurrentTimeList())
    #     # self.srcModel.initPort(self.__view.getPort(),self.__view.getBaudrate())
    #     # self.__view.set_port(self.srcModel.get_port())

    def startPumpModel(self,started):
        if started == True:
            return
        self.pumpModel = ModelPump()
        self.guard.getmodels(self.pumpModel)
        self.pumpModel.set_queue(self.guard.getQueue())
        self.pumpModel.begin()
        self.pumpModel.start()
        self.setPumpSignals()

        # self.__view.set_queue(self.pumpModel.get_queue())
        # self.__view.set_end_cmd(self.end_cmd)
        # self.__view.enablePortSet()
    # def startTempModel(self,started):
    #     if started == True:
    #         return
    #     self.tempModel = ModelTemp()
    #     self.tempModel.start()
    #     self.setTempSignals()
    #     self.tempModel.begin()
    #     # self.__view.set_queue(self.tempModel.get_queue())
    #     # self.__view.set_end_cmd(self.end_cmd)
    #     # self.__view.enablePortSet()

    # def setSourceSignals(self):
    #     self.__view.portUI.openportSource.clicked.connect(partial(self.setSrcPort,self.srcModel))
    #     self.__view.portUI.closeportSource.clicked.connect(partial(self.closePort,self.srcModel))
    #     self.srcModel.seedCurrentSignal.connect(self.__view.seedCurrentSet)
    #     self.srcModel.seedPulseSignal.connect(self.__view.seedPulseSet)
    #     self.srcModel.seedFrequeceSignal.connect(self.__view.seedFrequeceSet)
    #     self.__view.seedPulseFreChanged.connect(self.srcModel.setSeed)
    #     self.__view.openAll.clicked.connect(self.srcModel.openAllThread)
    #     self.__view.closeAll.clicked.connect(self.srcModel.closeAll)

    def setPumpSignals(self):
        pass
        """
        self.__view.portUI.openportPump.clicked.connect(partial(self.setPumpPort,self.pumpModel))
        self.__view.portUI.closeportPump.clicked.connect(partial(self.closePort,self.pumpModel))
        self.pumpModel.firstCurrentSignal.connect(self.__view.firstCurrentSet)
        self.pumpModel.secondCurrentSignal.connect(self.__view.secondCurrentSet)
        self.__view.firstPumpChanged.connect(self.pumpModel.writeFirstPumpCurrent)
        self.__view.secondPumpChanged.connect(self.pumpModel.writesecondPumpCurrent)
        self.__view.openAll.clicked.connect(self.pumpModel.openAllThread)
        self.__view.closeAll.clicked.connect(self.pumpModel.closeAll)
        self.pumpModel.plotPower.connect(self.__view.updataFigure)
        self.__view.powerRecord.beginTimeSignal.connect(self.pumpModel.setStartTime)
        self.__view.powerRecord.seButton.clicked.connect(self.pumpModel.setBeginPlotTime)
        self.__view.powerRecord.sqlTableName.connect(self.pumpModel.creatPlot)
        self.__view.powerRecord.stopSavePower.connect(self.pumpModel.setSaveStop)
        self.pumpModel.beginPlot.connect(self.__view.painter.clearPlotList)
        self.__view.emitUsername.connect(self.pumpModel.setUsername)
        self.pumpModel.updatePowerShow.connect(self.__view.setPowerShowList)
        """
    # def setSignals(self):
    #     # self.__view.send_data.connect(self.srcModel.write)
    #     self.__view.powerRecord.beginTimeSignal.connect(self.srcModel.setStartTime)
    #     self.__view.powerRecord.seButton.clicked.connect(self.srcModel.setBeginPlotTime)
    #     self.__view.powerRecord.sqlTableName.connect(self.srcModel.creatPlot)
    #     # self.srcModel.error.connect(self.__view.show_error)
        # self.srcModel.seedCurrentSignal.connect(self.__view.seedCurrentSet)
        # self.srcModel.seedPulseSignal.connect(self.__view.seedPulseSet)
        # self.srcModel.seedFrequeceSignal.connect(self.__view.seedFrequeceSet)
        # self.srcModel.firstCurrentSignal.connect(self.__view.firstCurrentSet)
        # self.srcModel.secondCurrentSignal.connect(self.__view.secondCurrentSet)
        # self.__view.seedPulseFreChanged.connect(self.srcModel.writeSeedPulseAndFre)
        #signals between view and model
        # startButton\setPortButton\closePortButton\openSeedButton
        #self.__view.setPortButton.
        # Signal connection
        # self.__view.baudrate_changed.connect(self.srcModel.set_br)
        # self.__view.port_changed.connect(self.srcModel.set_port)
        # self.__view.seedPulseChanged.connect(self.srcModel.writeSeedPulse)
        # self.__view.seedFreValueChanged.connect(self.srcModel.writeSeedFre)
    # def closeModel(self):
    #     self.end_cmd()

    # def setSrcPort(self,model):
    #     newPort = self.__view.getSrcPort()
    #     newBaud = self.__view.getSrcBaudrate()
    #     oldPort = model.get_port()
    #     oldBaud = model.get_br()
    #     #isPortOpen = self.srcModel.isPortOpen()
    #     if newPort != oldPort:
    #         print('portnewold:',newPort,oldPort)
    #         model.set_port(newPort)
    #     # if newBaud is not oldBaud:
    #         model.set_br(newBaud)
    #         model.reSetPort()
    #     if model.isPortOpen():
    #         self.__view.afterOpenPort()
    #     else:
    #         print('reopenport')
    #         model.set_port(newPort)
    #     # if newBaud is not oldBaud:
    #         model.set_br(newBaud)
    #         model.reSetPort()
    #         if model.isPortOpen():
    #             self.__view.afterOpenPort()

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
        if model.isPortOpen():
            self.__view.afterOpenPort()
        else:
            print('reopenport')
            model.set_port(newPort)
        # if newBaud is not oldBaud:
            model.set_br(newBaud)
            model.reSetPort()
            if model.isPortOpen():
                self.__view.afterOpenPort()

    def closePort(self,model):
        # canState = self.__view.enableClosePort()
        canState = True
        if canState:
            model.closePort()
            self.__view.afterClosePort()
        else:
            print('未成功关闭')

    def end_cmd(self):
        if self.srcModel:
            self.srcModel.stop()
        # self.tempModel.stop()
        if self.pumpModel:
            self.pumpModel.stop()
        self.__view.lastLogSave()




