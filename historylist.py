from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import pyqtSignal
from database import DataHand
import pdb
# from toolkit import WRpickle

class HistoryList(QListWidget):
    """docstring for HistoryList"""
    itemSelectedEmit = pyqtSignal(object)

    def __init__(self,):
        super(HistoryList, self).__init__()
        self.datahand = DataHand()
        self.nowtable = 0
        self.itemSelectionChanged.connect(self.itemSelect)
        self.table = []
        self.setCurrentRow(1)
        self.getTable()

    def getTable(self):
        table = self.datahand.getTable()
        # table.append(('last',))
        for x in table[::-1]:
            self.addItem(x[0])
        self.nowtable = table[-1][0]
        self.table = table
        # print(self.nowtable,type(self.nowtable))

    def getTableData(self):
        return self.datahand.getTableData(self.nowtable)

    def itemSelect(self):
        self.itemText = self.currentItem().text()
        self.itemIndex = self.table[-1-int(self.currentRow())][0]
        print(self.itemText,self.itemIndex)
        self.itemSelectedEmit.emit(self.itemIndex)


if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    ad = HistoryList()
    ad.show()
    ad.getTable()
    data = ad.getTableData()
    print(len(data))

    sys.exit(app.exec_())
