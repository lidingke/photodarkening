from model.modelcore import ModelCore
from PyQt5.QtCore import pyqtSignal,QObject
import time
import threading

class ModelSource(ModelCore):
    """docstring for ModelSource"""
    seedSignal = pyqtSignal(object,object,object)
    seedCurrentSignal = pyqtSignal(object)
    seedPulseSignal = pyqtSignal(object)
    seedFrequeceSignal = pyqtSignal(object)

    def __init__(self):
        super(ModelSource, self).__init__()
        # print('is ModelSource __init__?')

    def coreMsgProcess(self,data):
        '''
        input message analysis and manage
        '''
        if data[0:1] == b'\x01':
            if data[1:2] == b'\x00':
                # ==========
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

    def openAllThread(self):
        threading.Thread(target=self.openAll,).start()

    def openAll(self):
        self.write(self.msgDictHex['openseed'])
        '''
        time.sleep(0.3)
        self.printShow('init device set all zero')
        self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
        self.emitStatus()
        '''

    def closeAll(self):
        # self.writeSeedPulseAndFre([self.seedcurrent,self.seedpulse,self.seedfrequece])
        self.write(self.msgDictHex['closeseed'])

    # def isSeedOpened(self):
    #     if self.isSeedOpen\
    #         and self.isFirstPumpOpen\
    #         and self.isSecondPumpOpen:
    #         # self.printShow('openseed,1st,2st')
    #         return True
    #     return False




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

    def portOpenEvent(self):
        # self.openSeed()
        pass

# need to rewrite
    # def openSeed(self):
    #     self.write(self.msgDictHex['openseed'])
    #     # threading.Thread(target = self.writeSeedPulseAndFre, args = (self,seedPulseAndFre,))
    #     # self.writeSeedPulseAndFre()

    def setSeed(self,seedPulseAndFre):
        # print('setSeed')
        threading.Thread(target = self.writeSeedPulseAndFre, args = (seedPulseAndFre,)).start()


    def isSeedSet(self):
        # self.printShow(self.seedcurrentre ,'and', self.seedpulsere,'and', self.seedfrequecere)
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
        self.emitStatus()


#==============================================================================
# Signals for view
#==============================================================================
    # def emitSeedCurrent(self):
    #     self.seedCurrentSignal.emit(self.seedcurrent)

    # def emitSeedPulse(self):
    #     self.seedPulseSignal.emit(self.seedpulse)

    # def emitSeedFrequece(self):
    #     self.seedFrequeceSignal.emit(self.seedfrequece)

    def emitStatus(self):
        self.seedSignal.emit(self.seedcurrent, self.seedpulse, self.seedfrequece)
        # self.emitSeedCurrent()
        # self.emitSeedPulse()
        # self.emitSeedFrequece()
