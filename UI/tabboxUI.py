# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabbox.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(675, 590)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 641, 561))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget_2)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 180))
        self.tabWidget.setObjectName("tabWidget")
        self.userTab = QtWidgets.QWidget()
        self.userTab.setObjectName("userTab")
        self.layoutWidget = QtWidgets.QWidget(self.userTab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 189, 106))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
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
        self.tabWidget.addTab(self.userTab, "")
        self.portTab = QtWidgets.QWidget()
        self.portTab.setObjectName("portTab")
        self.layoutWidget1 = QtWidgets.QWidget(self.portTab)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 158, 77))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openportPump = QtWidgets.QPushButton(self.layoutWidget1)
        self.openportPump.setObjectName("openportPump")
        self.gridLayout_3.addWidget(self.openportPump, 0, 0, 1, 2)
        self.closeportPump = QtWidgets.QPushButton(self.layoutWidget1)
        self.closeportPump.setObjectName("closeportPump")
        self.gridLayout_3.addWidget(self.closeportPump, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.baundratePump = QtWidgets.QComboBox(self.layoutWidget1)
        self.baundratePump.setObjectName("baundratePump")
        self.gridLayout_3.addWidget(self.baundratePump, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.portPump = QtWidgets.QComboBox(self.layoutWidget1)
        self.portPump.setObjectName("portPump")
        self.gridLayout_3.addWidget(self.portPump, 2, 1, 1, 2)
        self.tabWidget.addTab(self.portTab, "")
        self.pumpTab = QtWidgets.QWidget()
        self.pumpTab.setObjectName("pumpTab")
        self.layoutWidget2 = QtWidgets.QWidget(self.pumpTab)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 10, 183, 54))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.sourceOpen = QtWidgets.QPushButton(self.layoutWidget2)
        self.sourceOpen.setObjectName("sourceOpen")
        self.gridLayout_5.addWidget(self.sourceOpen, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 1, 1, 1)
        self.firstpumpSpin = QtWidgets.QSpinBox(self.layoutWidget2)
        self.firstpumpSpin.setMaximum(500)
        self.firstpumpSpin.setSingleStep(50)
        self.firstpumpSpin.setObjectName("firstpumpSpin")
        self.gridLayout_5.addWidget(self.firstpumpSpin, 0, 2, 1, 1)
        self.sourceClose = QtWidgets.QPushButton(self.layoutWidget2)
        self.sourceClose.setObjectName("sourceClose")
        self.gridLayout_5.addWidget(self.sourceClose, 1, 0, 1, 1)
        self.firstPumpSet = QtWidgets.QPushButton(self.layoutWidget2)
        self.firstPumpSet.setObjectName("firstPumpSet")
        self.gridLayout_5.addWidget(self.firstPumpSet, 1, 1, 1, 2)
        self.tabWidget.addTab(self.pumpTab, "")
        self.helpTab = QtWidgets.QWidget()
        self.helpTab.setObjectName("helpTab")
        self.layoutWidget_2 = QtWidgets.QWidget(self.helpTab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 192, 106))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.historyGridLayout = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.historyGridLayout.setContentsMargins(0, 0, 0, 0)
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
        self.layoutWidget_3 = QtWidgets.QWidget(self.helpTab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(220, 10, 258, 111))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.logGridLayout = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.logGridLayout.setContentsMargins(0, 0, 0, 0)
        self.logGridLayout.setObjectName("logGridLayout")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.logGridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.printButton = QtWidgets.QPushButton(self.layoutWidget_3)
        self.printButton.setObjectName("printButton")
        self.logGridLayout.addWidget(self.printButton, 0, 1, 1, 1)
        self.historyEdit = QtWidgets.QPlainTextEdit(self.layoutWidget_3)
        self.historyEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.historyEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.historyEdit.setObjectName("historyEdit")
        self.logGridLayout.addWidget(self.historyEdit, 1, 0, 1, 2)
        self.tabWidget.addTab(self.helpTab, "")
        self.powerTab = QtWidgets.QWidget()
        self.powerTab.setObjectName("powerTab")
        self.tabWidget.addTab(self.powerTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.cmdLayout = QtWidgets.QVBoxLayout()
        self.cmdLayout.setObjectName("cmdLayout")
        self.canvas = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.canvas.setMinimumSize(QtCore.QSize(0, 0))
        self.canvas.setObjectName("canvas")
        self.cmdLayout.addWidget(self.canvas)
        self.mainLayout.addLayout(self.cmdLayout)
        self.matplot = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.matplot.setMinimumSize(QtCore.QSize(500, 100))
        self.matplot.setObjectName("matplot")
        self.mainLayout.addWidget(self.matplot)
        self.verticalLayout_2.addLayout(self.mainLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "用户名："))
        self.label_2.setText(_translate("Form", "密码："))
        self.login.setText(_translate("Form", "登录"))
        self.userRegister.setText(_translate("Form", "注册"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.userTab), _translate("Form", "用户登录"))
        self.openportPump.setText(_translate("Form", "打开串口"))
        self.closeportPump.setText(_translate("Form", "关闭串口"))
        self.label_5.setText(_translate("Form", "波特率："))
        self.label_6.setText(_translate("Form", "串口号："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.portTab), _translate("Form", "串口设置"))
        self.sourceOpen.setText(_translate("Form", "打开平台"))
        self.label_7.setText(_translate("Form", "电流："))
        self.firstpumpSpin.setSuffix(_translate("Form", "mA"))
        self.sourceClose.setText(_translate("Form", "关闭平台"))
        self.firstPumpSet.setText(_translate("Form", "设置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pumpTab), _translate("Form", "泵浦开关"))
        self.label_3.setText(_translate("Form", "记录时长："))
        self.stepEdit.setSuffix(_translate("Form", "秒"))
        self.logButton.setText(_translate("Form", "开始"))
        self.label_8.setText(_translate("Form", "记录步长："))
        self.label_9.setText(_translate("Form", "历史记录："))
        self.printButton.setText(_translate("Form", "打印"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.helpTab), _translate("Form", "功率计"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.powerTab), _translate("Form", "帮助"))

