#!/usr/bin/env python
# coding=utf-8

from time import sleep
from model import Model

class Presenter:

    def __init__(self, view):

        self.__model = Model()
        self.__view = view
        self.__view.show()
        self.__view.baudrate_changed.connect(self.__model.set_br)
        self.__view.port_changed.connect(self.__model.reset_port)
        self.__view.openPortButton.clicked.connect(self.modelBegin)
        #sleep(30)
        #self.modelBegin()
        self.__view.set_queue(self.__model.get_queue())
        self.__view.set_end_cmd(self.end_cmd)
        self.__view.set_port(self.__model.get_port())

        # Run communication and start thread

        self.__view.update_gui()

    def end_cmd(self):
        self.__model.stop()

    def modelBegin(self):

        if self.__model.isAlive() is False:
            print('===openPort===')
            self.__model.begin()
            try:
                self.__model.start()
            except RuntimeError:
                print('RuntimeError: threads can only be started once. ser = ',self.__model.get_ser())


            # Signal connection
            self.__view.send_data.connect(self.__model.write)
            self.__model.error.connect(self.__view.show_error)


            self.__model.cValue.connect(self.__view.setCurrentValue)
            self.__view.seedPulseChanged.connect(self.__model.writeSeedPulse)
            self.__view.seedFreValueChanged.connect(self.__model.writeSeedFre)

        else:

            print('不能重复打开port')


