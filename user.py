
from PyQt5.QtWidgets import (QLabel,QLineEdit, QGridLayout, QHBoxLayout, QPushButton,
    QVBoxLayout,QWidget,QLCDNumber,QListWidget,QListWidgetItem)
from PyQt5.QtCore       import pyqtSignal
from viewtool import TabWidget
import hashlib
import pickle


class UserView(QWidget):
    """docstring for UserView"""

    usersignal = pyqtSignal(object)

    def __init__(self):
        super(UserView, self).__init__()
        self.UI_init()
        self.userboss = UserManager()


    def UI_init(self):
        mainLayout = QGridLayout()
        namelabel = QLabel('use')
        self.nameIput = QLineEdit()
        passlabel = QLabel('password')
        self.passwordIput = QLineEdit()
        self.login= QPushButton('login')
        self.login.clicked.connect(self.loginin)
        self.register = QPushButton('register')
        self.register.setEnabled(False)
        self.register.clicked.connect(self.enableRegister)
        self.insert = QPushButton('insert')
        self.insert.setEnabled(False)
        self.insert.clicked.connect(self.insertUser)
        self.save = QPushButton('save')
        self.save.setEnabled(False)
        self.insert.clicked.connect(self.saveInsert)
        mainLayout.addWidget(namelabel, 0, 0)
        mainLayout.addWidget(passlabel, 0, 1)
        mainLayout.addWidget(self.nameIput, 1, 0)
        mainLayout.addWidget(self.passwordIput, 1, 1)
        mainLayout.addWidget(self.login, 2, 0)
        mainLayout.addWidget(self.register, 2, 1)
        mainLayout.addWidget(self.insert, 3, 0)
        mainLayout.addWidget(self.save, 3, 1)

        self.setLayout(mainLayout)

    def loginin(self):
        name = self.nameIput.text()
        password = self.passwordIput.text()
        use = self.userboss.findUser(name)
        useA = use.isPass(password)
        if useA:
            self.usersignal.emit(use)
        print('use:',useA)

    def enableRegister(self):
        pass

    def insertUser(self):
        pass

    def saveInsert(self):
        pass


class UserManager(object):
    """docstring for UserManager"""
    def __init__(self):
        super(UserManager, self).__init__()
        self.users = dict()
        self.loadUsers()

    def saveUsers(self):
        print('save a user.pickle len = ',len(self.users))
        with open('user.pickle', 'wb') as f:
            pickle.dump(self.users, f)

    def loadUsers(self):
        with open('user.pickle', 'rb') as f:
            self.users = pickle.load(f)
        # except FileNotFoundError:
        #     self.users = dict()
        # except EOFError:
        #     self.users = dict()

# class Users(dict):
#     """docstring for Users"""
#     def __init__(self):
#         super(Users, self).__init__()
#         # self.arg = arg

    def findUser(self,name):
        return self.users.get(name,User())

    def insertUser(self,name,user):
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

    def setUser(self,name,password,level,types):
        self.setName(name)
        self.setPassword(password)
        self.setLevel(level)
        self.setType(types)

    def getUser(self):
        us = (self.name,self.password,self.level,self.types)
        return us

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = UserView()
    addressBook.show()

    sys.exit(app.exec_())
