# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'portGB.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName("GroupBox")
        GroupBox.resize(627, 240)
        GroupBox.setTitle("")
        self.widget = QtWidgets.QWidget(GroupBox)
        self.widget.setGeometry(QtCore.QRect(0, 0, 402, 99))
        self.widget.setObjectName("widget")
        self.formLayout_3 = QtWidgets.QFormLayout(self.widget)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.openportSource = QtWidgets.QPushButton(self.widget)
        self.openportSource.setObjectName("openportSource")
        self.gridLayout.addWidget(self.openportSource, 0, 0, 1, 2)
        self.closeportSource = QtWidgets.QPushButton(self.widget)
        self.closeportSource.setObjectName("closeportSource")
        self.gridLayout.addWidget(self.closeportSource, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.baundrateSource = QtWidgets.QComboBox(self.widget)
        self.baundrateSource.setObjectName("baundrateSource")
        self.gridLayout.addWidget(self.baundrateSource, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.portSource = QtWidgets.QLineEdit(self.widget)
        self.portSource.setObjectName("portSource")
        self.gridLayout.addWidget(self.portSource, 2, 1, 1, 2)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.gridLayout)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openportPump = QtWidgets.QPushButton(self.widget)
        self.openportPump.setObjectName("openportPump")
        self.gridLayout_3.addWidget(self.openportPump, 0, 0, 1, 2)
        self.closeportPump = QtWidgets.QPushButton(self.widget)
        self.closeportPump.setObjectName("closeportPump")
        self.gridLayout_3.addWidget(self.closeportPump, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.baundratePump = QtWidgets.QComboBox(self.widget)
        self.baundratePump.setObjectName("baundratePump")
        self.gridLayout_3.addWidget(self.baundratePump, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.portPump = QtWidgets.QLineEdit(self.widget)
        self.portPump.setObjectName("portPump")
        self.gridLayout_3.addWidget(self.portPump, 2, 1, 1, 2)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.gridLayout_3)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.formLayout_2)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        self.label_3.setText(_translate("GroupBox", "种子源"))
        self.openportSource.setText(_translate("GroupBox", "打开串口"))
        self.closeportSource.setText(_translate("GroupBox", "关闭串口"))
        self.label.setText(_translate("GroupBox", "波特率："))
        self.label_2.setText(_translate("GroupBox", "串口号："))
        self.label_4.setText(_translate("GroupBox", "泵浦源"))
        self.openportPump.setText(_translate("GroupBox", "打开串口"))
        self.closeportPump.setText(_translate("GroupBox", "关闭串口"))
        self.label_5.setText(_translate("GroupBox", "波特率："))
        self.label_6.setText(_translate("GroupBox", "串口号："))
