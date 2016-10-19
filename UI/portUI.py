# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'port.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(381, 129)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 171, 111))
        self.groupBox.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(5, 11, 158, 77))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.openportSource = QtWidgets.QPushButton(self.layoutWidget)
        self.openportSource.setObjectName("openportSource")
        self.gridLayout.addWidget(self.openportSource, 0, 0, 1, 2)
        self.closeportSource = QtWidgets.QPushButton(self.layoutWidget)
        self.closeportSource.setObjectName("closeportSource")
        self.gridLayout.addWidget(self.closeportSource, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.baundrateSource = QtWidgets.QComboBox(self.layoutWidget)
        self.baundrateSource.setObjectName("baundrateSource")
        self.gridLayout.addWidget(self.baundrateSource, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.portSource = QtWidgets.QLineEdit(self.layoutWidget)
        self.portSource.setObjectName("portSource")
        self.gridLayout.addWidget(self.portSource, 2, 1, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(190, 10, 171, 111))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(5, 11, 158, 77))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openportPump = QtWidgets.QPushButton(self.layoutWidget_2)
        self.openportPump.setObjectName("openportPump")
        self.gridLayout_3.addWidget(self.openportPump, 0, 0, 1, 2)
        self.closeportPump = QtWidgets.QPushButton(self.layoutWidget_2)
        self.closeportPump.setObjectName("closeportPump")
        self.gridLayout_3.addWidget(self.closeportPump, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.baundratePump = QtWidgets.QComboBox(self.layoutWidget_2)
        self.baundratePump.setObjectName("baundratePump")
        self.gridLayout_3.addWidget(self.baundratePump, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.portPump = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.portPump.setObjectName("portPump")
        self.gridLayout_3.addWidget(self.portPump, 2, 1, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "种子源"))
        self.openportSource.setText(_translate("Form", "打开串口"))
        self.closeportSource.setText(_translate("Form", "关闭串口"))
        self.label.setText(_translate("Form", "波特率："))
        self.label_2.setText(_translate("Form", "串口号："))
        self.groupBox_2.setTitle(_translate("Form", "泵浦源"))
        self.openportPump.setText(_translate("Form", "打开串口"))
        self.closeportPump.setText(_translate("Form", "关闭串口"))
        self.label_5.setText(_translate("Form", "波特率："))
        self.label_6.setText(_translate("Form", "串口号："))

