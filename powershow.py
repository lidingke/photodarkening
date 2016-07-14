from PyQt5.QtWidgets    import QWidget
from PyQt5.QtGui import (QColor, QFont, QPainter, QPalette, QPen, QBrush)
from PyQt5.QtCore import Qt

class PowerShow(QWidget):
    """docstring for PowerShow"""
    def __init__(self,):
        super(PowerShow, self).__init__()
        self.setPalette(QPalette(QColor(239,246,250)))
        self.setAutoFillBackground(True)
        self.setGeometry(100,100,100,100)
        self.setMinimumSize(100, 100)
        self.pter = QPainter()
        self.powerList = {'logNumber':0,
            'currentPower':0,
            'averagePower':0,
            'variancePower':0,
            'maxPower':0,
            'minPower':0}

    def paintEvent(self,event):
        pter = self.pter
        self.text = '最大功率:'+self.__Power2str(self.powerList['maxPower'])+'\n\
最小功率:'+self.__Power2str(self.powerList['minPower'])+'\n\
平均功率:'+self.__Power2str(self.powerList['averagePower'])+'\n\
功率方差:'+str(round(self.powerList['variancePower'],2))+'\n'
        self.textshow = self.__Power2str(self.powerList['currentPower'])
        pter.begin(self)
        # print('PowerShowlist',self.text ,'\n',self.textshow)
        pter.setPen(QPen(Qt.black,0.1))
        pter.setBrush(QBrush(QColor(125,185,222)))
        pter.drawRoundedRect(event.rect(), 10, 10)
        pter.translate(10,10)
        self.drawPowerText(event,pter)
        # pter.drawRoundedRect(20,20, 210, 160,50,50)
        pter.translate(130,2)
        self.drawPowershishiText(event, pter)
        pter.translate(-5,20)
        self.drawPowerCurrentText(event, pter)
        pter.end()

    def drawPowerText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 10))
        qp.drawText(event.rect(), Qt.RightToLeft, self.text)

    def drawPowerCurrentText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 25))
        qp.drawText(event.rect(), Qt.RightToLeft, self.textshow)

    def drawPowershishiText(self,event,qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('微软雅黑', 8))
        qp.drawText(event.rect(), Qt.RightToLeft, '实时：')

    def updateFigure(self):
        self.update()

    def __Power2str(self,data):
        if data > 0.1:
            return str(round(data,2))+'W'
        else:
            return str(round(data*1000,2)) + 'mW'


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    addressBook = PowerShow()
    addressBook.show()

    sys.exit(app.exec_())
