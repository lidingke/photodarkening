#!/usr/bin/env python
# coding=utf-8

# System imports
import  threading
import  queue
#from    time                import sleep
import time
import logging
# from    sys                 import exit
import pickle
import sqlite3
import pdb
# PyQt5 imports
from    PyQt5.QtCore        import pyqtSignal
from    PyQt5.QtCore        import QObject
from    PyQt5.QtCore        import QTime
# PySerial imports
import  serial

from toolkit import HexSplit
# from    serial.serialutil   import SerialException
# from database import DataHand

class Model(threading.Thread, QObject):

    # This signal emitted when program fail to read serial port (self.port)
    error = pyqtSignal(object)
    cValue = pyqtSignal(object)
    seedCurrentSignal = pyqtSignal(object)
    seedPulseSignal = pyqtSignal(object)
    seedFrequeceSignal = pyqtSignal(object)
    firstCurrentSignal = pyqtSignal(object)
    secondCurrentSignal = pyqtSignal(object)
    plotPower = pyqtSignal(object)

    def __init__(self):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        # Queue with data (lines) received from serial port
        self.setDaemon(True)#deamon thread, close as same as father thread
        self.printText      = queue.Queue()
        self.currentValueList      = list()
        self.currentTimeList = list()
        # Communications settings
        self.port       = 'com1'
        self.br         = 9600
        self.timeout    = 0.001
        # Line ending id
        #self.eol        = 0
        self.username = 'nobody'
        # PySerial object
        self.ser        = None
        # Flag for main cycle
        self.running    = True
        self.ti0 = time.time()#set record start time
        self.startRecord = False# set start record statues
        self.tempdetector = TempDetector()
        self.__init__slaveStatus()

        with open('msg.pickle', 'rb') as f:
            entry = pickle.load(f)
        self.msgDictHex = entry['msgDictHex']
        self.msgDictStr = entry['msgDictStr']
        self.sendmsgrec = entry['sendmsgrec']
        self.entry = entry

        # self.datahand = DataHand('powerdata.db')
        # self.datahand.username = self.username

        # self.datahand.initSql()
        # self.datahand.connectSql()

    def __init__slaveStatus(self):
        self.isSeedOpen = True
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
        self.ti0 = 0

    def run(self):
        '''
        Run thread.
            Method representing the thread's activity.
            You may override this method in a subclass. The standard run() method
            invokes the callable object passed to the object's constructor as the
            target argument, if any, with sequential and keyword arguments taken
            from the args and kwargs arguments, respectively.
        '''
        while self.running:
            if self.ser:
                data = self.analysisbit()
                if data :
                    self.coreMsgProcess(data)
            time.sleep(self.timeout)

            #self.printShow('running:',self.running)
                #self.printShow('Model start',self.ser)
                #sleep(1)
                #data = self.readline()
                #ser = self.ser
                    #self.printShow('Error occured while reading data.')
                #try:runrun
                    #self.printShow('lendata',len(data))
                    #self.printShow('data:',data)
                    #self.printShow('上位机接收：',data)
                    # self.printText.put(data.strip())
                # except Exception as e:
                #     data=b-1

    def stop(self):
        '''
        Stop thread.
        '''
        self.printShow('stop thread Model and close serial')

        if self.ser:
            self.ser.timeout = 0
            # change to non blocking mode and then close
            self.ser.close()
        # self.ser = None
        self.running = False
        # self.datahand.closeConnect()

    def printShow(self,*value,ifprint = True,text = True,nobyte = True):
        ''' print to CMD and text plain
        '''
        printlist = list()
        textlist = list()
        if value:
            for x in value:
                if type(x) == str:
                    printlist.append(x)
                    textlist.append(x)
                elif type(x) == int:
                    printlist.append(str(x))
                    textlist.append(str(x))
                elif type(x) == bytes:
                    if nobyte == True:
                        textlist.append(x.hex())
                        # printlist.append(':'+str(x))
                    elif nobyte == False:
                        textlist.append(':'+str(x))
                    printlist.append(':'+str(x))
                else:
                    printlist.append(str(x))
                    textlist.append(str(x))
            if ifprint:
                print(''.join(printlist))
            if text:
                printText = ''.join(textlist)
                if printText != ':bytes':
                    self.printText.put(printText)

    def closePort(self):
        self.ser.close()

    def begin(self):
        '''
        Initializate PySerial object
        '''
        try:
            self.ser = serial.Serial(self.port, self.br, timeout=120)
        except serial.serialutil.SerialException:
            self.printShow('=== can not open the port ===')
            self.printShow('ser=',self.ser,text=False)
            #self.ser = serial.Serial(baudrate=self.br, timeout=120)
            #self.stop()


    def reSetPort(self):
        try:
            self.ser = serial.Serial(self.port, self.br, timeout=120)
            self.printShow(self.ser,text=False)
            self.printShow('port is open port name is ',self.port)
        except serial.serialutil.SerialException:
            self.printShow('=== can not open the port ===')
            self.ser = serial.Serial(baudrate=self.br, timeout=120)
            self.printShow('ser=',self.ser)


            #self.stop()

    def isPortOpen(self):
        if self.ser:
            ser = self.ser
            return ser.isOpen()
        else:
            return False

    def setBeginPlotTime(self):
        self.startRecord = True
        # self.ti0 = time.time()
        print('get ti0:',self.ti0)
        # self.datahand.initSqltabel(self.ti0,self.username)
        self.currentTimeList.clear()
        self.currentValueList.clear()

    def setStartTime(self,stime ):
        self.ti0 = stime

    # def self.printShowShow():
    #     """
    #     re define pirnt fun
    #     """
    #     pass
        # try:
        #     self.printShow(self.port,self.br)
        #     self.ser = serial.Serial(
        #             self.port, self.br, timeout=120
        #     )
        #     self.printShow(self.ser)
        #     return True
        # except SerialException:
        #     self.printShow('Fail to open default port.')
        #     #self.ser = serial.Serial(baudrate=self.br, timeout=120)
        #     time.sleep(1)
        #     # self.ser = serial.Serial(
        #     #         self.port, self.br, timeout=120
        #     # )
        #     self.stop()
        #     return False
        #self.printShow(self.ser)

