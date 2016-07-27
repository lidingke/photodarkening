
from model.modelcore import ModelCore
from PyQt5.QtCore import pyqtSignal
import threading
import time
from model.database import DataHand
import pdb
from model.toolkit import HexSplit
import collections
# from dataSaveTick import DataSaveTick
import queue

class ModelPump(ModelCore):
    """docstring for ModelPump"""
    def __init__(self,):
        super(ModelPump, self).__init__()
        # self.arg = arg


    def closePortPump(self):
        self.closePort()

    def baundrateIndexChanged(self,baudrate):
        self.set_br(int(baudrate))

    def portPump(self,port):
        self.set_port(port)
