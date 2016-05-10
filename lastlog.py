import pickle
from toolkit import WRpickle
# import WRpickle
# from re import findall

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
        # self.arg = arg
# from threading import Thread
        self.msg = {}
        self.msgDictStr = {
#===========seed===========
        #open seed \x00
        'openseed':                                   ' EB 90 01 00 00 01 90 EB',
        'openseedreturn':                         ' EB 90 01 00 00 01 90 EB',
        'openseederror':                           ' EB 90 01 00 10 00 90 EB',
        #close seed \x00
        'closeseed':                                  ' EB 90 01 00 00 00 90 EB',
        'closeseedreturn':                        ' EB 90 01 00 00 00 90 EB',
        'openseederror':                           ' EB 90 01 00 10 00 90 EB',
        # seed current \x01
        'seedcurrentvalueset':                 ' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvaluesetreturn':        ' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvalueseterror':         ' EB 90 01 01 10 00 90 EB',
        # seed pulse \x02
        'seedpulseset':                            ' EB 90 01 02 FF FF 90 EB',
        'seedpulsesetreturn':                  ' EB 90 01 02 FF FF 90 EB',
        'seedpulseseterror':                    ' EB 90 01 02 10 00 90 EB',
        # seed fre \x03
        'seedfreset':                                ' EB 90 01 03 FF FF 90 EB',
        'seedfresetreturn':                      ' EB 90 01 03 FF FF 90 EB',
        'seedfreseterror':                       ' EB 90 01 03 10 00 90 EB',
        #seed current \x04
        'seedcurrentvalueget':               ' EB 90 01 04 90 EB',
        'seedcurrentvaluegetreturn':      ' EB 90 01 04 FF FF 90 EB',
        'seedcurrentvaluegeterror':        ' EB 90 01 04 10 00 90 EB',
        #seed pluse \x05
        'seedpulseread':                        ' EB 90 01 05 90 EB',
        'seedpulsereadreturn':              ' EB 90 01 05 FF FF 90 EB',
        'seedpulsereaderror':                ' EB 90 01 05 10 00 90 EB',
        #seed frequance \x06
        'seedfreread':                            ' EB 90 01 06 90 EB',
        'seedfrereadreturn':                  ' EB 90 01 06 FF FF 90 EB',
        'seedfrereaderror':                    ' EB 90 01 06 10 00 90 EB',
        #test send plot
        'sendplot':                                  ' EB 90 01 11 FF FF 90 EB',
        #open and close seed LED
        'openseedLED':                        ' EB 90 02 00 05 00 01 90 EB',
        'closeseedLED':                       ' EB 90 02 00 05 00 00 90 EB',
#=======pump==========
        #first pump
        'openfirstpump':                        ' EB 90 02 00 0A 00 01 90 EB',
        'closefirstpump':                        ' EB 90 02 00 0A 00 00 90 EB',
        #second pump
        'opensecondpump':                   ' EB 90 02 00 0B 00 01 90 EB',
        'closesecondpump':                  ' EB 90 02 00 0B 00 00 90 EB',
        #set pump current
        'setfirstcurrent':                          ' EB 90 02 01 0A FF FF 90 EB',
        'setsecondcurrent':                    ' EB 90 02 01 0B FF FF 90 EB',
        # pumperror
        'pumperror':                               ' EB 90 02 FF FF FF FF 90 EB',
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
    ms = MsgSet()
    ms.msgProccess()
