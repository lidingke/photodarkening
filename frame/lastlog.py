from model.toolkit import WRpickle
from model.singleton import MetaDict, singleton

class LastLog(WRpickle, MetaDict):
    """docstring for LastLog"""
    def __init__(self,name = 'data\\lastlog.pickle'):
        super(LastLog, self).__init__(name)
        print(name)
