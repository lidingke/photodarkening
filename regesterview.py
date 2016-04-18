# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regesterview.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import (QLabel,QLineEdit, QGridLayout, QComboBox, QPushButton)
from PyQt5.QtCore       import QMetaObject,QCoreApplication
from PyQt5.QtWidgets import QApplication,QDialog
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(435, 262)
        self.gridLayout_2 =  QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("Dialog")
        self.gridLayout =  QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label =  QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit =  QLineEdit(Dialog)
        self.lineEdit.setObjectName("username")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 =  QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 =  QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("password")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_3 =  QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_3 =  QLineEdit(Dialog)
        self.lineEdit_3.setObjectName("passwordagain")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.label_4 =  QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.comboBox =  QComboBox(Dialog)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("level")
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.save =  QPushButton(Dialog)
        self.save.setObjectName("save")
        self.gridLayout.addWidget(self.save, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.comboBox.setCurrentIndex(-1)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "user name:"))
        self.label_2.setText(_translate("Dialog", "password:"))
        self.label_3.setText(_translate("Dialog", "password again:"))
        self.label_4.setText(_translate("Dialog", "level:"))
        self.save.setText(_translate("Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app =  QApplication(sys.argv)
    Dialog =  QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

