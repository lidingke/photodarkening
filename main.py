#!/usr/bin/env python
# coding=utf-8

# From https://github.com/lidingke/photodarkening
#  * branch            master     -> FETCH_HEAD
# Auto-merging view/view.py
# CONFLICT (content): Merge conflict in view/view.py
# Auto-merging view/user.py
# Auto-merging view/reportDialog.py
# Auto-merging view/powerrecord.py
# Auto-merging view/pdfcreater.py
# Auto-merging view/historylist.py
# Auto-merging presenter.py
# CONFLICT (content): Merge conflict in presenter.py
# Auto-merging model/toolkit.py
# Auto-merging model/singleton.py
# Auto-merging model/modelsource.py
# Auto-merging model/modelpump.py
# CONFLICT (content): Merge conflict in model/modelpump.py
# Auto-merging model/lastlog.py
# Automatic merge failed; fix conflicts and then commit the result.


import sys
sys.path.append("..")
# Library imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

# Local imports
from    view.view        import View
from    presenter   import Presenter



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
    font.setPointSize(10)
    font.setFamily('微软雅黑')

    app.setFont(font)

    gui         = View()

    presenter   = Presenter(gui)
    gui.show()

    sys.exit(app.exec_())
