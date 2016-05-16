from modelcore import ModelCore
from PyQt5.QtCore import pyqtSignal
import threading
import time
from database import DataHand
import pdb
from toolkit import HexSplit

class ModelPump(ModelCore):
    """docstring for ModelPump"""
    firstCurrentSignal = pyqtSignal(object)
    secondCurrentSignal = pyqtSignal(object)
    plotPower = pyqtSignal(object)
    beginPlot = pyqtSignal()

    def __init__(self):
        super(ModelPump, self).__init__()
        self.lastvalue = 0
        self.tempdetector = TempDetector()
        self.currentValue  = 0
        self.currentTime = 0
        self.ti0 = time.time()
        self.startRecord = False# set start record statues
        self.datahand = DataHand('data\\powerdata.db')
        self.datahand.username = self.username
        self.saveStop = False
        self.lastPower = 1
        self.lastTemp = 1
        self.MFilterLen = 5
        self.powerDataList = []
        self.powerDataNum = 0

    def coreMsgProcess(self,data):
        '''input message analysis and manage
        '''
        if data[0:1] == b'\x02':
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
            dlst = self.powerDataList
            powerDataAndOriginal = [self.getPowerData(data),HexSplit.fun(data)]
            if self.powerDataNum != self.MFilterLen:
                self.powerDataNum = self.powerDataNum +1
            else:
                self.powerDataNum = 1
                # pdb.set_trace()
                dlst.sort()
                midValue = dlst[int(self.MFilterLen/2)+1]
                try:
                    self.currentValue = midValue[0]
                    originData = midValue[1]
                except IndexError:
                    return
                except Exception as e :
                    raise e
                dlst.clear()
                # dlst.append([pdata,HexSplit.fun(data.hex())])
                ti1 = time.time() -self.ti0
                self.currentTime = ti1
                # self.currentValue = self.tmPower
                self.emitPlot()
                if (self.startRecord == True) and (self.saveStop == False):
                    # hexdata = data.hex()
                    self.save2sql(self.currentValue,originData)
            dlst.append(powerDataAndOriginal)


    def getPowerData(self,data):
        print('十六进制温度：',data[1:3],'电压：',data[5:7],'length',len(data))
        self.heat = int().from_bytes(data[1:3],'little')/100
        # self.firstPower = int().from_bytes(data[3:5],'little')
        # self.firstCurrent = int().from_bytes(data[5:7],'little')
        self.getPower = int().from_bytes(data[5:7],'little')
        # if self.getPower > 65200:#some times error number from slave ,most of them higher them 65200
        #     self.printShow('收到功率乱码')
        #     self.getPower = int().from_bytes(data[-7:-5],'little')
        print('十进制温度：',self.heat,'电压：',self.getPower)
        if self.heat <100:
            self.lastTemp = self.heat
        if self.getPower <65200:
            self.lastPower = self.getPower
        self.getPower = (self.getPower/4096)*3#！！！！！这里也改了注意！！！！！！！！！
        self.tmPower = self.tempdetector.getPower(self.heat,self.getPower)
        self.printShow('温度:',self.heat,'℃','  功率:',round(self.tmPower,4),'W')
        return self.tmPower

    def creatPlot(self,tableName):
        data = self.datahand.getTableData(tableName)
        self.datahand.createPlot(data)

