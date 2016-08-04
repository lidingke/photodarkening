#qt tool
from PyQt5.QtWidgets    import (QWidget, QVBoxLayout,
    QHBoxLayout, QPlainTextEdit, QApplication, QLineEdit)
from PyQt5.QtCore import Qt, QObject, pyqtSignal
#python tool
from queue              import Queue
import sys
sys.path.append("..")
import pdb

from UI.portGBUI import Ui_GroupBox as PortGBUI
from UI.pumpUI import Ui_GroupBox as PumpUI
from UI.tabboxUI import Ui_Form as TabBoxUI
# from UI.powerUI import Ui_Form as PowerUI
# from portGBUI import Ui_GroupBox as PortGBUI

from view.matplotlibPyQt5 import MyDynamicMplCanvas
from view.powershow import PowerShow
from view.powerrecord import PowerRecord
from view.user import UserView
from view.user import User
# from model.lastlog import LastLog
from frame.lastlog import LastLog
# from frame

class View(QWidget):
    """build from photodarker view"""
    startPumpModel = pyqtSignal(object)
    setBaundratePortSignal = pyqtSignal(object,object)
    # setSignal = pyqtSignal(object)


    def __init__(self,):
        super(View, self).__init__()
        QWidget.__init__(self)
        # self.arg = arg

        self.__initUI()
        self.queue      = Queue()
        # self.lastLog = LastLog()
        self._setLastLog()


    def __initUI(self):
        self.tabBoxUI = TabBoxUI()
        self.tabBoxUI.setupUi(self)

        self.__initUserUI()
        self.__initPort()
        self.__initLog()
        self.__initMatplotUI()
        self.__initPowerShow()

    def __initUserUI(self):
        self.myUserUI = MyUserUI(self.tabBoxUI)

    def __initPort(self):
        menuItem = ['300 baud','1200 baud',
            '2400 baud','4800 baud','9600 baud',
            '19200 baud','38400 baud','57600 baud',
            '115200 baud','230400 baud','250000 baud']
        self.tabBoxUI.baundratePump.addItems(menuItem)
        portItem = ['com1','com2','com3','com4',
            'com5','com6','com7','com8','com9',
            'com10','com11','com12','com13',
            'com14','com15','com16','com17',
            'com18','com19','com20']
        self.tabBoxUI.portPump.addItems(portItem)
        self.tabBoxUI.baundratePump.currentIndexChanged.connect(self.emitBaundratePort)
        self.tabBoxUI.portPump.currentIndexChanged.connect(self.emitBaundratePort)

    def __initMatplotUI(self):
        matplot = self.tabBoxUI.matplot
        self.painter = MyDynamicMplCanvas(matplot, width=5, height=4, dpi=100)
        # self.tabBoxUI.mainLayout.replaceWidget(matplot,self.painter)

    def __initPowerShow(self):
        self.powerShow1 = PowerShow()
        self.powerShow2 = PowerShow()
        self.powerShow3 = PowerShow()
        # self.tabBoxUI.canvas.hide()
        # self.tabBoxUI.canvas = self.powerShow3
        # self.tabBoxUI.canvas2.hide()
        # self.tabBoxUI.canvas2 = self.powerShow1
        # pdb.set_trace()
        self.tabBoxUI.cmdLayout.addWidget(self.powerShow1)
        # self.tabBoxUI.cmdLayout.replaceWidget(self.tabBoxUI.canvas, self.powerShow2)
        # self.tabBoxUI.cmdLayout.update()
        self.tabBoxUI.cmdLayout.addWidget(self.powerShow2)
        self.tabBoxUI.cmdLayout.addWidget(QPlainTextEdit())
        # self.tabBoxUI.mainLayout.setLayout(self.tabBoxUI.cmdLayout)

    def __initLog(self):
        self.powerLog = PowerLog(self.tabBoxUI)

    def _setLastLog(self):
        self.lastLog = LastLog()
        print('lastlog dict:', self.lastLog)
        userName = self.lastLog.get('username','')
        password = self.lastLog.get('password','')
        baudIndex = self.lastLog.get('baud', 4)
        portIndex = self.lastLog.get('port', 0)

        self.tabBoxUI.userName.setText(userName)
        self.tabBoxUI.passwordIput.setText(password)
        self.tabBoxUI.baundratePump.setCurrentIndex(baudIndex)
        self.tabBoxUI.portPump.setCurrentIndex(portIndex)

    def lastLogSave(self):
        self.lastLog['username'] = self.tabBoxUI.userName.text()
        self.lastLog['password'] = self.tabBoxUI.passwordIput.text()
        self.lastLog['baud'] = self.tabBoxUI.baundratePump.currentIndex()
        self.lastLog['port'] = self.tabBoxUI.portPump.currentIndex()
        self.lastLog.saveLast()

    def __setUser(self,value):
        pass

    def set_queue(self, queue):
        self.queue = queue

    def set_end_cmd(self, end_cmd):
        self.end_cmd = end_cmd

    def emitBaundratePort(self):
        bp = self.getBaundratePort()
        self.setBaundratePortSignal.emit(bp[0],bp[1])

    def getBaundratePort(self):
        port = self.tabBoxUI.portPump.currentText()
        baundrate = self.tabBoxUI.baundratePump.currentText()[:-5]
        return (port,baundrate)

    # def setPort(self):
    #     self.setPortSignal.emit()

    def update_gui(self):
        # self.process_incoming()
        self.update()

    # def set_end_cmd(self,end_cmd):
    def closeEvent(self, event):
        self.lastLogSave()
        print('last log ',self.lastLog)
        QWidget.closeEvent(self, event)

class MyUserUI(UserView,QObject):
    """docstring for myUserUI"""
    def __init__(self,father):
        self.father = father
        super(MyUserUI, self).__init__()
        QObject.__init__(self)

    def UI_init(self):
        self.passwordIput = self.father.passwordIput
        self.login = self.father.login
        self.register = self.father.userRegister
        self.nameIput = self.father.userName
        self.passwordIput.setEchoMode(QLineEdit.Password)
        self.login.status = 'login'
        self.login.clicked.connect(self.loginfun)
        self.register.clicked.connect(self.registerfun)

from view.powerrecord import PowerRecord
class PowerLog(PowerRecord, QObject):
    """docstring for PowerLog"""
    def __init__(self, father):
        self.father = father
        super (PowerLog, self).__init__()
        # self.arg = arg


    def _setupUi(self):
        self.logButton = self.father.logButton
        self.stepEdit = self.father.stepEdit
        self.printButton = self.father.printButton
        self.timeEdit = self.father.timeEdit
        self.gridLayout_2 = self.father.logGridLayout
        self.gridLayout = self.father.historyGridLayout
        self.ticker = self.father.ticker
        # self.ticker = self
        # pass



if __name__ == '__main__':
    app         = QApplication(sys.argv)
    gui         = View()

    gui.show()

    sys.exit(app.exec_())
