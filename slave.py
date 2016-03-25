import serial
from serial.tools import list_ports
import re
from model import Model
import threading
import random
from time import sleep


class Slave(object):
    """docstring for Slave"""
    def __init__(self):
        super(Slave, self).__init__()
        #self.arg = arg
        self.currentSendLive = True
        self.running = True
        self.port = 'com13'
        self.br = 9600

    def __init__slaveStatus(self):
        self.isSeedOpen = False
        self.seedcurrentre = False
        self.seedpulsere = False
        self.seedfrequecere = False
        self.seedcurrent = '-1'
        self.seedpluse = '-1'
        self.seedfrequece = '-1'
        self.seedfirstcurrent = '-1'
        self.seedsecondcurrent = '-1'
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

            sleep(10)
            #return currentmsg

    def randomSend(self,ser):
        while self.currentSendLive is True:
            self.sendmsglist = [v for k,v in self.sendmsg.items()]
            rd = int(random.uniform(2,len(self.sendmsglist)))

            print('发送：',self.sendmsglist[rd])
            ser.write(self.sendmsglist[rd])
            sleep(60)
            #return currentmsg




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



        # port_list = list(list_ports.comports())

        model = Model()
        model.set_port(self.port)
        self.ser = serial.Serial(self.port, self.br, timeout=120)
        #model.begin()
        #model.start()
        model.serSer(self.ser)

        self.sendmsg = model.get_msgDict()
        self.entry = model.getEntry()
        self.msgDictHex = self.entry['msgDictHex']
        self.msgDictStr = self.entry['msgDictStr']
        self.sendmsgrec = self.entry['sendmsgrec']
        #self.sendmsgrec = dict([(v,k) for k,v in self.sendmsg.items()])

        # ser = model.get_ser()
        # self.ser = ser
        print(ser)

        print('上位机信号包大小为：',len(self.sendmsgrec))
        #ser = serial.Serial(port_serial,9600,timeout = 120)
        print('下位机模拟器启动')
        print("check which port was really used >",ser.name)
        #threading.Thread()
        #ser.write(b'\xEB\x90\x04\x05\x09\x07\x08\x09\x90\xEB')
        #开个线程定时发送电流
        #threading.Thread(target=Slave.currentSend,args=(self,ser,)).start()
        #开个线程随机发送信号
        threading.Thread(target=Slave.randomSend,args=(self,ser,)).start()

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

        def rdcreate(self):
            cb = int(random.uniform(2,10)*100)
            cb = cb.to_bytes(2,'big')
            return cb

    def msganalysis(self,sertext):
        # self.msgDictHex = entry['msgDictHex']
        # self.msgDictStr = entry['msgDictStr']
        # self.sendmsgrec = entry['sendmsgrec']
        if sertext:
            serstr = sendmsgrec.get(sertext)
            if serstr:
                if serstr == 'openseed':
                    self.isSeedOpen = True
                elif serstr == 'closeseed':
                    self.isSeedOpen = False
                elif serstr == 'seedcurrentvalueset':
                    self.seedcurrent = sertext[4:6]
                elif serstr == 'seedpulseset':
                    self.seedpluse = sertext[4:6]
                elif serstr == 'seedfreset':
                    self.seedfrequece = sertext[4:6]
                elif serstr == 'seedcurrentvalueget':
                    writehex = sertext[:4] + self.seedcurrent + sertext[-2:]
                    self.ser.write(writehex)
                elif serstr == 'seedpulseread':
                    writehex = sertext[:4] + self.seedpluse + sertext[-2:]
                elif serstr == 'seedfreread':
                    writehex = sertext[:4] + self.seedfrequece + sertext[-2:]
                elif serstr == 'openseedLED':
                    self.isLEDOpen = True
                elif serstr == 'closeseedLED':
                    self.isLEDOpen = False
                elif serstr == 'openfirstpump':
                    self.isFirstPumpOpen = True
                elif serstr == 'opensecondpump':
                    self.isSecondPumpOpen = True
                elif serstr == 'closefirstpump':
                    self.isFirstPumpOpen = False
                elif serstr == 'closesecondpump':
                    self.isSecondPumpOpen = False
                elif serstr == 'setfirstcurrent':
                    self.seedfirstcurrent = sertext[4:6]
                elif serstr == 'setsecondcurrent':
                    self.seedsecondcurrent = sertext[4:6]









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


