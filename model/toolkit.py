import pickle
import sys
import pdb
import json
# from view.user import User

class WRpickle(object):
    """docstring for WRpickle
    input a pick name
    """
    def __init__(self, arg):
        super(WRpickle, self).__init__()
        self.pickname = arg
        self.pick = {}


    def loadPick(self):
        with open(self.pickname,'rb') as f:
            # print('f',f)
            try:
                self.pick = pickle.load(f)
            except Exception as e:
                # raise e
                pass
            # print('load',self.pick)
        return self.pick

    def savePick(self,pick):
        with open(self.pickname,'wb') as f:
            # print('savePick',pick)
            pickle.dump(pick,f)

    def insertItem(self,key,item):
        if type(key) is not str:
            raise TypeError('key must be a str')
        self.pick[key] = item



class WriteReadJson(object):
    """docstring for WriteReadJson"""
    def __init__(self, dir_):
        super(WriteReadJson, self).__init__()
        self.dir_ = dir_
        self.store = {}

    def load(self):
        with open(self.dir_,'rb') as f:
            try:
                bitFileRead2Str = f.read().decode('utf-8')
                self.store = json.loads(bitFileRead2Str)
            # except FileNotFoundError:

            except Exception as e:
                # raise e
                print(e)
                pdb.set_trace()

        return self.store

    def save(self , store):
        with open(self.dir_,'wb') as f:
            jsonBitBuffer = json.dumps(store).encode('utf-8')
            # print('json', jsonBitBuffer)
            f.write(jsonBitBuffer)




import threading
from queue import Queue
# from modelpump import ModelPump
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

class HexSplit(object):
    """docstring for hexSplit"""
    def __init__(self):
        super(HexSplit, self).__init__()
        # self.arg = arg

    def fun(c):
        if type(c) != bytes:
            return
        return " ".join("{:02x}".format(x) for x in c)

from collections import MutableMapping

class MetaDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

if __name__ == '__main__':
    # m = ModelPump()
    # p = portGard()

    # m.begin()
    # m.start()
    # m.port = 'com14'
    # m.reSetPort()
    # p.getmodels(m)
    # p.start()

    # x = b'\x01\x02\x0e'
    # # x =
    # print(HexSplit.fun(x))
    wrj = WriteReadJson("test.json")
    wrjdict = {'1':2,'2':'34'}
    wrj.load()
    wrj.save(wrjdict)
