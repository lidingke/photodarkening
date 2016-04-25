
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot
def func(x, a, c):
    return a * x**(-1) + c


xdata = [90,    80,     70,   60,     56, 50, 40, 30, 20, 11.4,  8, 5.5, 4, 3.5, 2]
ydata = [-18, -15.5, -14, -11.5, -10,  -8, -4,  1.5, 9.9, 20,   30, 40, 50, 60, 70]

popt, pcov = curve_fit(func, xdata, ydata)

print(popt)
# print(pcov)

def funout(x):
    return popt[0] * x**(-1) + popt[1]

y = funout(8.95)
print(y)

def plotpopt(x):
    y2 = [funout(i) for i in x]
    print(funout(8.95))
    pyplot.plot(x,y2, hold = True)
    while ydata:
        print('y:',ydata.pop(),y2.pop())
    return pyplot

pl = plotpopt(xdata)
pl.show()