#==============================================================================
# Get, Set port about message from view
#==============================================================================

    def get_queue(self):
        return self.printText

    def getcurrentValueList(self):
        return self.currentValueList

    def getcurrentTimeList(self):
        return self.currentTimeList

    def setSer(self,ser):
        self.ser = ser

    def set_port(self,port):
        self.port = port

    def set_br(self, baudrate):
        self.br = baudrate

        #self.ser.baudrate = self.br
        # if self.br is not baudrate:
        # if self.port is not port:
    # def reset_port(self, port):
    #     #self.ser.close()
    #     time.sleep(0.1)
    #     if self.port is not port:
    #         self.port = port
            #self.stop()
        #self.begin()
        #!!!
        #self.ser = serial.Serial( port, self.br, timeout=120)
        # try:
        #     if not self.ser._port_handle:
        #         self.printShow(self.ser._port_handle)

        #     self.ser.port = self.port
        #     self.ser.open()
        # except SerialException:
        #     self.emit_error('Can\'t open this port: ' + str(port) + '.')


    def get_msgDict(self):
        return self.msgDictHex

    def get_port(self):
        return self.port

    def getEntry(self):
        return self.entry

    def get_br(self):
        return self.br

    def get_ser(self):
        return self.ser

    # def set_eol(self, value):
    #     self.eol = value

    # def get_eol(self):
    #     return self.config['eol'][self.eol]

