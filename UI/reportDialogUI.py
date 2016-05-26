# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(409, 121)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 406, 118))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditProducer = QtWidgets.QLineEdit(self.widget)
        self.lineEditProducer.setObjectName("lineEditProducer")
        self.gridLayout.addWidget(self.lineEditProducer, 3, 1, 1, 1)
        self.labelFiberNo = QtWidgets.QLabel(self.widget)
        self.labelFiberNo.setObjectName("labelFiberNo")
        self.gridLayout.addWidget(self.labelFiberNo, 3, 2, 1, 1)
        self.lineEditFiberlength = QtWidgets.QLineEdit(self.widget)
        self.lineEditFiberlength.setObjectName("lineEditFiberlength")
        self.gridLayout.addWidget(self.lineEditFiberlength, 2, 3, 1, 1)
        self.labelFiberlength = QtWidgets.QLabel(self.widget)
        self.labelFiberlength.setObjectName("labelFiberlength")
        self.gridLayout.addWidget(self.labelFiberlength, 2, 2, 1, 1)
        self.labelProducer = QtWidgets.QLabel(self.widget)
        self.labelProducer.setObjectName("labelProducer")
        self.gridLayout.addWidget(self.labelProducer, 3, 0, 1, 1)
        self.lineEditFiberNo = QtWidgets.QLineEdit(self.widget)
        self.lineEditFiberNo.setObjectName("lineEditFiberNo")
        self.gridLayout.addWidget(self.lineEditFiberNo, 3, 3, 1, 1)
        self.labelWorker = QtWidgets.QLabel(self.widget)
        self.labelWorker.setObjectName("labelWorker")
        self.gridLayout.addWidget(self.labelWorker, 1, 0, 1, 1)
        self.lineEditWorker = QtWidgets.QLineEdit(self.widget)
        self.lineEditWorker.setObjectName("lineEditWorker")
        self.gridLayout.addWidget(self.lineEditWorker, 1, 1, 1, 1)
        self.labelHumidity = QtWidgets.QLabel(self.widget)
        self.labelHumidity.setObjectName("labelHumidity")
        self.gridLayout.addWidget(self.labelHumidity, 1, 2, 1, 1)
        self.lineEditDate = QtWidgets.QLineEdit(self.widget)
        self.lineEditDate.setObjectName("lineEditDate")
        self.gridLayout.addWidget(self.lineEditDate, 0, 1, 1, 1)
        self.lineEditTemperature = QtWidgets.QLineEdit(self.widget)
        self.lineEditTemperature.setObjectName("lineEditTemperature")
        self.gridLayout.addWidget(self.lineEditTemperature, 0, 3, 1, 1)
        self.lineEditHumidity = QtWidgets.QLineEdit(self.widget)
        self.lineEditHumidity.setObjectName("lineEditHumidity")
        self.gridLayout.addWidget(self.lineEditHumidity, 1, 3, 1, 1)
        self.labelFibertype = QtWidgets.QLabel(self.widget)
        self.labelFibertype.setObjectName("labelFibertype")
        self.gridLayout.addWidget(self.labelFibertype, 2, 0, 1, 1)
        self.lineEditFibertype = QtWidgets.QLineEdit(self.widget)
        self.lineEditFibertype.setObjectName("lineEditFibertype")
        self.gridLayout.addWidget(self.lineEditFibertype, 2, 1, 1, 1)
        self.labelTemperature = QtWidgets.QLabel(self.widget)
        self.labelTemperature.setObjectName("labelTemperature")
        self.gridLayout.addWidget(self.labelTemperature, 0, 2, 1, 1)
        self.labelDate = QtWidgets.QLabel(self.widget)
        self.labelDate.setObjectName("labelDate")
        self.gridLayout.addWidget(self.labelDate, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelFiberNo.setText(_translate("Dialog", "光纤编号："))
        self.labelFiberlength.setText(_translate("Dialog", "光纤长度："))
        self.labelProducer.setText(_translate("Dialog", "生产厂家："))
        self.labelWorker.setText(_translate("Dialog", "操作人："))
        self.labelHumidity.setText(_translate("Dialog", "环境湿度："))
        self.labelFibertype.setText(_translate("Dialog", "光纤型号："))
        self.labelTemperature.setText(_translate("Dialog", "环境温度："))
        self.labelDate.setText(_translate("Dialog", "日期："))

