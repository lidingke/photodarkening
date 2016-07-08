#qt tool
from PyQt5.QtWidgets    import (QWidget, QVBoxLayout,
    QHBoxLayout, QPlainTextEdit, QApplication, QLineEdit)
from PyQt5.QtCore import Qt
#python tool
import sys
sys.path.append("..")
import pdb
#DIY tool
from matplotlibPyQt5 import MyDynamicMplCanvas
from powershow import PowerShow
from UI.tabboxUI import Ui_Form as TabBoxUI
from user import UserView

class View(QWidget):
    """build from photodarker view"""
    def __init__(self,):
        super(View, self).__init__()
        # self.arg = arg
        self.__initUI()


    def __initUI(self):
        self.tabBoxUI = QWidget()
        tabboxtemp = TabBoxUI()
        tabboxtemp.setupUi(self.tabBoxUI)

        self.setWindowState(Qt.WindowMaximized)
        self.editer = QPlainTextEdit()
        self.editer.setReadOnly(True)
        paintwidget = QWidget()
        self.painter = MyDynamicMplCanvas(paintwidget, width=5, height=4, dpi=100)

        self.powerShow1 = PowerShow()
        self.powerShow2 = PowerShow()
        cmdBox = QVBoxLayout()
        cmdBox.addWidget(self.powerShow1)
        cmdBox.addWidget(self.powerShow2)
        cmdBox.addWidget(self.editer)
        showBox = QHBoxLayout()
        showBox.addLayout(cmdBox)
        showBox.addWidget(self.painter)
        self.mainBox = QVBoxLayout()
        self.mainBox.addWidget(self.tabBoxUI)
        # self.mainBox.addLayout(showBox)
        # pdb.set_trace()
        self.setLayout(self.mainBox)
        self.setWindowTitle("光子暗化平台软件")
        self.__initUserUI()

    def __initUserUI(self):
        # self.tabBoxUI.passwordIput
        myUserUI(self.tabBoxUI)
        # userbox.usersignal.connect()



class myUserUI(UserView):
    """docstring for myUserUI"""
    def __init__(self,father):
        self.father = father
        super(myUserUI, self).__init__()



    def UI_init(self):
        pdb.set_trace()
        self.passwordIput = self.father.passwordIput
        self.login = self.father.login
        self.register = self.father.register

        self.passwordIput.setEchoMode(QLineEdit.Password)
        self.login.status = 'login'
        self.login.clicked.connect(self.loginfun)
        try:
            self.register = self.register_2
        except:
            pass
        self.register.setEnabled(True)
        self.register.clicked.connect(self.registerfun)



if __name__ == '__main__':
    app         = QApplication(sys.argv)
    # pt = QPalette()
    # pt.setColor(QPalette.Background , QColor(239,246,250))
    # # pt.setColor(QPalette.Button, QColor(239,246,250))
    # pt.setColor(QPalette.ButtonText, QColor(34,39,42))
    # # pt.setColor(QPalette.WindowText, QColor(34,39,42))
    # pt.setColor(QPalette.Highlight, QColor(74,149,184))
    # app.setPalette(pt)
    font = app.font()
    font.setPointSize(10)
    font.setFamily('微软雅黑')

    app.setFont(font)

    gui         = View()

    gui.show()

    sys.exit(app.exec_())