#==============================================================================
# PySerial communication
#==============================================================================

    def write(self, data):
        '''
        data to send
        '''
        if type(data) is str:
            if data[:3] == 'msg':
                dataSend = b''.fromhex(data[4:])
            else:
                dataSend = self.msgcoup(data)
        else:
            dataSend =data
        if dataSend:
            self.printShow('上位机发送:',dataSend,text =False)
            self.ser.write(dataSend)
        time.sleep(0.1)

                # print(data)
        #self.printShow(dataSend)
                # pdb.set_trace()data[4:]
    # def readline(self):
    #     try:
    #         data = self.ser.read(15)
    #     except Exception as e:
    #         raise e
    #     return data
            # if ser and ser.isOpen is True:
        # except Exception as e:
        #     raise e

    def readbit(self,ser):
        try:
            if ser:
                data = ser.read(1)
        except serial.serialutil.SerialException :
            time.sleep(1)
            data = b'-1'
        # except NoneType :
        #     time.sleep(1)
        #     data = b'-1'
        return data

    def msgcoup(self,msg):
        '''package a message if msg length > 6
        '''
        msg = self.msgDictHex.get(msg, b'-1')
        if msg is b'-1':
            return msg
        else:
            if len(msg) > 6:
                return msg
            else:
                return b'\xEB\x90'+msg+b'\x90\xEB'

    def analysisbit(self):
        '''
                return without package
                input bit data analysis
        '''
        # readlive = True
        # xebstatue = False
        # x90statue = False
        bitlist = list()
        while self.running:
            #self.printShow('keepbit')
            ser = self.ser
            databit = self.readbit(self.ser)
            if databit == b'\xeb':
                # self.printShow(databit,'1')
                databit = self.readbit(self.ser)
                if databit == b'\x90':
                    while True:
                        # self.printShow(databit,'2')
                        databit = self.readbit(self.ser)
                        if databit == b'\x90':
                            databit = self.readbit(self.ser)
                            data = b''.join(bitlist)
                            self.printShow(data)
                            return data
                        bitlist.append(databit)
            elif databit == b'\x9A':
                while True:
                    databit = self.readbit(self.ser)
                    if databit == b'\xA9':
                        databit = self.readbit(self.ser)
                        data = b''.join(bitlist)
                        self.printShow('received:',data,text = False)
                        return b'\x9A' + data
                    bitlist.append(databit)
        return None

    def coreMsgProcess(self,data):
        '''
        input message analysis and manage
        '''
        # if data == None:
        #     return '-1'
        # elif len(data) > 5:
        #     data = data[2:]
        #     data = data[:-2]
        # self.printShow(data[0:1],':',data[1:2],type(data[0]),type(data))
        if data[0:1] == b'\x01':
            # # ti =
            # if data[1:2] == b'\x11':
            #     pass
                # #current plot msg
                # #self.printShow(data,'12:',data[-2:])
                # currentValue = data[-2:].strip()
                # currentValue = int().from_bytes(currentValue,'big')/100
                # self.printShow('currentValue=',currentValue)
                # self.currentValueList.append(currentValue)
                # self.ti0 = 1 + self.ti0
                # self.currentTimeList.append(self.ti0)
                # self.emitPlot()
            if data[1:2] == b'\x00':
                # ==========
                #open and close seed
                #if data[2:3] == b'\x00\x00':
                # self.printShow('seed received',data, text =False,text=False)
                if data[2:3] == b'\x00':
                    if data[3:4] == b'\x01':
                        self.printShow('openseedreturn')
                        self.isSeedOpen = True
                    elif data[3:4] == b'\x00':
                        self.printShow('closeseedreturn')
                        self.isSeedOpen = False
                elif data[2:3] == b'\x10':
                        self.printShow('openseederror')
                        self.isSeedOpen = False
            elif data[1:2] == b'\x01':
                # ========
                #seed current value set \x01
                self.printShow('seed received',data, text =False)
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedcurrentre = False
                else:
                    self.seedcurrentre = True
                    #current
            elif data[1:2] == b'\x02':
                #seed pulse width
                self.printShow('seed received',data, text =False)
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedpulsere = False
                else:
                    self.seedpulsere = True
                    #current
            elif data[1:2] == b'\x03':
                #seed frequece set
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedfrequecere = False
                else:
                    self.seedfrequecere = True
                    #current
                self.printShow('seed received',data, text =False)
            elif data[1:2] == b'\x04':
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedcurrent = -1
                else:
                    self.seedcurrent = int().from_bytes(data[2:4],'big')

                #seed current value get
                self.printShow('seed received',data, text =False)
            elif data[1:2] == b'\x05':
                #seed pluse width read
                self.printShow('seed received',data, text =False)
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedpulse = -1
                else:
                    self.seedpulse = int().from_bytes(data[2:4],'big')
            elif data[1:2] == b'\x06':
                #seed frequece read
                self.printShow('seed received',data, text =False)
                if data[2:3] == b'\x10':
                    self.printShow('seederror')
                    self.seedfrequece = -1
                else:
                    self.seedfrequece = int().from_bytes(data[2:4],'big')
            else:
                return -1
        elif data[0:1] == b'\x02':
            if data[1:2] == b'\x00':
                if data[2:3] == b'\x0A':
                    if data[3:5] == b'\x00\x01':
                        self.printShow('openfirstpump')
                        self.isFirstPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        self.printShow('closefirstpump')
                        self.isFirstPumpOpen = False
                elif data[2:3] == b'\x0B':
                    if data[3:5] == b'\x00\x01':
                        self.printShow('opensecondpump')
                        self.isSecondPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        self.printShow('closesecondpump')
                        self.isSecondPumpOpen = False
            elif data[1:2] == b'\x01':
                if data[2:3] == b'\x0A':
                    firstcurrent = int().from_bytes(data[3:5],'big')
                    self.printShow('getfirstcurrent:',firstcurrent)
                elif data[2:3] == b'\x0B':
                    secondcurrent = int().from_bytes(data[3:5],'big')
                    self.printShow('getsecondcurrent:',secondcurrent)
        elif data[0:1] == b'\x9A':
            ti1 = time.time() -self.ti0
            self.currentTimeList.append(ti1)
            self.heat = int().from_bytes(data[1:3],'big')
            self.firstPower = int().from_bytes(data[3:5],'big')
            self.firstCurrent = int().from_bytes(data[5:7],'big')
            self.getPower = int().from_bytes(data[7:9],'big')
            self.tmPower = self.tempdetector.getPower(self.heat,self.getPower)
            self.printShow('temperature and power is :',self.heat,
                'and',self.tmPower)
            self.currentValueList.append(self.tmPower)
            if self.startRecord == True:
                self.save2sql(self.tmPower)
            self.emitPlot()


