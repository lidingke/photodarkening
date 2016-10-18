import serial
# from serial.tools import list_ports
import re
import sys
sys.path.append("..")
from slave.model import Model
import threading
import random
from time import sleep
import pdb


class Slave(object):
    """docstring for Slave"""
    def __init__(self):
        super(Slave, self).__init__()
        #self.arg = arg
        self.currentSendLive = True
        self.running = True
        self.port = 'com15'
        self.br = 9600

    def __init__slaveStatus(self):
        self.isSeedOpen = True
        self.seedcurrentre = False
        self.seedpulsere = False
        self.seedfrequecere = False
        self.seedcurrent = 1
        self.seedpulse = 1
        self.seedfrequece = 1
        self.firstcurrent = 1
        self.seedsecondcurrent = 1
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False

    def currentSend(self,ser):
        while self.currentSendLive is True:

            currentmsg = self.sendmsg['sendplot']
            cb = int(random.uniform(2,10)*100)
            cb = cb.to_bytes(2,'big')
            #print(currentmsg,':',cb)
            currentmsg = currentmsg.replace(b'\xFF\xFF',cb)
            #print(currentmsg)
            cp = 0
            print('发送电流：',currentmsg,': int ',cb,int().from_bytes(cb,'big'))

            ser.write(currentmsg)

            sleep(1)
            #return currentmsg

    def randomSend(self,ser):
        while self.currentSendLive is True:
            self.sendmsglist = [v for k, v in self.sendmsg.items()]
            rd = int(random.uniform(2, len(self.sendmsglist)))

            print('发送：', self.sendmsglist[rd])
            ser.write(self.sendmsglist[rd])
            sleep(60)
            #return currentmsg

    def powerSend(self,ser):
        #currentmsg = self.sendmsg['sendplot']
        while True:
            #print(currentmsg)
            cp1,cp2,cp3,cp4 = self.rdcreate(8,12,1),self.rdcreate(),self.rdcreate(20,60,1,head = 'little'),self.rdcreate(3,6,1)
            currentmsg = b'\x9A'+ cp1 +cp2 + cp3 + cp4 +b'\xFF\xFF'+b'\xA9'
            # print('发功：',currentmsg)
            # pdb.set_trace()
            # print('发送电流：',currentmsg,': ',int().from_bytes(cb1,'big'),int().from_bytes(cb2,'big'),int().from_bytes(cb3,'big'),int().from_bytes(cb4,'big')
            ser.write(currentmsg)
            sleep(0.02)


    def bigPowerSend(self,ser):
        #currentmsg = self.sendmsg['sendplot']
        while True:
            #print(currentmsg)
            cp1,cp2,cp3,cp4 = self.rdcreate(8,12,1),self.rdcreate(),self.rdcreate(2,1000,1,head = 'little'),self.rdcreate(3,6,1)
            currentmsg = b'\x9A'+ cp1 +cp2 + cp3 + cp4 +b'\xFF\xFF'+b'\xA9'
            print('发功：',currentmsg)
            # pdb.set_trace()
            # print('发送电流：',currentmsg,': ',int().from_bytes(cb1,'big'),int().from_bytes(cb2,'big'),int().from_bytes(cb3,'big'),int().from_bytes(cb4,'big')
            ser.write(currentmsg)
            sleep(10)

    def errorSend(self,ser):
        errorlist = [
        b'\x9A\xA9',
        b'\x9A\xA9\x9A\xA9\x9A\xA9\x9A\xA9\x9A\xA9',
        b'\x9A\x01\x01\x03\x08\x9A\xA9',
        b'\x9A\x23\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA9'
        ]
        while True:
            for x in errorlist:
                print('send error msg')
                ser.write(x)
                sleep(10)


    def process(self):

        devState={
            'comNum':'com3',
            'comState':'open',
            'seedState':'open',
            '1stState':'close',
            '1stValue':'0',
            '2stState':'close',
            '2stValue':'0'
            }

        # self.seedcurrent = 1
        # self.seedpulse = 1
        # self.seedfrequece = 1
        # self.firstcurrent = 1
        # self.seedsecondcurrent = 1
        # port_list = list(list_ports.comports())

        model = Model()
        model.set_port(self.port)
        self.ser = serial.Serial(self.port, self.br, timeout=120)
        #model.begin()
        #model.start()
        model.setSer(self.ser)

        self.sendmsg = model.get_msgDict()
        self.entry = model.getEntry()
        self.msgDictHex = self.entry['msgDictHex']
        self.msgDictStr = self.entry['msgDictStr']
        self.sendmsgrec = self.entry['sendmsgrec']


        #self.sendmsgrec = dict([(v,k) for k,v in self.sendmsg.items()])

        # ser = model.get_ser()
        ser = self.ser
        print(ser)

        print('上位机信号包大小为：',len(self.sendmsgrec))
        #ser = serial.Serial(port_serial,9600,timeout = 120)
        print('下位机模拟器启动')
        print("check which port was really used >",ser.name)
        #threading.Thread()
        #ser.write(b'\xEB\x90\x04\x05\x09\x07\x08\x09\x90\xEB')
        # 开个线程定时发送电流
        # threading.Thread(target=Slave.currentSend,args=(self,ser,)).start()
        #开个线程随机发送信号
        #threading.Thread(target=Slave.randomSend,args=(self,ser,)).start()
        # 开个线程发功
        threading.Thread(target=self.powerSend,args=(ser,)).start()
        # 开个线程发噪声
        threading.Thread(target=self.bigPowerSend,args=(ser,)).start()
        #开个线程发error信息
        threading.Thread(target=self.errorSend,args=(ser,)).start()
        while True:
            sertext = model.analysisbit()
            #sertext=ser.read(7)
            if len(sertext) > 0:
                sertext = b'\xEB\x90'+sertext+b'\x90\xEB'
                print('下位机接收并返回：',sertext)
                ser.write(sertext)
                self.msganalysis(sertext)

                #print(self.sendmsgrec.get(sertext))

        ser.close()

    def rdcreate(self,a = 2, b =10 ,c =100 , head = 'big'):
        cb = int(random.uniform(a,b)*c)
        cb = cb.to_bytes(2,head)
        return cb

    def msganalysis(self,sertext):
        # self.msgDictHex = entry['msgDictHex']
        # self.msgDictStr = entry['msgDictStr']
        # self.sendmsgrec = entry['sendmsgrec']
        if sertext:
            serstr = self.sendmsgrec.get(sertext)
            if serstr:
                if serstr == 'openseed':
                    self.isSeedOpen = True
                    print(serstr)
                elif serstr == 'closeseed':
                    self.isSeedOpen = False
                    print(serstr)
                elif serstr == 'openseedLED':
                    print(serstr)
                    self.isLEDOpen = True
                elif serstr == 'closeseedLED':
                    print(serstr)
                    self.isLEDOpen = False
                elif serstr == 'openfirstpump':
                    print(serstr)
                    self.isFirstPumpOpen = True
                elif serstr == 'opensecondpump':
                    self.isSecondPumpOpen = True
                    print(serstr)
                elif serstr == 'closefirstpump':
                    print(serstr)
                    self.isFirstPumpOpen = False
                elif serstr == 'closesecondpump':
                    print(serstr)
                    self.isSecondPumpOpen = False
                elif serstr == 'seedcurrentvalueget':
                    # pdb.set_trace()
                    writehex = sertext[:4] + self.seedcurrent.to_bytes(2, 'big') + sertext[-2:]
                    print(serstr,writehex)
                    self.ser.write(writehex)
                elif serstr == 'seedpulseread':
                    writehex = sertext[:4] + self.seedpulse.to_bytes(2, 'big') + sertext[-2:]
                    print(serstr,writehex)
                    self.ser.write(writehex)
                elif serstr == 'seedfreread':
                    writehex = sertext[:4] + self.seedfrequece.to_bytes(2, 'big') + sertext[-2:]
                    print(serstr,writehex)
                    self.ser.write(writehex)

                else:
                    print('in dict error:',serstr,sertext)
