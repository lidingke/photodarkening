from PyQt5.QtWidgets import QDialog
from regesterview import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType
from user import User
from user import UserManager
form_class, base_class = loadUiType('regesterview.ui')

class Regester(QDialog, form_class):
    """docstring for Regester"""
    def __init__(self):
        super(Regester, self).__init__()
        # self.arg = arg
        # self.ui = Ui_Dialog()
        self.setupUi(self)
        self.levelitems = ['master','worker','user','guest']
        self.level.addItems(self.levelitems)
        self.save.clicked.connect(self.saveuser)
        self.level.setCurrentIndex(2)


    def saveuser(self):
        self.name = self.username.text()
        self.password1 = self.password.text()
        self.password2 = self.passwordagain.text()
        self.types = self.level.currentText()
        if self.password1 is not self.password2:
            return
        us = User()
        us.setUser(self.name, self.password, self.types)
        usm = UserManager()
        usm.loadUsers()
        usm.insertUser(us.getName, us)
        usm.saveUsers()


if __name__ == "__main__":
    import sys
    app =  QApplication(sys.argv)
    re = Regester()
    re.show()
    sys.exit(app.exec_())
