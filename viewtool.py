from PyQt5.QtWidgets    import QWidget
from PyQt5.QtWidgets    import QGroupBox
from PyQt5.QtWidgets    import QPushButton

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor




class NQGroupBox(QGroupBox):
    """docstring for NQGroupBox"""
    def __init__(self):
        super(NQGroupBox, self).__init__()
        QGroupBox.__init__(self)
        # self.arg = arg

        pt = QPalette()
        pt.setColor(QPalette.Background , QColor(239,246,250))

        self.setPalette(pt)

        self.setStyleSheet("QGroupBox{border:None;}")


class TabWidget(QWidget):
    """docstring for TabWidget"""
    def __init__(self):
        super(TabWidget, self).__init__()
        QWidget.__init__(self)
        # self.arg = arg
        # pt = QPalette()
        # pt.setColor(QPalette.Background , QColor(239,246,250))
        # self.setPalette(pt)

class NPushButton(QPushButton):
    """docstring for NPushButton"""
    def __init__(self):
        super(NPushButton, self).__init__()
        # QPushButton.__init__(self)
        self.setStyleSheet("background-color: rgb(239,246,250);")

