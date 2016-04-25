import numpy as np
from matplotlib import pyplot
import pdb

def fun1(lit = -1):

    z = np.polyfit(x, y, lit)
    pfit = np.poly1d(z)
    print('p:',pfit )
    y2 = [pfit(i) for i in x]
    print(pfit(8.95))
    pyplot.plot(x,y2, hold = True)
    return pyplot


for x in range(5,10):
    pl = fun1(lit = -1)
pl.show()


