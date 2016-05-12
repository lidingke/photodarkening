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
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(1000)
        self.axes.set_xlabel('Time(s)')
        self.axes.set_ylabel('Power(W)')
        self.axes.grid(True)
        self.isStartLog = False
        self.lasty = 1
        self.xlist = list()
        self.ylist = list()
        self.timeState = datetime.time()
        self.timeStatesec = 0

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 'r')
        # self.axes.xticks([0.0,0.5,1.0])

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        # l = [random.randint(0, 10) for i in range(4)]
        if self.ylist:
            try:
                hugeNumAvoid = abs(self.ylist[-1]/self.lasty)
                if hugeNumAvoid >100 or hugeNumAvoid < 0.001:
                    return
            except ZeroDivisionError:
                pass
            print('isStartLog',self.isStartLog)
            if self.isStartLog == False:
                self.beforeLog()
            else:
                # self.getLogPlotPara()
                self.afterLog()
            self.lasty = self.ylist[-1]

    def beforeLog(self):
            self.axes.plot(self.xlist, self.ylist, 'r')
            if self.ylist[-1] < 1:
                self.axes.set_ylim(0,1)
            self.draw()

    def getStartLog(self,bool_ ):
        print('lg set ',bool_)
        self.isStartLog = bool_

    def getLogTimeState(self,pydatetime ):
        self.timeState = pydatetime
        tp = pydatetime
        self.timeStatesec = (tp.hour*60+tp.minute)*60+tp.second
        print('timsec',self.timeStatesec)

    def afterLog(self):
            self.axes.plot(self.xlist, self.ylist, 'r')
            # if self.timeState.hour > 0:
            self.axes.set_xlim(0,self.timeStatesec)
            print('setsec ',self.timeStatesec)
            if self.ylist[-1] < 1:
                self.axes.set_ylim(0,1)
            self.draw()

    def savePlotFig(self):
        pass
        # threading.Thread(target = self.savefigThread,daemon = True).start()

    def savefigThread(self):
        if self.xlist:
            pyplot.plot(self.xlist, self.ylist)
            pyplot.show()
            pyplot.savefig("d.png",dpi = 100)
        # self.axes.plot(self.xlist, self.ylist, 'r')
        # import matplotlib.pyplot as plt
        # plt.plot(range(10))
        # plt.savefig('testplot.png')

    def XYaxit(self,x,y):
        self.xlist = x
        self.ylist = y

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





