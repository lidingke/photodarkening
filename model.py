#!/usr/bin/env python
# coding=utf-8

# System imports
import  threading
import  queue
from    time                import sleep
from    sys                 import exit

# PyQt5 imports
from    PyQt5.QtCore        import pyqtSignal
from    PyQt5.QtCore        import QObject

# PySerial imports
import  serial
from    serial.serialutil   import SerialException

class Model(threading.Thread, QObject):

    # This signal emitted when program fail to read serial port (self.port)
    error = pyqtSignal(object)

    def __init__(self):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        # Queue with data (lines) received from serial port
        self.queue      = queue.Queue()
        self.currentValueList      = list()
        # Communications settings
        self.port       = 'com12'
        self.br         = 9600
        self.timeout    = 0.01
        # Line ending id
        #self.eol        = 0

        # PySerial object
        self.ser        = None
        # Flag for main cycle
        self.running    = True

        self.msgDictStr={
        #open seed \x00
        'openseed':' EB 90 01 00 00 01 90 EB',
        'openseedreturn':' EB 90 01 00 00 01 90 EB',
        'openseederror':' EB 90 01 00 10 00 90 EB',
        #close seed \x00
        'closeseed':' EB 90 01 00 00 00 90 EB',
        'closeseedreturn':' EB 90 01 00 00 00 90 EB',
        'closeseederror':' EB 90 01 00 01 00 90 EB',
        # seed current \x01
        'seedcurrentvalueset':' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvaluesetreturn':' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvalueseterror':' EB 90 01 01 10 00 90 EB',
        # seed pulse \x02
        'seedpulseset':' EB 90 01 02 FF FF 90 EB',
        'seedpulsesetreturn':' EB 90 01 02 FF FF 90 EB',
        'seedpulseseterror':' EB 90 01 02 10 00 90 EB',
        # seed fre \x03
        'seedfreset':' EB 90 01 03 FF FF 90 EB',
        'seedfresetreturn':' EB 90 01 03 FF FF 90 EB',
        'seedfreseterror':' EB 90 01 03 1000 90 EB',
        #seed current \x04
        'seedcurrentvalueget':' EB 90 01 04 90 EB',
        'seedcurrentvaluegetreturn':' EB 90 01 04 FF FF 90 EB',
        'seedcurrentvaluegeterror':' EB 90 01 04 10 00 90 EB',
        #seed pluse \x05
        'seedpluseread':' EB 90 01 05 90 EB',
        'seedplusereadreturn':' EB 90 01 05 FF FF 90 EB',
        'seedplusereaderror':' EB 90 01 05 10 00 90 EB',
        #seed frequance \x06
        'seedfreread':' EB 90 01 06 90 EB',
        'seedfrereadreturn':' EB 90 01 06 FF FF 90 EB',
        'seedfrereaderror':' EB 90 01 06 10 00 90 EB'
        }
        self.msgDictHex = dict()

        for k,v in self.msgDictStr.items():
            self.msgDictHex[k] = b''.fromhex(v) #v.replace(b" ",b"\x")
        #self.msgDict = self.msgDictHex
        self.sendmsgrec = dict([(v,k) for k,v in self.msgDictHex.items()])

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
                #print('Model start')
                data = None
                #sleep(1)
                #data = self.readline()
                data = self.analysisbit(self.ser)
                    #print('Error occured while reading data.')
                #try:
                if len(data)>0:
                    #print('lendata',len(data))
                    self.coreMsgProcess(data)
                    #print('上位机接收：',data)
                    self.queue.put(data.strip())
                # except Exception as e:
                #     data=b'-1'

                sleep(self.timeout)

        except KeyboardInterrupt:
            exit()

    def stop(self):
        '''
        Stop thread.
        '''
        print('stop thread Model and close serial')
        self.ser.close()
        self.running = False

    def begin(self):
        '''
        Initializate PySerial object
        '''
        try:
            print(self.port,self.br)
            self.ser = serial.Serial(
                    self.port, self.br, timeout=120
            )
            print(self.ser)
        except SerialException:
            print('Fail to open default port.')
            self.ser = serial.Serial(baudrate=self.br, timeout=120)
            sleep(20)

        print(self.ser)

#==============================================================================
# Get, Set
#==============================================================================

    def get_queue(self):
        return self.queue


    def getcurrentValueList(self):
        return self.currentValueList

    def set_port(self,port):
        self.port = port



    def reset_port(self, port):
        self.ser.close()
        sleep(0.1)
        self.port = port
        self.begin()
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

    def set_br(self, baudrate):
        self.br = baudrate
        self.ser.baudrate = self.br

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
        dataSend = self.msgcoup(data)
        #print(dataSend)
        if dataSend:
            print('上位机发送:',dataSend)
            self.ser.write(dataSend)

        sleep(0.1)

    # def readline(self):
    #     try:
    #         data = self.ser.read(15)
    #     except Exception as e:
    #         raise e
    #     return data

    def readbit(self,ser):
        sleep(0.1)
        try:
            data = ser.read(1)
        except Exception as e:
            raise e
        except portNotOpenError :
            sleep(1)
        return data

    def msgcoup(self,msg):
        msg = self.msgDictHex.get(msg, b'-1')
        if msg is b'-1':
            return msg
        else:
            if len(msg) > 6:
                return msg
            else:
                return b'\xEB\x90'+msg+b'\x90\xEB'

    def analysisbit(self,ser):
        '''
                return without package
        '''
        readlive = True
        # xebstatue = False
        # x90statue = False
        bitlist = list()
        while readlive and self.running:
            databit = self.readbit(ser)
            if databit == b'\xeb':
                # print(databit,'1')
                databit = self.readbit(ser)
                if databit == b'\x90':
                    while True:
                        #print(databit,'2')
                        databit = self.readbit(ser)
                        if databit == b'\x90':
                            databit = self.readbit(ser)
                            data = b''.join(bitlist)
                            #print(data)
                            return data
                        bitlist.append(databit)

    def coreMsgProcess(self,data):

        if data == None:
            return '-1'
        elif len(data) > 5:
            data = data[2:6]
        print(data[0:1],':',data[1:2],type(data[0]),type(data))
        if data[0:1] == b'\x01':
            if data[1:2] == b'\x11':
                #current plot msg
                print(data,'12:',data[-2:])
                currentValue = data[-2:]
                print(currentValue)
                self.currentValueList.append(currentValue.strip())
            elif data[1:2] == b'\x00':
                #if data[2:3] == b'\x00\x00':
                print('seed received',data)
                #open and close seed
                pass
            elif data[1:2] == b'\x01':
                #seed current value set \x01
                print('seed received',data)
                pass
            elif data[1:2] == b'\x02':
                #seed pulse width
                print('seed received',data)
                pass
            elif data[1:2] == b'\x03':
                #seed frequece set
                print('seed received',data)
                pass
            elif data[1:2] == b'\x04':
                #seed current value get
                print('seed received',data)
                pass
            elif data[1:2] == b'\x05':
                #seed pluse width read
                print('seed received',data)
                pass
            elif data[1:2] == b'\x06':
                #seed frequece read
                print('seed received',data)
                pass
            else:
                return b'-1'



#==============================================================================
# Signals
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)
