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
             pickle.dump(pick,f)

    def insertItem(self,key,item):
        if type(key) is not str:
            raise TypeError('key must be a str')
        self.pick[key] = item
