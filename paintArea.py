import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PaintArea(QWidget):
	"""docstring for PaintArea"""
	def __init__(self):
		super(PaintArea, self).__init__()
		self.setPalette(QPalette(Qt.white))
		self.setAutoFillBackground(True)
		self.setMinimumSize(400,400)

	def paintEvent(self,QPaintEvent):
		p = QPainter(self)
		# p.setPen(self.pen)
		# p.setBrush(self.brush)

		rect = QRect(50,100,300,200)
		# points = [QPoint(150,100),QPoint(300,150),QPoint(350,250),QPoint(100,300)]
		# startAngle = 30 * 16
		# spanAngle = 120 * 16

		path = QPainterPath();
		# path.addRect(150,150,100,100)
		# path.moveTo(100,100)
		# path.cubicTo(300,100,200,200,300,300)
		# path.cubicTo(100,300,200,200,100,100)

