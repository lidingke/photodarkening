import pickle
from model.toolkit import WRpickle
from view.user import User
# import WRpickle
# from re import findall
import pdb

class LastLog(WRpickle):
    """docstring for LastLog"""
    def __init__(self,name = 'data\\lastlog.pickle'):
        super(LastLog, self).__init__(name)
        # self.arg = arg
        # self.pickname = name
        self.pick = {}

    def loadLast(self):
        self.pick = self.loadPick()
        return self.pick

    def saveLast(self,pick):
        # print('saveLast',pick)
        self.savePick(pick)

# rewrite insertItem
    def insertItem(self,key,item):
        if type(key) is not str:
            raise TypeError('key must be a str')
        self.pick[key] = item

class MsgSet(object):
    """docstring for MsgSet"""
    def __init__(self):
        super(MsgSet, self).__init__()
        self.msg = {}
        self.msgDictStr = {

#=======pump==========
        #first pump
        'openpump':                        ' EB 90 02 00 0A 00 01 90 EB',
        'closepump':                        ' EB 90 02 00 0A 00 00 90 EB',
        #set pump current
        'setcurrent':                          ' EB 90 02 01 0A FF FF 90 EB',
        #power caculate
        'powerandtemp':                        '9A FF FF FF FF FF FF FF FF A9'


        }

    def msgProccess(self):
        msg = self.msg
        msg['msgDictStr'] = self.msgDictStr
        msgDictHex = dict()

        for k,v in self.msgDictStr.items():
            msgDictHex[k] = b''.fromhex(v) #v.replace(b" ",b"\x")
        #self.msgDict = self.msgDictHex
        msgDictHexNoRe = {}
        print(msgDictHex)
        for k,v in msgDictHex.items():
            if k[-6:] != 'return':
                msgDictHexNoRe[k] = v

        sendmsgrec = dict([(v,k) for k,v in msgDictHexNoRe.items()])
        msg['msgDictHex'] = msgDictHex
        msg['sendmsgrec'] = sendmsgrec
        print(sendmsgrec)
        print('len,msgDictHex,sendmsgrec',len(msgDictHex),len(sendmsgrec))

        with open('data\\msg.pickle', 'wb') as f1:
            pickle.dump(msg, f1)


if __name__ == '__main__':
    pc = LastLog()
    pick = pc.loadLast()
    print(pick)
    pdb.set_trace()
    pass

