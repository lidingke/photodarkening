import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from queue              import Queue


class PaintArea(QWidget):
	"""docstring for PaintArea"""
	def __init__(self):
		super(PaintArea, self).__init__()
		self.setPalette(QPalette(Qt.white))
		self.setAutoFillBackground(True)
		self.setMinimumSize(500,400)
		self.text = u'这个地方是绘图区域'
		self.show()
		self.pList = list()

	def paintEvent(self,QPaintEvent):
		print('调用paintEvent？')
		p = QPainter(self)
		if len(self.pList) > 0:
			qPointList = [QPointF(c/2,c/3) for c in self.pList]

			p.begin(self)
			#self.drawText(QPaintEvent,p)
			# p.drawPoint(1,2)
			# p.drawLine(0,0,10,20)
			# p.drawLine(90,70,10,20)
			# p.setPen(self.pen)
			# p.setBrush(self.brush)

			p.drawLines(qPointList)
			p.end()
		else:
			p.begin(self)
			self.drawText(QPaintEvent,p)
			# p.drawPoint(1,2)
			# p.drawLine(0,0,10,20)
			# p.drawLine(90,70,10,20)
			# p.setPen(self.pen)
			# p.setBrush(self.brush)

			p.end()


		# p.begin(self)

		# p.drawLine(1,2,1,200)
		# p.drawLine(9,7,100,200)
		# # p.setPen(self.pen)
		# # p.setBrush(self.brush)
		# p.end()

		#rect = QRect(50,100,300,200)
		# points = [QPoint(150,100),QPoint(300,150),QPoint(350,250),QPoint(100,300)]
		# startAngle = 30 * 16
		# spanAngle = 120 * 16

		#path = QPainterPath();
		# path.addRect(150,150,100,100)
		# path.moveTo(100,100)
		# path.cubicTo(300,100,200,200,300,300)
		# path.cubicTo(100,300,200,200,100,100)

	def drawText(self,QPaintEvent,qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setFont(QFont('微软雅黑', 20))
		qp.drawText(QPaintEvent.rect(), Qt.AlignCenter, self.text)

	def getpList(self, pList):
		self.pList = pList
		return self.pList


