from PyQt5.QtWidgets    import QWidget
from PyQt5.QtGui import (QColor, QFont, QPainter, QPalette, QPen, QBrush)
from PyQt5.QtCore import Qt

class PowerShow(QWidget):
    """docstring for PowerShow"""
    def __init__(self):
        super(PowerShow, self).__init__()
        # self.arg = arg

        self.setPalette(QPalette(QColor(239,246,250)))
        self.setAutoFillBackground(True)
        self.setGeometry(100,100,100,100)
        self.setMinimumSize(100, 100)
        # self.show()
        self.powerList = ['0W','0W','0W','0W','0W']
        self.text = '功率方差:'+self.powerList[0]+\
        '\n平均功率:'+self.powerList[1]+\
        '\n最大功率:'+self.powerList[2]+\
        '\n最小功率:'+self.powerList[3]+'\n'
        self.textshow = self.powerList[4]

    def paintEvent(self,event):
        pter = QPainter(self)
        pter.begin(self)
        pter.setPen(QPen(Qt.black,0.1))
        pter.setBrush(QBrush(QColor(125,185,222)))
        pter.drawRoundedRect(event.rect(), 10, 10)
        pter.translate(10,10)
        self.drawPowerText(event,pter)
        # pter.drawRoundedRect(20,20, 210, 160,50,50)
        pter.translate(120,10)
        self.drawPowerCurrentText(event, pter)
        pter.translate(0,-8)
        self.drawPowershishiText(event, pter)
        pter.end()

    def drawPowerText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 12))
        qp.drawText(event.rect(), Qt.RightToLeft, self.text)

    def drawPowerCurrentText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 40))
        qp.drawText(event.rect(), Qt.RightToLeft, self.textshow)

    def drawPowershishiText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 8))
        qp.drawText(event.rect(), Qt.RightToLeft, '实时：')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    addressBook = PowerShow()
    addressBook.show()

    sys.exit(app.exec_())
