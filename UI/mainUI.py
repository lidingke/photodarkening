# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(795, 642)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 641, 561))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabBox = QtWidgets.QTabWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabBox.sizePolicy().hasHeightForWidth())
        self.tabBox.setSizePolicy(sizePolicy)
        self.tabBox.setMinimumSize(QtCore.QSize(0, 180))
        self.tabBox.setObjectName("tabBox")
        self.userTab = QtWidgets.QWidget()
        self.userTab.setObjectName("userTab")
        self.layoutWidget = QtWidgets.QWidget(self.userTab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 189, 106))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.userName = QtWidgets.QLineEdit(self.layoutWidget)
        self.userName.setObjectName("userName")
        self.gridLayout.addWidget(self.userName, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordIput = QtWidgets.QLineEdit(self.layoutWidget)
        self.passwordIput.setObjectName("passwordIput")
        self.gridLayout.addWidget(self.passwordIput, 1, 1, 1, 1)
        self.login = QtWidgets.QPushButton(self.layoutWidget)
        self.login.setObjectName("login")
        self.gridLayout.addWidget(self.login, 2, 1, 1, 1)
        self.userRegister = QtWidgets.QPushButton(self.layoutWidget)
        self.userRegister.setObjectName("userRegister")
        self.gridLayout.addWidget(self.userRegister, 3, 1, 1, 1)
        self.tabBox.addTab(self.userTab, "")
        self.portTab = QtWidgets.QWidget()
        self.portTab.setObjectName("portTab")
        self.layoutWidget1 = QtWidgets.QWidget(self.portTab)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 158, 77))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openPort = QtWidgets.QPushButton(self.layoutWidget1)
        self.openPort.setObjectName("openPort")
        self.gridLayout_3.addWidget(self.openPort, 0, 0, 1, 2)
        self.closePort = QtWidgets.QPushButton(self.layoutWidget1)
        self.closePort.setObjectName("closePort")
        self.gridLayout_3.addWidget(self.closePort, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.baundrate = QtWidgets.QComboBox(self.layoutWidget1)
        self.baundrate.setObjectName("baundrate")
        self.gridLayout_3.addWidget(self.baundrate, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.port = QtWidgets.QComboBox(self.layoutWidget1)
        self.port.setObjectName("port")
        self.gridLayout_3.addWidget(self.port, 2, 1, 1, 2)
        self.tabBox.addTab(self.portTab, "")
        self.pumpTab = QtWidgets.QWidget()
        self.pumpTab.setObjectName("pumpTab")
        self.layoutWidget2 = QtWidgets.QWidget(self.pumpTab)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 10, 183, 54))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.openPlatform = QtWidgets.QPushButton(self.layoutWidget2)
        self.openPlatform.setObjectName("openPlatform")
        self.gridLayout_5.addWidget(self.openPlatform, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 1, 1, 1)
        self.currentSpin = QtWidgets.QSpinBox(self.layoutWidget2)
        self.currentSpin.setMaximum(500)
        self.currentSpin.setSingleStep(50)
        self.currentSpin.setObjectName("currentSpin")
        self.gridLayout_5.addWidget(self.currentSpin, 0, 2, 1, 1)
        self.closePlatform = QtWidgets.QPushButton(self.layoutWidget2)
        self.closePlatform.setObjectName("closePlatform")
        self.gridLayout_5.addWidget(self.closePlatform, 1, 0, 1, 1)
        self.setCurrent = QtWidgets.QPushButton(self.layoutWidget2)
        self.setCurrent.setObjectName("setCurrent")
        self.gridLayout_5.addWidget(self.setCurrent, 1, 1, 1, 2)
        self.tabBox.addTab(self.pumpTab, "")
        self.logTab = QtWidgets.QWidget()
        self.logTab.setObjectName("logTab")
        self.layoutWidget_2 = QtWidgets.QWidget(self.logTab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 218, 106))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.historyGridLayout = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.historyGridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.historyGridLayout.setObjectName("historyGridLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.historyGridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.timeEdit = QtWidgets.QDateTimeEdit(self.layoutWidget_2)
        self.timeEdit.setObjectName("timeEdit")
        self.historyGridLayout.addWidget(self.timeEdit, 0, 1, 1, 1)
        self.stepEdit = QtWidgets.QSpinBox(self.layoutWidget_2)
        self.stepEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stepEdit.setMaximum(10000)
        self.stepEdit.setProperty("value", 60)
        self.stepEdit.setObjectName("stepEdit")
        self.historyGridLayout.addWidget(self.stepEdit, 1, 1, 1, 1)
        self.logButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.logButton.setObjectName("logButton")
        self.historyGridLayout.addWidget(self.logButton, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.historyGridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.ticker = QtWidgets.QLCDNumber(self.layoutWidget_2)
        self.ticker.setEnabled(False)
        self.ticker.setObjectName("ticker")
        self.historyGridLayout.addWidget(self.ticker, 3, 1, 1, 1)
        self.layoutWidget_3 = QtWidgets.QWidget(self.logTab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(230, 10, 371, 223))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.logGridLayout = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.logGridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.logGridLayout.setObjectName("logGridLayout")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.logGridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.printButton = QtWidgets.QPushButton(self.layoutWidget_3)
        self.printButton.setObjectName("printButton")
        self.logGridLayout.addWidget(self.printButton, 0, 1, 1, 1)
        self.historyEdit = QtWidgets.QPlainTextEdit(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.historyEdit.sizePolicy().hasHeightForWidth())
        self.historyEdit.setSizePolicy(sizePolicy)
        self.historyEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.historyEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.historyEdit.setObjectName("historyEdit")
        self.logGridLayout.addWidget(self.historyEdit, 1, 0, 1, 2)
        self.tabBox.addTab(self.logTab, "")
        self.helpTab = QtWidgets.QWidget()
        self.helpTab.setObjectName("helpTab")
        self.tabBox.addTab(self.helpTab, "")
        self.verticalLayout_2.addWidget(self.tabBox)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(-1, -1, 0, -1)
        self.mainLayout.setObjectName("mainLayout")
        self.cmdLayout = QtWidgets.QVBoxLayout()
        self.cmdLayout.setObjectName("cmdLayout")
        self.canvas2 = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.canvas2.setObjectName("canvas2")
        self.cmdLayout.addWidget(self.canvas2)
        self.mainLayout.addLayout(self.cmdLayout)
        self.matplot = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.matplot.setMinimumSize(QtCore.QSize(500, 100))
        self.matplot.setObjectName("matplot")
        self.tabBox.raise_()
        self.mainLayout.addWidget(self.matplot)
        self.verticalLayout_2.addLayout(self.mainLayout)

        self.retranslateUi(Form)
        self.tabBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "用户名："))
        self.label_2.setText(_translate("Form", "密码："))
        self.login.setText(_translate("Form", "登录"))
        self.userRegister.setText(_translate("Form", "注册"))
        self.tabBox.setTabText(self.tabBox.indexOf(self.userTab), _translate("Form", "用户登录"))
        self.openPort.setText(_translate("Form", "打开串口"))
        self.closePort.setText(_translate("Form", "关闭串口"))
        self.label_5.setText(_translate("Form", "波特率："))
        self.label_6.setText(_translate("Form", "串口号："))
        self.tabBox.setTabText(self.tabBox.indexOf(self.portTab), _translate("Form", "串口设置"))
        self.openPlatform.setText(_translate("Form", "打开平台"))
        self.label_7.setText(_translate("Form", "电流："))
        self.currentSpin.setSuffix(_translate("Form", "mA"))
        self.closePlatform.setText(_translate("Form", "关闭平台"))
        self.setCurrent.setText(_translate("Form", "设置"))
        self.tabBox.setTabText(self.tabBox.indexOf(self.pumpTab), _translate("Form", "泵浦开关"))
        self.label_3.setText(_translate("Form", "记录时长："))
        self.stepEdit.setSuffix(_translate("Form", "秒"))
        self.logButton.setText(_translate("Form", "开始"))
        self.label_8.setText(_translate("Form", "记录步长："))
        self.label_9.setText(_translate("Form", "历史记录："))
        self.printButton.setText(_translate("Form", "打印"))
        self.tabBox.setTabText(self.tabBox.indexOf(self.logTab), _translate("Form", "功率计"))
        self.tabBox.setTabText(self.tabBox.indexOf(self.helpTab), _translate("Form", "帮助"))