#pump


    def openAllThread(self):
        threading.Thread(target=self.openAll).start()

    def openAll(self):
        '''
        self.write(self.msgDictHex['openfirstpump'])
        time.sleep(0.3)
        '''
        self.write(self.msgDictHex['opensecondpump'])
        '''
        time.sleep(0.3)

        # isopen = self.isSeedOpened()
        # if isopen:
        self.printShow('init device set all zero')
        # self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
        self.writeFirstPumpCurrent(self.firstcurrent)
        self.writesecondPumpCurrent(self.secondcurrent)
        self.emitStatus()
        '''

    def closeAll(self):
        # self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
        '''
        self.writeFirstPumpCurrent(self.firstcurrent)
        self.writesecondPumpCurrent(self.secondcurrent)
        '''
        self.write(self.msgDictHex['closesecondpump'])
        # '''
        time.sleep(0.3)
    # if self.isFirstPumpOpen:
        self.write(self.msgDictHex['closefirstpump'])
        time.sleep(0.3)
        # '''


        # self.printShow('seed:',self.isSeedOpen,
        #     'isFirstPumpOpen:',self.isFirstPumpOpen,
        #     'isSecondPumpOpen:',self.isSecondPumpOpen)
    # def isSeedOpened(self):
    #     if self.isSeedOpen\
    #         and self.isFirstPumpOpen\
    #         and self.isSecondPumpOpen:
    #         self.printShow('openpaltform,seed,1st,2st')
    #         return True
    #     return False


    def writeFirstPumpCurrent(self,value):
        # lastvalue = self.lastvalue
        # nowvalue = value
        # self.printShow('frevalue:',value)
        # self.printShow('setfirstcurrent:',value,type(value),int(value))
        print('firstvalue',value)
        value = int(value)*4#*4 is about slave
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setfirstcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        self.printShow('setfirstcurrent',valuemsg)
        self.write(valuemsg)


    def writesecondPumpCurrent(self,value):
        threading.Thread(target = self.threeTimesSpump, args = (value,)).start()
        # self.printShow('frevalue:',value)
        # self.printShow('setsecondcurrent:',value,type(value),int(value))

    def threeTimesSpump(self,value):
        value = int(value)
        if value == self.lastvalue:
            return
        lvalue = self.lastvalue
        pvalue = value
        delta = (pvalue - lvalue)/5
        print('delta:',delta)
        for x in range(1,6):
            print(lvalue + delta*x)
            self.secondPumpCurrentMsg(lvalue + delta*x)
            time.sleep(0.1)
        self.lastvalue = value

    def secondPumpCurrentMsg(self,value):
        value = value/4.6#
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setsecondcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        self.printShow('setfirstcurrent',valuemsg,'v',value)
        self.write(valuemsg)


    def emitFirstCurrent(self):
        self.firstCurrentSignal.emit(self.firstcurrent)

    def emitSencondCurrent(self):
        self.secondCurrentSignal.emit(self.secondcurrent)

    def emitStatus(self):
        # self.emitSeedCurrent()
        # self.emitSeedPulse()
        # self.emitSeedFrequece()
        self.emitFirstCurrent()
        self.emitSencondCurrent()

    def emitCurrentValue(self, value):
        gotTime = time.time()
        self.cValue.emit([gotTime,value])

    def emitPlot(self):
        self.plotPower.emit([self.currentTime,self.currentValue])


    def getcurrentValue(self):
        return self.currentValue

    def getcurrentTime(self):
        return self.currentTime

    def setSaveStop(self,isture):
        self.saveStop = isture

#plort start status
    def setBeginPlotTime(self):
        self.startRecord = True
        self.saveStop = False
        # self.ti0 = time.time()
        print('get ti0:',self.ti0,'init tabel username',self.username)
        self.datahand.initSqltabel(self.ti0,self.username)
        self.beginPlot.emit()
        # self.currentTime.clear()
        # self.currentValue.clear()

    def setStartTime(self,stime ):
        self.ti0 = stime


#sqlite save
    def save2sql(self, power ,hexdata):
        startTime = str(int(self.ti0))
        localTime = time.time()
        tableName = 'TM'+startTime+'US'+self.username
        try:
            self.datahand.save2Sql(tableName, localTime, power, hexdata)
        except Exception as e:
            raise e

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
        # self.poly = self.fit(10)

    def getPower(self, temp = 0, voltage = 0,):
        stand_temp= self.stand_temp
        init_sen = self.init_sen
        correct_sen = self.correct_sen
        # temp = self.poly(temp)
        #Z=Z0+（T-T0）*Zc
        sensitivity = init_sen +(temp-stand_temp)*correct_sen
        #Φ = U/Z
        power = voltage*1000/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        return power

    # def fit(self,lit = 10):
    #     x = [90,    80,     70,   60,     56, 50, 40, 30, 20, 11,   8, 5.5, 4, 3.5, 2]
    #     y = [-18, -15.5, -14, -11.5, -10,  -8, -4,  1.5, 10, 20, 30, 40, 50, 60, 70]
    #     z = np.polyfit(x, y, lit)
    #     p = np.poly1d(z)
    #     # print('p:',p )
    #     # y2 = [p(i) for i in x]
    #     # pyplot.plot(x,y2, hold = True)
    #     return p
