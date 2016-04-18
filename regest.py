from PyQt5.QtWidgets import QWidget
from regesterview import Ui_Dialog
from PyQt5.QtWidgets import QApplication

class Regester(QWidget):
    """docstring for Regester"""
    def __init__(self):
        super(Regester, self).__init__()
        # self.arg = arg
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.level = ['master','worker','user','guest']


if __name__ == "__main__":
    import sys
    app =  QApplication(sys.argv)
    re = Regester()
    re.show()
    sys.exit(app.exec_())
