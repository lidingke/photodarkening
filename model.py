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
        self.msgDict = {
            'sendcurrent':b'\xEB\x90\x01\xFF\xFF\x90\xEB',
            'openlaser':b'\xEB\x90\x00\x00\x01\x90\xEB',
            'closelaser':b'\xEB\x90\x00\x00\x00\x90\xEB',
            'pulsewidthajust':b'\xEB\x90\x02\xFF\xFF\x90\xEB',
            'frequencyajust':b'\xEB\x90\x03\xFF\xFF\x90\xEB',
            'hellocom':b'\xEB\x90\x10\x00\x00\x90\xEB',
            'openseed':b'\xEB\x90\x01\x00\x00\x01\x90\xEB',
            'openseedreturn':b'\xEB\x90\x01\x00\x00\x01\x90\xEB',

            }


    def run(self):
        '''
        Run thread.
        In every iteration trying to read one line from serial port and put
        it in queue.
        thread class
        run(self)
     |      Method representing the thread's activity.
     |
     |      You may override this method in a subclass. The standard run() method
     |      invokes the callable object passed to the object's constructor as the
     |      target argument, if any, with sequential and keyword arguments taken
     |      from the args and kwargs arguments, respectively.

        '''
        try:
            while self.running:
                data = None
                #sleep(1)
                #data = self.readline()
                data = self.analysisbit()
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

    def set_port(self,port):
        self.port = port



    def reset_port(self, port):
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


    def get_msgDict(self):
        return self.msgDict

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

    def readline(self):
        try:
            data = self.ser.read(15)
        except Exception as e:
            raise e
        return data

    def readbit(self):
        sleep(0.1)
        try:
            data = self.ser.read(1)
        except Exception as e:
            raise e
        return data

    def msgcoup(self,msg):
        msg = self.msgDict.get(msg)
        if len(msg) > 0:
            return msg
        else:
            return b'\xEB\x90'+msg+b'\x90\xEB'

    def analysisbit(self):

        readlive = True
        # xebstatue = False
        # x90statue = False
        bitlist = list()
        while readlive and self.running:
            databit = self.readbit()
            if databit == b'\xeb':
                # print(databit,'1')
                databit = self.readbit()
                if databit == b'\x90':
                    while True:
                        #print(databit,'2')
                        databit = self.readbit()
                        if databit == b'\x90':
                            databit = self.readbit()
                            return b''.join(bitlist)
                        bitlist.append(databit)


            # databit = self.readbit()
            # print(databit)
            # if databit == b'\xEB':
            #     xebstatue = not xebstatue
            # elif databit == b'\x90':
            #     x90statue = not x90statue
            # else:
            #     pass
            # print(xebstatue,':',x90statue)
            # if xebstatue and x90statue:
            #     self.bitlist.put(databit)
            # elif xebstatue and not x90statue:
            #     pass
            # else:
            #     readlive = False
            #     #xebstatue = False
            #     #x90statue = False
            # if bitlist.qsize() > 0:
            #     print(bitlist.qsize())
            #     return b''.join(bitlist)


#==============================================================================
# Signals
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)
