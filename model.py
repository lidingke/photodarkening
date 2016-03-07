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

        #send command to control device
        # self.sendmsg = {
        #     'sendcurrent':b'\xEB\x90\x01\xFF\xFF\x90\xEB',
        #     'openlaser':b'\xEB\x90\x00\x00\x01\x90\xEB',
        #     'closelaser':b'\xEB\x90\x00\x00\x00\x90\xEB',
        #     'pulsewidthajust':b'\xEB\x90\x02\xFF\xFF\x90\xEB',
        #     'frequencyajust':b'\xEB\x90\x03\xFF\xFF\x90\xEB',
        #     'hellocom':b'\xEB\x90\x10\x00\x00\x90\xEB'
        #     }

        #send command to control device
        self.sendmsg = {
            'sendcurrent':b'sendcurrent0000',
            'openlaser':b'openlaser000000',
            'closelaser':b'closelaser00000',
            'pulsewidthajust':b'pulsewidthajust',
            'frequencyajust':b'frequencyajust0',
            'hellocom':b'hellocom0000000',
            'openseed':b'openseed0000000',
            'open1st':b'open1st00000000',
            'open2sr':b'open2sr00000000',
            '1stajust':b'1stajust0000000',
            '2stajust':b'2stajust0000000'
            }

        # TODO
        # Configuration for line ending
        #self.config     = {'eol':['','\n','\r','\r\n']}

    def run(self):
        '''
        Run thread.
        In every iteration trying to read one line from serial port and put
        it in queue.
        '''
        try:
            while self.running:
                data = None
                #sleep(1)
                try:
                    data = self.readline()
                except SerialException:
                    pass

                    #print('Error occured while reading data.')
                try:
                    if len(data)>0:
                        print('上位机接收：',data)
                        self.queue.put(data.strip())
                except Exception as e:
                    data=b'-1'


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

    def set_port(self, port):
        self.ser.close()
        sleep(0.1)
        self.port=port
        self.begin()
        #self.ser = serial.Serial( port, self.br, timeout=120)

        # try:
        #     if not self.ser._port_handle:
        #         print(self.ser._port_handle)

        #     self.ser.port = self.port
        #     self.ser.open()
        # except SerialException:
        #     self.emit_error('Can\'t open this port: ' + str(port) + '.')




    def get_port(self):
        return self.port

    def set_br(self, baudrate):
        self.br = baudrate
        self.ser.baudrate = self.br

    def get_br(self):
        return self.br

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
        dataSend=self.sendmsg.get(data)
        #print(dataSend)
        if dataSend:
            print('上位机发送:',dataSend)
            self.ser.write(dataSend)

        sleep(0.1)

    def readline(self):
        try:
            data = self.ser.read(15)
        except Exception as e:
            raise e

        #print(data)
        return data#.decode('ASCII')


#==============================================================================
# Signals
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)
