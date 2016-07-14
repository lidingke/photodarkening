
from PyQt5.QtWidgets import (QLabel,QLineEdit, QGridLayout, QPushButton,
    QVBoxLayout,QWidget,QLCDNumber,QListWidget,QListWidgetItem)
from PyQt5.QtCore       import pyqtSignal
# from viewtool import TabWidget
import hashlib
import pickle
import pdb
# from regest import Register
from PyQt5.QtWidgets import QDialog
from UI.registerUI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from UI.userUI import Ui_Form as userUI
# from PyQt5.uic import loadUiType
# form_class, base_class = loadUiType('Registerview.ui')

class Register(QDialog):
    """docstring for Register"""
    # passwdSignal1 = pyqtSignal(object)
    # passwdSignal2 = pyqtSignal(object)
    pass2father = pyqtSignal(object)

    def __init__(self):
        super(Register, self).__init__()
        # self.arg = arg
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.levelitems = ['master','worker','user','guest']
        self.ui.level.addItems(self.levelitems)
        self.ui.save.clicked.connect(self.saveuser)
        self.ui.level.setCurrentIndex(2)
        self.ui.msgtext.setText('')
        self.ui.password.textChanged.connect(self.passwdDetector)
        self.ui.passwordagain.textChanged.connect(self.passwdDetector)

        # self.passwdSignal1.connect(self.password1)
        # self.passwdSignal2.connect(self.password2)

    def saveuser(self):
        self.name = self.ui.username.text()
        self.password1 = self.ui.password.text()
        self.password2 = self.ui.passwordagain.text()
        self.types = self.ui.level.currentText()
        # print(self.password1.strip(),'\n',self.password2.strip())
        if self.password1.strip() != self.password2.strip():
            self.ui.msgtext.setText('密码不相等')
            return
        self.ui.msgtext.setText('保存用户')
        us = User()
        us.setUser(self.name, self.password1.strip(), self.types)
        usm = UserManager()
        # pdb.set_trace()
        if us.getName() in usm.users.keys():
            self.ui.msgtext.setText('用户已存在')
            return
        # usm.loadUsers()
        usm.insertUser(us.getName(), us)
        usm.saveUsers()

    def passwdDetector(self):
        pswd1 = self.ui.password.text()
        pswd2 = self.ui.passwordagain.text()
        if pswd2 or pswd1:
            if len(pswd1)<6 or len(pswd2)<6:
                self.ui.msgtext.setText('密码必须大于6位')
            elif len(pswd1)>18 or len(pswd2)>18:
                self.ui.msgtext.setText('密码必须小于18位')
            else:
                self.ui.msgtext.setText('')
            for x in pswd1, pswd2:
                # if (x.isdigit() or x.isalpha() ) is True:
                #     print('zhimushuz:',x.isdigit() ,x.isalpha(),x)
                if x.isalpha() or x.isdigit():
                    # print('alpha or digit:')
                    pass
                elif x == ' ':
                    self.ui.msgtext.setText('密码不能包含空格')
                else:
                    self.ui.msgtext.setText('密码必须为字母或数字')



class UserView(QWidget,userUI):
    """docstring for UserView"""

    usersignal = pyqtSignal(object)

    def __init__(self):
        super(UserView, self).__init__()
        self.UI_init()
        self.userboss = UserManager()


    def UI_init(self):
        self.setupUi(self)
        # mainLayout = QGridLayout()
        # namelabel = QLabel('user')
        # self.nameIput = QLineEdit()
        # passlabel = QLabel('password')
        # self.passwordIput = QLineEdit()
        self.passwordIput.setEchoMode(QLineEdit.Password)
        # self.login= QPushButton('login')
        self.login.status = 'login'
        self.login.clicked.connect(self.loginfun)
        # self.logout = QPushButton('logout')
        # self.logout.clicked.connect(self.logoutfun)
        try:
            self.register = self.register_2
        except:
            pass
        # self.register = QPushButton('register')
        self.register.setEnabled(True)

        self.register.clicked.connect(self.registerfun)
        # mainLayout.addWidget(namelabel, 0, 0)
        # mainLayout.addWidget(passlabel, 0, 1)
        # mainLayout.addWidget(self.nameIput, 1, 0)
        # mainLayout.addWidget(self.passwordIput, 1, 1)
        # mainLayout.addWidget(self.login, 2, 0)
        # # mainLayout.addWidget(self.logout, 2, 1)
        # mainLayout.addWidget(self.register, 2, 1)
        # mainLayout.addWidget(self.save, 3, 1)

        # self.setLayout(mainLayout)

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
        print("in to loginfun")
        re = Register()
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
        self.loadUsers()

    def saveUsers(self):
        print('save a user.pickle len = ',len(self.users))
        with open('data\\user.pickle', 'wb') as f:
            pickle.dump(self.users, f)

    def loadUsers(self):
        with open('data\\user.pickle', 'rb') as f:
            self.users = pickle.load(f)
        # print(self.users)

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
        # print(newvalue)
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
