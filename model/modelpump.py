
from model.modelcore import ModelCore
from PyQt5.QtCore import pyqtSignal
import threading
import time
from model.database import DataHand
import pdb
from model.toolkit import HexSplit
import collections
# from dataSaveTick import DataSaveTick
import queue

class ModelPump(ModelCore):
    """docstring for ModelPump"""
    def __init__(self,):
        super(ModelPump, self).__init__()
        self.startRecord = False
        self.tempdetector = TempDetector()
        self.logTimeStep = 1
        self.dataGetDict = {'dataGet': []}
        self.datasaveTick = DataSaveTick(self.logTimeStep, self.dataGetDict)
        self.datasaveTick.start()
        self.datasaveTick.resultEmite.connect(self.powerDataProcess)

    def setBaundratePort(self, port, baudrate):
        self.set_br(int(baudrate))
        self.set_port(port)
        self.reSetPort()
        print('ser', self.ser)

    def openPlatform(self):
        msg = self.msgDictHex['openpump']
        self.write(msg)


    def closePlatform(self):
        msg = self.msgDictHex['closepump']
        self.write(msg)


    def setCurrent(self, current):
        current = int(current)
        msg = self.msgDictHex['setcurrent']
        msg = msg[:5] + current.to_bytes(2, 'little') + msg[7:]
        self.write(msg)

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
            # pdb.set_trace()
            # self.printShow('keepbit')
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
                tick = 1
                while True:
                    tick = tick + 1
                    databit = self.readbit(self.ser)
                    # print('tick ',tick)
                    if databit == b'\xA9':
                        data = b''.join(bitlist)
                        # print ('while data', data)
                        return b'\x9A' + data + b'\xA9'
                    bitlist.append(databit)


    def coreMsgProcess(self, data):
        if data[0:1] == b'\x9A':
            # print('POWER GET: ',data)
            self.dataGetDict['dataGet'].append([time.time(),data])


    def powerDataProcess(self, data):
        '''get power result and sent it to view
        '''
        newtime = time.time()
        if self.startRecord == True:
            # print('is startRecord', self.startRecord)
            threading.Thread(target=self.save2sql, args=(data, '',), daemon=True).start()
        self.currentTime = newtime
        self.currentValue = data
        print ('get current ',data)
        # self.emitPlot(newtime - self.ti0, data)
        # self.powerStatus(self.currentValue)





class TempDetector(object):
    '''
    型号         |T0 【℃】| Z0 【mV/W】| Zc【（mV/W）/℃】
    B01-SMC| 20℃         | 50.3                | 0.088
    B05-SMC| 20℃         | 134.2              | 0.235
    C50-MC   | 20℃        | 0.59775          | 0.000747
    给出的temp实际上是电阻值单位kΩ，
    给出的功率power实际上是电压值单位为V'''

    def __init__(self, detect = 'C50-MC'):
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

    def getPower(self, temp = 0, voltage = 0,):
        stand_temp= self.stand_temp
        init_sen = self.init_sen
        correct_sen = self.correct_sen
        # temp = self.poly(temp)
        # Z = Z0 +（T-T0）*Zc
        sensitivity = init_sen +(temp-stand_temp)*correct_sen

        voltage = (voltage*1000-8.977)/346.34
        if voltage < 0:
            print("voltage < 0")
            voltage = 0.000001
        #Φ = U/Z
        power = voltage/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        return power

    def hex2power(self,data = b''):
        heat = int().from_bytes(data[1:3],'little')/100
        getPower = int().from_bytes(data[5:7],'little')
        getPower = (getPower/4096)*3#！！！！！这里也改了注意！！！！！！！！！
        tmPower = self.getPower(heat,getPower)
        return tmPower

from    PyQt5.QtCore        import QObject

class DataSaveTick(threading.Thread,QObject):
    """docstring for DataSaveTick
    need a input dict which hold the dataqueue,
    pass the list to process and return a new list to get new data
    """
    resultEmite = pyqtSignal(object)

    def __init__(self,ticktime,dataGetDict):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        super(DataSaveTick, self).__init__()
        self.daemon = True
        # self.arg = arg
        self.tick = ticktime
        self.dataGet = dataGetDict
        self.detector = TempDetector()
        # print('tick start')

    def run(self):
        '''rewrite this run() for a clock
        pass datalist to proccess per steptime
        '''
        while True:
            getlist = self.dataGet['dataGet']
            if len(getlist) > 2:
                self.factory(getlist)
                self.dataGet['dataGet'] = []
            time.sleep(self.tick)

    def factory(self,getlist):
        datalist = []
        for x in getlist:
            # pass
            power = self.detector.hex2power(x[1])
            # datalist.append([power,x[0],x[1]])
            datalist.append(power)
        datalist.sort()
        dataLen = len(datalist)
        powerresult = sum(datalist[1:dataLen-1])/(dataLen - 2)
        # print(powerresult)
        getlist.clear()
        # print ('power result', powerresult)
        self.emitPower(powerresult)


    def emitPower(self,powerresult):
        # pass
        self.resultEmite.emit(powerresult)