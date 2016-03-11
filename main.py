#!/usr/bin/env python
# coding=utf-8

import sys

# Library imports
from PyQt5.QtWidgets import QApplication

# Local imports
from    view        import View
from    presenter   import Presenter


if __name__ == '__main__':
    app         = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(16)
    font.setFamily('微软雅黑')
    app.setFont(font)
    gui         = View()
    presenter   = Presenter(gui)

    gui.show()
    sys.exit(app.exec_())
