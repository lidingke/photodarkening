
from database import DataHand
# from modelpump import TempDetector

import numpy as np
from matplotlib import pyplot as pl

import pdb

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
        power = voltage*1000/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        return power

    def hex2power(self,data = b''):
        heat = int().from_bytes(data[1:3],'little')/100
        getPower = int().from_bytes(data[5:7],'little')
        getPower = (getPower/4096)*3#！！！！！这里也改了注意！！！！！！！！！
        tmPower = self.getPower(heat,getPower)
        return tmPower

datahand = DataHand()
data = datahand.getTableData('test123')
# pdb.set_trace()
listtime = []
listpower = []
tDt = TempDetector()
for x in data:
    listtime.append(x[0])
    listpower.append(tDt.hex2power(b''.fromhex(x[2])))

# phex = '9a66089a0e9b040500ff0fa9'
# power =
# print(power)
# print(len(data))



sampling_rate = 50
fft_size = len(listtime)
# t = np.arange(0, 1.0, 1.0/sampling_rate)
# x = np.sin(2*np.pi*156.25*t)  + 2*np.sin(2*np.pi*234.375*t)
t = listtime
x = listpower
xs = x[:fft_size]
xf = np.fft.rfft(xs)/fft_size
freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
pl.figure(figsize=(8,4))
pl.subplot(211)
pl.plot(t[:fft_size], xs)
pl.xlabel(u"时间(秒)")
pl.title(u"156.25Hz和234.375Hz的波形和频谱")
pl.subplot(212)
pl.plot(freqs, xfp)
pl.xlabel(u"频率(Hz)")
pl.subplots_adjust(hspace=0.4)
pl.show()
