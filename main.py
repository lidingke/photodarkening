# coding=utf-8


import sys
# sys.path.append("..")
import pdb
# Library imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QCoreApplication

# Local imports
from    view.view        import View
from    presenter   import Presenter



if __name__ == '__main__':

    # QCoreApplication.setLibraryPaths(['C:\\Users\\lidingke\\Envs\\py34qt5\\Lib\\site-packages\\PyQt5\\plugins'])

    QCoreApplication.setLibraryPaths(['./plugins'])
    # pdb.set_trace()


    app         = QApplication(sys.argv)
    pt = QPalette()
    pt.setColor(QPalette.Background , QColor(239,246,250))
    # pt.setColor(QPalette.Button, QColor(239,246,250))
    pt.setColor(QPalette.ButtonText, QColor(34,39,42))
    # pt.setColor(QPalette.WindowText, QColor(34,39,42))
    # pt.setColor(QPalette.Hghlight, QColor(74,149,184))

    app.setPalette(pt)
    font = app.font()
    font.setPointSize(10)
    font.setFamily('微软雅黑')

    app.setFont(font)

    gui         = View()

    presenter   = Presenter(gui)
    gui.show()

    sys.exit(app.exec_())