# ==================
# function send
# ==================

    def openAllThread(self):
        threading.Thread(target=Model.openpaltform,args=(self,)).start()

    def openpaltform(self):
        # self.write(self.msgDictHex['openseed'])
        # time.sleep(0.3)
        # if self.isSeedOpen:
        self.write(self.msgDictHex['openfirstpump'])
        time.sleep(0.3)
        # if self.isFirstPumpOpen:
        self.write(self.msgDictHex['opensecondpump'])
        time.sleep(0.3)
        isopen = self.isSeedOpened()
        # pdb.set_trace()
        if isopen:
            self.printShow('init device set all zero')
            self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
            self.writeFirstPumpCurrent(self.firstcurrent)
            self.writesecondPumpCurrent(self.secondcurrent)
        #     self.write(self.msgDictHex['seedcurrentvalueget'])
        #     time.sleep(0.1)
        #     self.write(self.msgDictHex['seedpulseread'])
        #     time.sleep(0.1)
        #     self.write(self.msgDictHex['seedfreread'])
        #     time.sleep(0.1)
        #     # pdb.set_trace()
        #     # value = self.firstcurrent if self.firstcurrent > 0 else 0
        #     # value = int(self.firstcurrent).to_bytes(2,'big')
        #     valuemsg = self.msgDictHex['setfirstcurrent']
        #     valuemsg = valuemsg[:5] + valuemsg[-2:]
        #     time.sleep(0.1)
        #     # value = self.secondcurrent if self.secondcurrent > 0 else 0
        #     # value = int(self.secondcurrent).to_bytes(2,'big')
        #     valuemsg = self.msgDictHex['setsecondcurrent']
        #     valuemsg = valuemsg[:5] + valuemsg[-2:]
        #     time.sleep(0.1)
        self.emitStatus()

    def closeAll(self):
        self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
        self.writeFirstPumpCurrent(self.firstcurrent)
        self.writesecondPumpCurrent(self.secondcurrent)

        self.write(self.msgDictHex['closesecondpump'])
        time.sleep(0.3)
    # if self.isFirstPumpOpen:
        self.write(self.msgDictHex['closefirstpump'])
        time.sleep(0.3)


        # self.printShow('seed:',self.isSeedOpen,
        #     'isFirstPumpOpen:',self.isFirstPumpOpen,
        #     'isSecondPumpOpen:',self.isSecondPumpOpen)
    def isSeedOpened(self):
        if self.isSeedOpen\
            and self.isFirstPumpOpen\
            and self.isSecondPumpOpen:
            self.printShow('openpaltform,seed,1st,2st')
            return True
        return False

    def isSeedSet(self):
        self.printShow(self.seedcurrentre ,'and', self.seedpulsere,'and', self.seedfrequecere)

        if self.seedcurrentre and self.seedpulsere\
        and self.seedfrequecere:
            time.sleep(0.1)
            self.write(self.msgDictHex['seedpulseread'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedfreread'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedcurrentvalueget'])
            if self.seedcurrent != -1:
                self.printShow('seedcurrent is set to ',self.seedcurrent)
            if self.seedpulse != -1:
                self.printShow('seedpulse is set to ',self.seedpulse)
            if self.seedfrequece != -1:
                self.printShow('seedfrequece is set to ',self.seedfrequece)




