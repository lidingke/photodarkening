import collections
import pdb

class SoftFilter(object):
    """docstring for SoftFilter"""
    def __init__(self, ):
        super(SoftFilter, self).__init__()
        # self.arg = arg
        self.que = collections.deque( maxlen=5)

    def putIn(self,var):
        self.que.append(var)
        if len(self.que) == 5:
            lst = [x[0] for x in self.que]
            lst.sort()
            power = sum(lst[1:4])/3



    # def filterFun(self,que):
    #     lst = [x[0] for x in que]
    #     lst.sort()
    #     return sum(lst[1:4])/3


if __name__ == '__main__':
    testlist = [[3.5,'010203'],
    [3.4,'020304'],
    [3.2,'030405'],
    [3.1,'040506'],
    [3.7,'050607'],
    [3.8,'060708'],
    [3.5,'070809'],
    [3.2,'080910']


    ]

    softFilter = SoftFilter()
    for var in testlist:
        softFilter.putIn(var)

