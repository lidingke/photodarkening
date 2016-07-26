from PyQt5.QtWidgets import QListWidget,QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from model.database import DataHand
import time
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
            # pdb.set_trace()
            # QListWidgetItem(x)
            xsplit = x[0].split('US')
            timetick = xsplit[0][2:]
            username = xsplit[1]
            timeShow = time.strftime('%Y:%m:%d||%H:%M:%S',
                time.localtime(int(timetick)))
            item = QListWidgetItem('时间:{}用户:{}'.format(timeShow,username))
            item.tableName = x[0]
            self.addItem(item)
        self.nowtable = table[-1][0]
        self.table = table
        # print(self.nowtable,type(self.nowtable))

    def getTableData(self):
        return self.datahand.getTableData(self.nowtable)

    def itemSelect(self):
        self.itemText = self.currentItem().tableName
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
    # print(len(data))

    sys.exit(app.exec_())