#==============================================================================
# Signals from view
#==============================================================================
    # def writeSeedPulse(self,value):
    #     # self.printShow('pulevalue:',value,type(value),int(value))
    #     value = int(value).to_bytes(2,'big')
    #     valuemsg = self.msgDictHex['seedpulseset']
    #     valuemsg = valuemsg[:4] + value + valuemsg[6:]
    #     self.printShow('pulevaluemsg',valuemsg)
    #     #self.write()
    # def writeSeedFre(self,value):
    #     # self.printShow('frevalue:',value)
    #     # self.printShow('frevalue:',value,type(value),int(value))
    #     value = int(value).to_bytes(2,'big')
    #     valuemsg = self.msgDictHex['seedfreset']
    #     valuemsg = valuemsg[:4] + value + valuemsg[6:]
    #     self.printShow('frevaluemsg',valuemsg)
    #     #self.write()

    def writeSeedPulseAndFre(self,seedPulseAndFre):
        self.printShow('seedPulseAndFre:',seedPulseAndFre)
        if seedPulseAndFre:
            value = seedPulseAndFre[0]
            # self.printShow('frevalue:',value            # self.printShow('frevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedfreset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            self.printShow('frevaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            value = seedPulseAndFre[1]
            # self.printShow('pulevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedpulseset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            self.printShow('pulsevaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            value = seedPulseAndFre[2]
            # self.printShow('pulevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedcurrentvalueset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            self.printShow('currentvaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            self.write(self.msgDictHex['openseedLED'])
            self.isSeedSet()

    def writeFirstPumpCurrent(self,value):
        # self.printShow('frevalue:',value)
        # self.printShow('setfirstcurrent:',value,type(value),int(value))
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setfirstcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        self.printShow('setfirstcurrent',valuemsg)
        self.write(valuemsg)

    def writesecondPumpCurrent(self,value):
        # self.printShow('frevalue:',value)
        # self.printShow('setsecondcurrent:',value,type(value),int(value))
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setsecondcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        self.printShow('setfirstcurrent',valuemsg)
        self.write(valuemsg)

    # def creatPlot(self,tableName):
    #     data = self.datahand.getTableData(tableName)
    #     self.datahand.createPlot(data)


###
#sqlite save
###

    def save2sql(self, power ):
        startTime = str(int(self.ti0))
        localTime = time.time()
        tableName = 'TM'+startTime+'US'+self.username
        # try:
        #     self.datahand.save2Sql(tableName, localTime, power)
        # except Exception as e:
        #     raise e


#==============================================================================
# Signals for view
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)

    def emitCurrentValue(self, value):
        gotTime = time.time()
        self.cValue.emit([gotTime,value])

    def emitSeedCurrent(self):
        self.seedCurrentSignal.emit(self.seedcurrent)

    def emitSeedPulse(self):
        self.seedPulseSignal.emit(self.seedpulse)

    def emitSeedFrequece(self):
        self.seedFrequeceSignal.emit(self.seedfrequece)

    def emitFirstCurrent(self):
        self.firstCurrentSignal.emit(self.firstcurrent)

    def emitSencondCurrent(self):
        self.secondCurrentSignal.emit(self.secondcurrent)

    def emitStatus(self):
        self.emitSeedCurrent()
        self.emitSeedPulse()
        self.emitSeedFrequece()
        self.emitFirstCurrent()
        self.emitSencondCurrent()

    def emitPlot(self):
        self.plotPower.emit([self.currentTimeList,self.currentValueList])

import numpy as np
# from matplotlib import pyplot

class TempDetector(object):
    """
型号         |T0 【℃】| Z0 【mV/W】| Zc【（mV/W）/℃】
B01-SMC| 20℃         | 50.3                | 0.088
B05-SMC| 20℃         | 134.2              | 0.235
C50-MC   | 20℃        | 0.59775          | 0.000747
给出的temp实际上是电阻值单位kΩ，
给出的功率power实际上是电压值单位为V
    """
    def __init__(self, detect = 'B05-SMC'):
        super(TempDetector, self).__init__()
        para = {
        'B01-SMC': [20,50.3,0.088],
        'B05-SMC': [20,134.2,0.235],
        'C50-MC':   [20,0.59775,0.000747]
        }
        getpara = para[detect]
        self.stand_temp = getpara[0]
        self.init_sen = getpara[1]
        self.correct_sen = getpara[2]
        # self.temp = temp
        # self.voltage = power
        self.poly = self.fit(10)

    def getPower(self, temp = 0, voltage = 0,):
        stand_temp= self.stand_temp
        init_sen = self.init_sen
        correct_sen = self.correct_sen
        temp = self.poly(temp)
        #Z=Z0+（T-T0）*Zc
        sensitivity = init_sen +(temp-stand_temp)*correct_sen
        #Φ = U/Z
        power = voltage/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        return power

    def fit(self,lit = 10):
        x = [90,    80,     70,   60,     56, 50, 40, 30, 20, 11,   8, 5.5, 4, 3.5, 2]
        y = [-18, -15.5, -14, -11.5, -10,  -8, -4,  1.5, 10, 20, 30, 40, 50, 60, 70]
        z = np.polyfit(x, y, lit)
        p = np.poly1d(z)
        # print('p:',p )
        # y2 = [p(i) for i in x]
        # pyplot.plot(x,y2, hold = True)
        return p
