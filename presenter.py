#!/usr/bin/env python
# coding=utf-8


from model import Model

class Presenter:

    def __init__(self, view):

        self.__model = Model()
        self.__view = view

        # Run communication and start thread
        self.__model.begin()
        self.__model.start()

        # Signal connection
        self.__view.send_data.connect(self.__model.write)
        self.__view.baudrate_changed.connect(self.__model.set_br)
        #self.__view.eol_changed.connect(self.__model.set_eol)
        self.__view.port_changed.connect(self.__model.reset_port)

        self.__model.error.connect(self.__view.show_error)

        self.__view.set_queue(self.__model.get_queue())
        self.__view.set_end_cmd(self.end_cmd)
        self.__view.set_port(self.__model.get_port())
        self.__view.update_gui()

    def end_cmd(self):
        self.__model.stop()
