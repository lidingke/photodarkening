
class TempDetector(object):
    """
型号         |T0 【℃】| Z0 【mV/W】| Zc【（mV/W）/℃】
B01-SMC| 20℃         | 50.3                | 0.088
B05-SMC| 20℃         | 134.2              | 0.235
C50-MC   | 20℃        | 0.59775          | 0.000747
给出的temp实际上是电阻值单位kΩ，
给出的功率power实际上是电压值单位为V
    """
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
        voltage = (voltage*1000-8.977)/346.34
        power = voltage/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        return power

    def hex2power(self,data = b''):
        heat = int().from_bytes(data[1:3],'little')/100
        getPower = int().from_bytes(data[5:7],'little')
        getPower = (getPower/4096)*3#！！！！！这里也改了注意！！！！！！！！！
        tmPower = self.getPower(heat,getPower)
        return tmPower

    # def fit(self,lit = 10):
    #     x = [90,    80,     70,   60,     56, 50, 40, 30, 20, 11,   8, 5.5, 4, 3.5, 2]
    #     y = [-18, -15.5, -14, -11.5, -10,  -8, -4,  1.5, 10, 20, 30, 40, 50, 60, 70]
    #     z = np.polyfit(x, y, lit)
    #     p = np.poly1d(z)
    #     # print('p:',p )
    #     # y2 = [p(i) for i in x]
    #     # pyplot.plot(x,y2, hold = True)
    #     return p
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
            # pass
            getlist = self.dataGet['dataGet']
            # print('listget?',getlist)
            if getlist:
                # powerdata = []
                # print('单位时间',len(getlist),getlist.pop())
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
        self.emitPower(powerresult)


    def emitPower(self,powerresult):
        # pass
        self.resultEmite.emit(powerresult)


class DataBaseSaveTick(threading.Thread,QObject):
    """docstring for DataBaseSaveTick
    need a input dict which hold the dataqueue,
    pass the list to process and return a new list to get new data
    """
    # resultEmite = pyqtSignal(object)

    def __init__(self,ticktime,dataGetDict):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        super(DataBaseSaveTick, self).__init__()
        # self.arg = arg
        self.tick = ticktime
        self.daemon = True
        self.dataGet = dataGetDict
        # self.detector = TempDetector()
        self.datahand = DataHand()
        # print('tick start')

    def run(self):
        '''rewrite this run() for a clock
        pass datalist to proccess per steptime
        '''
        while True:
            # pass
            getlist = self.dataGet['dataGet']
            # print('listget?',getlist)
            if getlist:
                # powerdata = []
                print('单位时间',len(getlist),getlist.pop())
                # self.factory(getlist)
                self.datahand.save2SqlAll('test123', getlist)
                # self.datahand.save2SqlAll('test123', getlist)
                self.dataGet['dataGet'] = []
            time.sleep(self.tick)

    # def factory(self,getlist):
    #     datalist = []
    #     for x in getlist:
    #         # pass
    #         power = self.detector.hex2power(x[1])
    #         # datalist.append([power,x[0],x[1]])
    #         datalist.append(power)
    #     datalist.sort()
    #     dataLen = len(datalist)
    #     powerresult = sum(datalist[1:dataLen-1])/(dataLen - 2)
    #     print(powerresult)
    #     self.emitPower(powerresult)


    # def emitPower(self,powerresult):
    #     # pass
    #     self.resultEmite.emit(powerresult)
