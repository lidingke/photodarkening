#!/usr/bin/env python
# coding=utf-8

# System imports
import  threading
import  queue
#from    time                import sleep
import time
from    sys                 import exit
import pickle

# PyQt5 imports
from    PyQt5.QtCore        import pyqtSignal
from    PyQt5.QtCore        import QObject

# PySerial imports
import  serial
from    serial.serialutil   import SerialException

class Model(threading.Thread, QObject):

    # This signal emitted when program fail to read serial port (self.port)
    error = pyqtSignal(object)
    cValue = pyqtSignal(object)
    def __init__(self):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        # Queue with data (lines) received from serial port
        self.queue      = queue.Queue()
        self.currentValueList      = list()
        # Communications settings
        self.port       = 'com6'
        self.br         = 9600
        self.timeout    = 0.01
        # Line ending id
        #self.eol        = 0

        # PySerial object
        self.ser        = None
        # Flag for main cycle
        self.running    = True

        with open('msg.pickle', 'rb') as f:
            entry = pickle.load(f)
        self.msgDictHex = entry['msgDictHex']
        self.msgDictStr = entry['msgDictStr']
        self.sendmsgrec = entry['sendmsgrec']

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

                time.sleep(self.timeout)

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
            time.sleep(20)

        print(self.ser)

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

    def set_port(self,port):
        self.port = port



    def reset_port(self, port):
        self.ser.close()
        time.sleep(0.1)
        self.port = port
        self.begin()
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

        time.sleep(0.1)

    # def readline(self):
    #     try:
    #         data = self.ser.read(15)
    #     except Exception as e:
    #         raise e
    #     return data

    def readbit(self,ser):
        time.sleep(0.1)
        try:
            data = ser.read(1)
        except Exception as e:
            raise e
        except portNotOpenError :
            time.sleep(1)
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
        '''
        message analysis and manage
        '''
        if data == None:
            return '-1'
        elif len(data) > 5:
            data = data[2:6]
        print(data[0:1],':',data[1:2],type(data[0]),type(data))
        if data[0:1] == b'\x01':
            if data[1:2] == b'\x11':
                #current plot msg
                #print(data,'12:',data[-2:])
                currentValue = data[-2:].strip()
                currentValue = int().from_bytes(currentValue,'big')/100
                print('currentValue=',currentValue)
                self.currentValueList.append(currentValue)
                self.emitCurrentValue(currentValue)
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
# Signals for view
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)

    def emitCurrentValue(self, value):
        gotTime = time.time()
        self.cValue.emit([gotTime,value])
