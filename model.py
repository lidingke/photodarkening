#!/usr/bin/env python
# coding=utf-8

# System imports
import  threading
import  queue
#from    time                import sleep
import time
from    sys                 import exit
import pickle
import pdb

# PyQt5 imports
from    PyQt5.QtCore        import pyqtSignal
from    PyQt5.QtCore        import QObject
from    PyQt5.QtCore        import QTime

# PySerial imports
import  serial
from    serial.serialutil   import SerialException

class Model(threading.Thread, QObject):

    # This signal emitted when program fail to read serial port (self.port)
    error = pyqtSignal(object)
    cValue = pyqtSignal(object)
    seedCurrentSignal = pyqtSignal(object)
    seedPulseSignal = pyqtSignal(object)
    seedFrequeceSignal = pyqtSignal(object)
    firstCurrentSignal = pyqtSignal(object)
    secondCurrentSignal = pyqtSignal(object)

    def __init__(self):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        # Queue with data (lines) received from serial port
        self.queue      = queue.Queue()
        self.currentValueList      = list()
        # Communications settings
        self.port       = 'com1'
        self.br         = 9600
        self.timeout    = 0.01
        # Line ending id
        #self.eol        = 0

        # PySerial object
        self.ser        = None
        # Flag for main cycle
        self.running    = True
        self.__init__slaveStatus()

        with open('msg.pickle', 'rb') as f:
            entry = pickle.load(f)
        self.msgDictHex = entry['msgDictHex']
        self.msgDictStr = entry['msgDictStr']
        self.sendmsgrec = entry['sendmsgrec']
        self.entry = entry

    def __init__slaveStatus(self):
        self.isSeedOpen = False
        self.seedcurrentre = False
        self.seedpulsere = False
        self.seedfrequecere = False
        self.seedcurrent = -1
        self.seedpulse = -1
        self.seedfrequece = -1
        self.firstcurrent = -1
        self.secondcurrent = -1
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False
        self.isLEDOpen = False

    def run(self):
        '''
        Run thread.
            Method representing the thread's activity.
            You may override this method in a subclass. The standard run() method
            invokes the callable object passed to the object's constructor as the
            target argument, if any, with sequential and keyword arguments taken
            from the args and kwargs arguments, respectively.
        '''
        try:

            while self.running:
                #print('running:',self.running)
                if self.ser:
                    #print('Model start',self.ser)
                    data = None
                    #sleep(1)
                    #data = self.readline()
                    #ser = self.ser
                    data = self.analysisbit()
                        #print('Error occured while reading data.')
                    #try:runrun
                    if data :
                        #print('lendata',len(data))
                        #print('data:',data)
                        self.coreMsgProcess(data)
                        #print('上位机接收：',data)
                        self.queue.put(data.strip())
                    # except Exception as e:
                    #     data=b-1
                    time.sleep(self.timeout)

        except KeyboardInterrupt:
            exit()

    def stop(self):
        '''
        Stop thread.
        '''
        print('stop thread Model and close serial')

        if self.ser:
            self.ser.timeout = 0
            # change to non blocking mode and then close
            self.ser.close()
        # self.ser = None
        self.running = False

    def closePort(self):
        self.ser.close()

    def begin(self):
        '''
        Initializate PySerial object
        '''
        try:
            self.ser = serial.Serial(self.port, self.br, timeout=120)
        except serial.serialutil.SerialException:
            print('=== can not open the port ===')
            print('ser=',self.ser)
            #self.ser = serial.Serial(baudrate=self.br, timeout=120)
            #self.stop()


    def reSetPort(self):

        try:
            self.ser = serial.Serial(self.port, self.br, timeout=120)
            print(self.ser)
        except serial.serialutil.SerialException:
            print('=== can not open the port ===')
            self.ser = serial.Serial(baudrate=self.br, timeout=120)
            print('ser=',self.ser)


            #self.stop()

    def isPortOpen(self):
        if self.ser:
            ser = self.ser
            return ser.isOpen()
        else:
            return False





        # try:
        #     print(self.port,self.br)
        #     self.ser = serial.Serial(
        #             self.port, self.br, timeout=120
        #     )
        #     print(self.ser)
        #     return True
        # except SerialException:
        #     print('Fail to open default port.')
        #     #self.ser = serial.Serial(baudrate=self.br, timeout=120)
        #     time.sleep(1)
        #     # self.ser = serial.Serial(
        #     #         self.port, self.br, timeout=120
        #     # )
        #     self.stop()
        #     return False

        #print(self.ser)

