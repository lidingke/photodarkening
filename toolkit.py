import pickle

class WRpickle(object):
    """docstring for WRpickle
    input a pick name
    """
    def __init__(self, arg):
        super(WRpickle, self).__init__()
        self.pickname = arg
        try:
            self.pick = self.loadPick()
        except Exception as e:
            raise e

    def loadPick(self):
        with open(self.pickname,'rb') as f:
            self.pick = pickle.load(f)
        return self.pick

    def savePick(self,pick):
        with open(self.pickname,'wb') as f:
            # print('savePick',pick)
            pickle.dump(pick,f)

    def insertItem(self,key,item):
        if type(key) is not str:
            raise TypeError('key must be a str')
        self.pick[key] = item


import threading
from queue import Queue
from modelpump import ModelPump
from time import sleep

class portGard(threading.Thread):
    """docstring for portGard"""
    def __init__(self):
        super(portGard, self).__init__()
        self.msgQueue = Queue()
        self.modelList = list()
        # self.m = ModelPump()

    def getmodels(self,model):
        self.modelList.append(model)

    def getQueue(self):
        return self.msgQueue

    def run(self):

        while True:
            for x in self.modelList:
                # print(x)
                if x.isAlive == False:
                # x.isAlive
                    print('thread is killed',x)
                # print(x.ser)
                sleep(10)



if __name__ == '__main__':
    m = ModelPump()
    p = portGard()

    m.begin()
    m.start()
    m.port = 'com14'
    m.reSetPort()
    p.getmodels(m)
    p.start()