# key changed canot find in dict
            else:
                value = sertext[4:6]
                value = int().from_bytes(value,'big')
                sertext = sertext[0:4] + b'\xFF\xFF' + sertext[-2:]
                serstr = self.sendmsgrec.get(sertext)
                if serstr:
                    if serstr == 'seedcurrentvalueset':
                        self.seedcurrent = value
                        print(serstr,value)
                    elif serstr == 'seedpulseset':
                        self.seedpulse = value
                        print(serstr,value)
                    elif serstr == 'seedfreset':
                        self.seedfrequece = value
                        print(serstr,value)
                    elif serstr == 'setfirstcurrent':
                        print(serstr,value)
                        self.firstcurrent = value
                    elif serstr == 'setsecondcurrent':
                        print(serstr,value)
                        self.seedsecondcurrent = value
                    else:
                        print('out dict error:',serstr,sertext)








    # def analysisbit(self,ser):
    #         '''
    #                 return without package
    #         '''
    #         readlive = True
    #         # xebstatue = False
    #         # x90statue = False
    #         bitlist = list()
    #         while readlive and self.running:
    #             databit = self.readbit(ser)
    #             if databit == b'\xeb':
    #                 print(databit,'1')
    #                 databit = self.readbit(ser)
    #                 if databit == b'\x90':
    #                     while True:
    #                         print(databit,'2')
    #                         databit = self.readbit(ser)
    #                         if databit == b'\x90':
    #                             databit = self.readbit(ser)
    #                             data = b''.join(bitlist)
    #                             print(data)
    #                             return data
    #                         bitlist.append(databit)


    # def readbit(self,ser):
    #     sleep(0.1)
    #     try:
    #         data = ser.read(1)
    #     except Exception as e:
    #         raise e
    #     except portNotOpenError :
    #         sleep(1)
    #     return data




if __name__=='__main__':
        slave = Slave()
        slave.process()