#==============================================================================
# Get, Set from view
#==============================================================================

    def get_queue(self):
        return self.queue

    def getcurrentValueList(self):
        if len(self.currentValueList) >0:
            return self.currentValueList.pop()
        else:
            return None

    def setSer(self,ser):
        self.ser = ser

    def set_port(self,port):
        # if self.port is not port:
        self.port = port

    def set_br(self, baudrate):
        # if self.br is not baudrate:
        self.br = baudrate
        #self.ser.baudrate = self.br


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
        #         print(self.ser._port_handle)

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
        @data data to send
        '''
        if type(data) is str:
            pass
            dataSend = self.msgcoup(data)
        else:
            dataSend =data
        #print(dataSend)
        if dataSend:
            print('上位机发送:',dataSend)
            self.ser.write(dataSend)

        time.sleep(0.1)

    # def readline(self):
    #     try:
    #         data = self.ser.read(15)
    #     except Exception as e:
    #         raise e
    #     return data

    def readbit(self,ser):
        try:
            if ser:
            # if ser and ser.isOpen is True:
                data = ser.read(1)
        # except Exception as e:
        #     raise e
        except serial.serialutil.SerialException :
            time.sleep(1)
            data = b'-1'
        except NoneType :
            time.sleep(1)
            data = b'-1'


        return data




    def msgcoup(self,msg):
        '''
        package a message if msg length > 6
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
        '''
        readlive = True
        # xebstatue = False
        # x90statue = False
        bitlist = list()
        while self.running:
            #print('keepbit')
            ser = self.ser
            databit = self.readbit(self.ser)
            if databit == b'\xeb':
                # print(databit,'1')
                databit = self.readbit(self.ser)
                if databit == b'\x90':
                    while True:
                        # print(databit,'2')
                        databit = self.readbit(self.ser)
                        if databit == b'\x90':
                            databit = self.readbit(self.ser)
                            data = b''.join(bitlist)
                            print(data)
                            return data
                        bitlist.append(databit)
            elif databit == b'\x9A':
                while True:
                    databit = self.readbit(self.ser)
                    if databit == b'\xA9':
                        databit = self.readbit(self.ser)
                        data = b''.join(bitlist)
                        print(data)
                        return b'\x9A' + data
                    bitlist.append(databit)

        return b'-1'

    def coreMsgProcess(self,data):
        '''
        message analysis and manage
        '''
        # if data == None:
        #     return '-1'
        # elif len(data) > 5:
        #     data = data[2:]
        #     data = data[:-2]
        # print(data[0:1],':',data[1:2],type(data[0]),type(data))
        if data[0:1] == b'\x01':
            if data[1:2] == b'\x11':
                #current plot msg
                #print(data,'12:',data[-2:])
                currentValue = data[-2:].strip()
                currentValue = int().from_bytes(currentValue,'big')/100
                print('currentValue=',currentValue)
                self.currentValueList.append(currentValue)
                #停掉绘图以便测试
                #self.emitCurrentValue(currentValue)
            elif data[1:2] == b'\x00':
                # ==========
                #open and close seed
                #if data[2:3] == b'\x00\x00':
                print('seed received',data)
                if data[2:3] == b'\x00':
                    if data[3:4] == b'\x01':
                        print('openseedreturn')
                        self.isSeedOpen = True
                    elif data[3:4] == b'\x00':
                        print('closeseedreturn')
                        self.isSeedOpen = False
                elif data[2:3] == b'\x10':
                        print('openseederror')
                        self.isSeedOpen = False
            elif data[1:2] == b'\x01':
                # ========
                #seed current value set \x01
                print('seed received',data)
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedcurrentre = False
                else:
                    self.seedcurrentre = True
                    #current
            elif data[1:2] == b'\x02':
                #seed pulse width
                print('seed received',data)
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedpulsere = False
                else:
                    self.seedpulsere = True
                    #current
            elif data[1:2] == b'\x03':
                #seed frequece set
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedfrequecere = False
                else:
                    self.seedfrequecere = True
                    #current
                print('seed received',data)
            elif data[1:2] == b'\x04':
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedcurrent = -1
                else:
                    self.seedcurrent = int().from_bytes(data[2:4],'big')

                #seed current value get
                print('seed received',data)
            elif data[1:2] == b'\x05':
                #seed pluse width read
                print('seed received',data)
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedpulse = -1
                else:
                    self.seedpulse = int().from_bytes(data[2:4],'big')
            elif data[1:2] == b'\x06':
                #seed frequece read
                print('seed received',data)
                if data[2:3] == b'\x10':
                    print('seederror')
                    self.seedfrequece = -1
                else:
                    self.seedfrequece = int().from_bytes(data[2:4],'big')
            else:
                return b-1
        elif data[0:1] == b'\x02':
            if data[1:2] == b'\x00':
                if data[2:3] == b'\x0A':
                    if data[3:5] == b'\x00\x01':
                        print('openfirstpump')
                        self.isFirstPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        print('closefirstpump')
                        self.isFirstPumpOpen = False

                elif data[2:3] == b'\x0B':
                    if data[3:5] == b'\x00\x01':
                        print('opensecondpump')
                        self.isSecondPumpOpen = True
                    elif data[3:5] == b'\x00\x00':
                        print('closesecondpump')
                        self.isSecondPumpOpen = False
            elif data[1:2] == b'\x01':
                if data[2:3] == b'\x0A':
                    firstcurrent = int().from_bytes(data[3:5],'big')
                    print('getfirstcurrent:',firstcurrent)
                elif data[2:3] == b'\x0B':
                    secondcurrent = int().from_bytes(data[3:5],'big')
                    print('getsecondcurrent:',secondcurrent)
        elif data[0:1] == b'\x9A':
            self.heat = int().from_bytes(data[1:3],'big')
            self.firstPower = int().from_bytes(data[3:5],'big')
            self.firstCurrent = int().from_bytes(data[5:7],'big')
            self.getPower = int().from_bytes(data[7:9],'big')
            print('temperature and power is :',self.heat,
                'and',self.getPower)


# ==================
# function send
# ==================

    def openpaltform(self):
        self.write(self.msgDictHex['openseed'])
        time.sleep(0.3)
        if self.isSeedOpen:
            self.write(self.msgDictHex['openfirstpump'])
            time.sleep(0.3)
            if self.isFirstPumpOpen:
                self.write(self.msgDictHex['opensecondpump'])
                time.sleep(0.3)
        isopen = self.isSeedOpened()
        if isopen:
            self.write(self.msgDictHex['seedcurrentvalueget'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedpulseread'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedfreread'])
            time.sleep(0.1)
            # pdb.set_trace()
            # value = self.firstcurrent if self.firstcurrent > 0 else 0
            # value = int(self.firstcurrent).to_bytes(2,'big')
            valuemsg = self.msgDictHex['setfirstcurrent']
            valuemsg = valuemsg[:5] + valuemsg[-2:]
            time.sleep(0.1)
            # value = self.secondcurrent if self.secondcurrent > 0 else 0
            # value = int(self.secondcurrent).to_bytes(2,'big')
            valuemsg = self.msgDictHex['setsecondcurrent']
            valuemsg = valuemsg[:5] + valuemsg[-2:]
            time.sleep(0.1)
        self.emitStatus()


        # print('seed:',self.isSeedOpen,
        #     'isFirstPumpOpen:',self.isFirstPumpOpen,
        #     'isSecondPumpOpen:',self.isSecondPumpOpen)
    def isSeedOpened(self):
        if self.isSeedOpen\
            and self.isFirstPumpOpen\
            and self.isSecondPumpOpen:
            print('openpaltform,seed,1st,2st')
            return True
        return False

    def isSeedSet(self):
        print(self.seedcurrentre ,'and', self.seedpulsere,'and', self.seedfrequecere)

        if self.seedcurrentre and self.seedpulsere\
        and self.seedfrequecere:
            time.sleep(0.1)
            self.write(self.msgDictHex['seedpulseread'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedfreread'])
            time.sleep(0.1)
            self.write(self.msgDictHex['seedcurrentvalueget'])
            if self.seedcurrent != -1:
                print('seedcurrent is set to ',self.seedcurrent)
            if self.seedpulse != -1:
                print('seedpulse is set to ',self.seedpulse)
            if self.seedfrequece != -1:
                print('seedfrequece is set to ',self.seedfrequece)




#==============================================================================
# Signals from view
#==============================================================================
    # def writeSeedPulse(self,value):
    #     # print('pulevalue:',value,type(value),int(value))
    #     value = int(value).to_bytes(2,'big')
    #     valuemsg = self.msgDictHex['seedpulseset']
    #     valuemsg = valuemsg[:4] + value + valuemsg[6:]
    #     print('pulevaluemsg',valuemsg)
    #     #self.write()
    # def writeSeedFre(self,value):
    #     # print('frevalue:',value)
    #     # print('frevalue:',value,type(value),int(value))
    #     value = int(value).to_bytes(2,'big')
    #     valuemsg = self.msgDictHex['seedfreset']
    #     valuemsg = valuemsg[:4] + value + valuemsg[6:]
    #     print('frevaluemsg',valuemsg)
    #     #self.write()

    def writeSeedPulseAndFre(self,seedPulseAndFre):
        print('seedPulseAndFre:',seedPulseAndFre)
        if seedPulseAndFre:
            value = seedPulseAndFre[0]
            # print('frevalue:',value            # print('frevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedfreset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            print('frevaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            value = seedPulseAndFre[1]
            # print('pulevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedpulseset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            print('pulsevaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            value = seedPulseAndFre[2]
            # print('pulevalue:',value,type(value),int(value))
            value = int(value).to_bytes(2,'big')
            valuemsg = self.msgDictHex['seedcurrentvalueset']
            valuemsg = valuemsg[:4] + value + valuemsg[-2:]
            print('currentvaluemsg',valuemsg)
            self.write(valuemsg)
            time.sleep(0.3)
            self.write(self.msgDictHex['openseedLED'])
            self.isSeedSet()

    def writeFirstPumpCurrent(self,value):
        # print('frevalue:',value)
        print('setfirstcurrent:',value,type(value),int(value))
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setfirstcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        print('setfirstcurrent',valuemsg)
        self.write(valuemsg)

    def writesecondPumpCurrent(self,value):
        # print('frevalue:',value)
        print('setsecondcurrent:',value,type(value),int(value))
        value = int(value).to_bytes(2,'big')
        valuemsg = self.msgDictHex['setsecondcurrent']
        valuemsg = valuemsg[:5] + value + valuemsg[-2:]
        print('setfirstcurrent',valuemsg)
        self.write(valuemsg)


    def function():
        pass


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
        # pdb.set_trace()
        self.emitSeedCurrent()
        self.emitSeedPulse()
        self.emitSeedFrequece()
        self.emitFirstCurrent()
        self.emitSencondCurrent()
        # pdb.set_trace()

