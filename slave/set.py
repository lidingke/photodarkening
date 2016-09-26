
def singlenton(class_):
    instance = {}
    def getinstance(*args,**kwargs):
        if class_ not in instance:
            instance[class_] = class_(*args,**kwargs)
        return instance[class_]
    return getinstance

@singlenton
class SourcePowerPara(object):
    """docstring for ClassName"""
    def __init__(self,):
        SourcePowerPara.__init__()
        self.POWER = 0
