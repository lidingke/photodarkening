# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regesterview.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(435, 262)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.username = QtWidgets.QLineEdit(Dialog)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordagain = QtWidgets.QLineEdit(Dialog)
        self.passwordagain.setObjectName("passwordagain")
        self.gridLayout.addWidget(self.passwordagain, 2, 1, 1, 1)
        self.save = QtWidgets.QPushButton(Dialog)
        self.save.setObjectName("save")
        self.gridLayout.addWidget(self.save, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)
        self.level = QtWidgets.QComboBox(Dialog)
        self.level.setCurrentText("")
        self.level.setObjectName("level")
        self.gridLayout.addWidget(self.level, 3, 1, 1, 1)
        self.msgtext = QtWidgets.QLabel(Dialog)
        self.msgtext.setObjectName("msgtext")
        self.gridLayout.addWidget(self.msgtext, 4, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.level.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "user name:"))
        self.label_2.setText(_translate("Dialog", "password:"))
        self.save.setText(_translate("Dialog", "Save"))
        self.label_4.setText(_translate("Dialog", "level:"))
        self.label_3.setText(_translate("Dialog", "password again:"))
        self.msgtext.setText(_translate("Dialog", "TextLabel"))

