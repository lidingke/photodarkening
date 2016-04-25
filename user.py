
from PyQt5.QtWidgets import (QLabel,QLineEdit, QGridLayout, QHBoxLayout, QPushButton,
    QVBoxLayout,QWidget,QLCDNumber,QListWidget,QListWidgetItem)
from PyQt5.QtCore       import pyqtSignal
# from viewtool import TabWidget
import hashlib
import pickle
import pdb
# from regest import Regester
from PyQt5.QtWidgets import QDialog
from regesterview import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType
form_class, base_class = loadUiType('regesterview.ui')

class Regester(QDialog, form_class):
    """docstring for Regester"""
    pass2father = pyqtSignal(object)
    def __init__(self):
        super(Regester, self).__init__()
        # self.arg = arg
        # self.ui = Ui_Dialog()
        self.setupUi(self)
        self.setModal(True)
        # self.pass2father.connect(father.getsignal)
        self.levelitems = ['master','worker','user','guest']
        self.level.addItems(self.levelitems)
        self.save.clicked.connect(self.getUser)
        self.level.setCurrentIndex(2)
        self.password.setEchoMode(QLineEdit.Password)
        self.passwordagain.setEchoMode(QLineEdit.Password)


    def getUser(self):
        self.name = self.username.text()
        self.password1 = self.password.text()
        self.password2 = self.passwordagain.text()
        self.types = self.level.currentText()
        # pdb.set_trace()
        print(self.password1 ,':', self.password2,type(self.password1),type(self.password2))
        if self.password1 == self.password2:
            self.pass2father.emit((self.name,self.password1,self.types))
            self.accept()



class UserView(QWidget):
    """docstring for UserView"""

    usersignal = pyqtSignal(object)

    def __init__(self):
        super(UserView, self).__init__()
        self.UI_init()
        self.userboss = UserManager()


    def UI_init(self):
        mainLayout = QGridLayout()
        namelabel = QLabel('user')
        self.nameIput = QLineEdit()
        passlabel = QLabel('password')
        self.passwordIput = QLineEdit()
        self.passwordIput.setEchoMode(QLineEdit.Password)
        self.login= QPushButton('login')
        self.login.status = 'login'
        self.login.clicked.connect(self.loginfun)
        # self.logout = QPushButton('logout')
        # self.logout.clicked.connect(self.logoutfun)

        self.register = QPushButton('register')
        self.register.setEnabled(True)

        self.register.clicked.connect(self.registerfun)
        mainLayout.addWidget(namelabel, 0, 0)
        mainLayout.addWidget(passlabel, 0, 1)
        mainLayout.addWidget(self.nameIput, 1, 0)
        mainLayout.addWidget(self.passwordIput, 1, 1)
        mainLayout.addWidget(self.login, 2, 0)
        # mainLayout.addWidget(self.logout, 2, 1)
        mainLayout.addWidget(self.register, 2, 1)
        # mainLayout.addWidget(self.save, 3, 1)

        self.setLayout(mainLayout)

    def loginfun(self):
        if self.login.status == 'login':

            name = self.nameIput.text()
            password = self.passwordIput.text()
            self.userboss.loadUsers()
            use = self.userboss.findUser(name)
            useA = use.isPass(password)
            if useA:
                self.usersignal.emit(use)
                self.login.status = 'logout'
            print('use:',useA)
        elif self.login.text() == 'logout':
            use = User()
            self.usersignal.emit(use)
            self.login.status = 'login'


    # def logoutfun(self):
    #     pass

    def registerfun(self):
        re = Regester()
        re.pass2father.connect(self.getsignal)
        re.exec_()
            # pass

    def getsignal(self,arg):
        use = User()
        use.setUser(arg[0], arg[1] , arg[2])
        self.userboss.insertUser(use.getName(), use)
        self.userboss.saveUsers()
        print('father get :',arg[0], arg[1] , arg[2])


class UserManager(object):
    """docstring for UserManager"""
    def __init__(self):
        super(UserManager, self).__init__()
        self.users = dict()
        # self.us = User()
        # self.loadUsers()

    def saveUsers(self):
        print('save a user.pickle len = ',len(self.users))
        with open('user.pickle', 'wb') as f:
            pickle.dump(self.users, f)

    def loadUsers(self):
        with open('user.pickle', 'rb') as f:
            self.users = pickle.load(f)
        print(self.users)

    def findUser(self,name):
        return self.users.get(name,User())

    def insertUser(self,name,user):
        print('insert users :')
        self.users[name] = user

    def delUser(self,name):
        self.users.pop(name)


class User(object):
    """docstring for User"""
    def __init__(self,name = False):
        super(User, self).__init__()
        self.name = name
        self.password = False
        self.level = '1'
        self.types = 'user'
        self.hashkey1 = 'YOFC'
        self.hashkey2 = 'CFOY'
        self.leveldict = {
        'master':1,'worker':2,'user':3,'guest':4}

    def setName(self,value):
        if self.name is False:
            self.name = value
        else:
            raise ValueError('name can only be named once')

    def setPassword(self,value):
        if self.name is not False:
            self.password = self.__MD5value(value)
            print(self.password)
        else:
            raise ValueError('the is not a user name')

    def __MD5value(self,value):
        md = hashlib.sha1()
        if type(value) is not str:
            raise TypeError('value is not str')
        value = self.hashkey1+value +self.hashkey2
        md.update(value.encode('utf-8'))
        return md.hexdigest()

    def isPass(self,value):
        if type(value) is not str:
            raise TypeError('value is not str')
        # value = self.hashkey1+value +self.hashkey2
        newvalue = self.__MD5value(value)
        print(newvalue)
        if newvalue == self.password:
            return True
        else:
            return False

    def setLevel(self,value):
        self.level = value

    def setType(self,value):
        self.types = value

    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

    def getLevel(self):
        return self.level

    def getType(self):
        return self.types

    def setUser(self,name,password,types):
        level = self.leveldict.get(types,10)
        self.setName(name)
        self.setPassword(password)
        self.setLevel(level)
        self.setType(types)

    def getUser(self):
        us = (self.name,self.password,self.types)
        return us

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = UserView()
    addressBook.show()

    sys.exit(app.exec_())
