# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(250, 150)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 189, 106))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.nameIput = QtWidgets.QLineEdit(self.widget)
        self.nameIput.setObjectName("nameIput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameIput)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.passwordIput = QtWidgets.QLineEdit(self.widget)
        self.passwordIput.setObjectName("passwordIput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordIput)
        self.login = QtWidgets.QPushButton(self.widget)
        self.login.setObjectName("login")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.login)
        self.register_2 = QtWidgets.QPushButton(self.widget)
        self.register_2.setObjectName("register_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.register_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "用户名："))
        self.label_2.setText(_translate("Form", "密码："))
        self.login.setText(_translate("Form", "登陆"))
        self.register_2.setText(_translate("Form", "注册"))

