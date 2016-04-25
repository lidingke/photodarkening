#!/usr/bin/env python
# coding=utf-8

import sys

# Library imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

# Local imports
from    view        import View
from    presenter   import Presenter
from user import User


if __name__ == '__main__':
    app         = QApplication(sys.argv)
    pt = QPalette()
    pt.setColor(QPalette.Background , QColor(239,246,250))
    # pt.setColor(QPalette.Button, QColor(239,246,250))
    pt.setColor(QPalette.ButtonText, QColor(34,39,42))
    # pt.setColor(QPalette.WindowText, QColor(34,39,42))
    pt.setColor(QPalette.Highlight, QColor(74,149,184))

    app.setPalette(pt)
    font = app.font()
    font.setPointSize(12)
    font.setFamily('微软雅黑')

    app.setFont(font)

    gui         = View()

    presenter   = Presenter(gui)
    gui.show()

    sys.exit(app.exec_())
