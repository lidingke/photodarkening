import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
# from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot
import threading
import datetime
import pdb

#branch


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor = 'white' )
        self.fig = fig
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel('Time(s)')
        self.axes.set_ylabel('Power(W)')
        self.axes.grid(True)
        self.isStartLog = False
        self.lasty = 1
        self.xlist = [0]
        self.y1list = [0]
        self.y2list = [0]
        self.yMax = 1
        self.xpoint = 0
        self.y1point = 0
        self.y1point = 0

        self.timeStatesec = 0
        self.xunit = 'sec'
        self.isPloting = True

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 'r')


    def update_figure(self):
        if self.y1list:
            try:
                hugeNumAvoid = abs(self.y1list[-1]/self.lasty)
                if hugeNumAvoid >100 or hugeNumAvoid < 0.001:
                    return
            except ZeroDivisionError:
                pass
            if self.isStartLog == False:
                self.beforeLog()
            else:
                self.afterLog()
            self.lasty = self.y1point

    def beforeLog(self):
            self.axes.plot(self.xlist, self.y1list, 'r',\
                           self.xlist, self.y2list, 'b')

            if self.y1list[-1] < 1:
                self.axes.set_ylim(0,1)
            self.draw()

    def getStartLog(self,bool_ ):
        self.isStartLog = bool_

    def getLogTimeState(self,tp ):
        self.timeStatesec = tp
        print(self.timeStatesec,'timeStatesec')
        if self.timeStatesec>3600:
            self.xunit = 'hour'
            self.timended = (self.timeStatesec/3600)*1.2
        elif self.timeStatesec > 300:#5min
            self.xunit = 'min'
            self.timended = (self.timeStatesec/60)*1.2
        else:
            self.xunit = 'sec'
            self.timended = self.timeStatesec
        print('timsec',self.timeStatesec)

    def afterLog(self):
            self.axes.plot(self.xlist, self.y1list, 'r')
            xlimit = self.timended
            self.axes.set_xlim(0,xlimit)
            if self.y1list[-1] < 1:
                self.axes.set_ylim(0,1)
            else:
                self.axes.set_ylim(0,self.y1point*1.5)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel('Power')
            self.axes.grid(True)
            self.draw()

    def savePlotFig(self):
        def savefigThread(self):
            self.fig.savefig("data\\plot.svg", format = 'svg')#data\
        threading.Thread(target = savefigThread, daemon = True).start()



        # self.axes.plot(self.xlist, self.y1list, 'r')
        # import matplotlib.pyplot as plt
        # plt.plot(range(10))
        # plt.savefig('testplot.png')

    def XYaxit(self,x,y1,y2):
        if self.isPloting:
        # print('x_sec:',x,'xunit:',self.xunit)
        # pdb.set_trace()
            x = self.sec2HourOrMin(x)
            # print('x_min:',x)
            if x:
                self.xpoint = x
                self.y1point = y1
                self.y2point = y2
                self.xlist.append(x)
                self.y1list.append(y1)
                self.y2list.append(y2)
        self.update_figure()

    def XYaxitList(self,is_,x,y):
        self.isPloting = is_
        print('getplot ',is_)
        self.xlist = x
        self.y1list = y
        self.axes.plot(self.xlist, self.y1list, 'r')
        # if self.y1list[-1] < 1:
        #     self.axes.set_ylim(0,1)
        self.draw()


    def sec2HourOrMin(self,x):
        if self.xunit == 'sec':
            return x
        elif self.xunit == 'min':
            return x/60
        elif self.xunit == 'hour':
            return x/3600
        else:
            return x

    def setisPloting(self,is_):
        self.isPloting = is_


    def clearPlotList(self,is_):
        self.xlist.clear()
        self.y1list.clear()
        self.isPloting = is_

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        # sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        # l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
"""embedding_in_qt5.py example
Copyright 2015 BoxControL

This program is a simple example of a Qt5 application embedding matplotlib
canvases. It is base on example from matplolib documentation, and initially was
developed from Florent Rougon and Darren Dale.

http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("PyQt5 Matplot Example")
    aw.show()
    #sys.exit(qApp.exec_())
    app.exec_()





