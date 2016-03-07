import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets    import QVBoxLayout
from PyQt5.QtWidgets    import QHBoxLayout
from PyQt5.QtWidgets    import QLineEdit
from PyQt5.QtGui       import QPaintEvent
from PyQt5.QtGui       import QPixmap

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
mainBox = QVBoxLayout()
vboxMenu = QHBoxLayout()
vboxSet = QHBoxLayout()
vboxShow = QHBoxLayout()
edit1 = QLineEdit()
edit2 = QLineEdit()
edit3 = QLineEdit()
edit4 = QLineEdit()
widget2 = QtWidgets.QWidget()
#painter=QPaintEvent(widget2)

#edit6 = QPainter()
#vboxMenu.addWidget(painter)
vboxMenu.addWidget(edit2)
vboxSet.addWidget(edit3)
#vboxShow.addWidget(edit5)
mainBox.addLayout(vboxMenu)
mainBox.addLayout(vboxSet)
mainBox.addLayout(vboxShow)
widget.setLayout(mainBox)


widget.resize(360, 360)
widget.setWindowTitle("Hello, PyQt5!")
widget.show()
sys.exit(app.exec_())
