# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'record.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(536, 264)
        Form.setWindowTitle("")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(12, 12, 192, 106))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.timeEdit = QtWidgets.QDateTimeEdit(self.widget)
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 0, 1, 1, 1)
        self.stepEdit = QtWidgets.QSpinBox(self.widget)
        self.stepEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stepEdit.setMaximum(10000)
        self.stepEdit.setProperty("value", 60)
        self.stepEdit.setObjectName("stepEdit")
        self.gridLayout.addWidget(self.stepEdit, 1, 1, 1, 1)
        self.logButton = QtWidgets.QPushButton(self.widget)
        self.logButton.setObjectName("logButton")
        self.gridLayout.addWidget(self.logButton, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ticker = QtWidgets.QLCDNumber(self.widget)
        self.ticker.setEnabled(False)
        self.ticker.setObjectName("ticker")
        self.gridLayout.addWidget(self.ticker, 3, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(222, 10, 258, 111))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.printButton = QtWidgets.QPushButton(self.widget1)
        self.printButton.setObjectName("printButton")
        self.gridLayout_2.addWidget(self.printButton, 0, 1, 1, 1)
        self.historyEdit = QtWidgets.QPlainTextEdit(self.widget1)
        self.historyEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.historyEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.historyEdit.setObjectName("historyEdit")
        self.gridLayout_2.addWidget(self.historyEdit, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "记录时长："))
        self.stepEdit.setSuffix(_translate("Form", "秒"))
        self.logButton.setText(_translate("Form", "开始"))
        self.label_2.setText(_translate("Form", "记录步长："))
        self.label_3.setText(_translate("Form", "历史记录："))
        self.printButton.setText(_translate("Form", "打印"))

