from frame.singleton import MetaDict
from model.toolkit import WRpickle


def singleton(class_):
    instance = {}
    def getinstance(*args,**kwargs):
        if class_ not in instance:
            instance[class_] = class_(*args,**kwargs)
        return instance[class_]
    return getinstance

@singleton
class LastLog(WRpickle, MetaDict):
    """docstring for LastLog"""
    def __init__(self, name = 'data\\lastlog.pickle'):
        MetaDict.__init__(self)
        WRpickle.__init__(self, name)
        # self.pickname = name
        # self.store = self.pick
        self.store = self.loadPick()

    def saveLast(self):
        self.savePick(self.store)

