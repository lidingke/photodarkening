import sys
from PyQt5.QtGui import QPagedPaintDevice, QPdfWriter, QTextDocument
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
# from PyQt5.QtPrintSupport import QPrinter
import pdb
import re
from model.database import DataHand
#todo
#refactoring need to change PickContext's gethtml method
#by using jinja2 and print method need to use weasyprint
from model.singleton import PickContext

class PdfCreater(object):
    """docstring for PdfCreater"""
    def __init__(self,parentWidget,context = {}):
        super(PdfCreater, self).__init__()
        self.parent = parentWidget
        self.powerstable = '12'
        # self.htmlGet()
        self.dbdata = None
        # self.pcontext = PdfContext(parentWidget.pickContext)
        self.pcontext = PickContext()
        # print(parentWidget.pickContext)
        # self.thtml =
        self.fileName = 'test.pdf'
        self.datahand = DataHand()

        # self.pickContext


    # def run(self):
    #     # print(self.thtml[-100:])
    #     self.savePdf()
    def getDBData(self,name):
        # self.sqlName = name
        self.dbdata = self.datahand.getTableData(name)

    def savePdf(self,fileName):
        pt = QPdfWriter(fileName)
        # pt.logicalDpiX
        pt.setPageSize(QPagedPaintDevice.A4)
        # print('resolution',pt.resolution())
        pt.setResolution(10000)
        # print('resolution',pt.resolution())

        textDocument = QTextDocument()
        textDocument.setHtml(self.pcontext.thtmlGet())
        textDocument.print_(pt)
        textDocument.end()
        print('pdf creat = ',fileName)

    def saveCsv(self, fileName):
        if self.dbdata is None:
            dt = self.datahand.getTable()
            if dt:
                self.dbdata = self.datahand.getTableData(''.join(dt[-1]))
        # xlsContain = tuple(self.dbdata)
        # XlsWrite(fileName,'Sheet1', xlsContain).runSave()
        with open(fileName,'w') as f:
            CsvWrite(f,self.dbdata).runSave()

    def saveXls(self, fileName):
        if self.dbdata is None:
            dt = self.datahand.getTable()
            if dt:
                self.dbdata = self.datahand.getTableData(''.join(dt[-1]))
        xlsContain = self.pcontext.xlsContainGet() + tuple(self.dbdata)
        XlsWrite(fileName,'Sheet1', xlsContain).runSave()

    def saveTxt(self, fileName):
        txtContext = self.pcontext.txtGet()
        if self.dbdata is None:
            dt = self.datahand.getTable()
            if dt:
                self.dbdata = self.datahand.getTableData(''.join(dt[-1]))
        with open(fileName,'wb') as f:
            for x in self.dbdata:
                print(x,x[0],x[1])
                txtContext = txtContext +'\r\n' + str(x[0])+','+str(x[1])
            txtContext = bytes(txtContext, encoding='utf-8')
            f.write(txtContext)

    def saveHtml(self,fileName):
        context = self.pcontext.thtmlGet()
        with open(fileName,'w') as f:
            f.write(context)

        # with open(fileName,'w+') as f:

        #     for x in :
        #         f.writeline(x[0],',',x[1])

    def saveFile(self, fileName):
        self.saveTxt(fileName)

    def saveToFile(self):
        fileName, fileform = QFileDialog.getSaveFileName(self.parent, "Save Report",
                '', " (*.pdf);;(*.csv);;(*.xls);;(*.txt);;(*.html);;All Files (*)")
        print('fileform',fileform)
        # pdb.set_trace()
        if not (fileName and fileform):
            return
        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QMessageBox.information(self.parent, "无法打开文件",
                    "在打开文件 \"%s\" 时出错，新文件未生成" % fileName)
            return
        out_file.close()
        # self.thtml = PdfContext(parentWidget.pickContext).thtmlGet()
        self.fileName = fileName
        if fileform:
            try:
                fileform = re.findall('\(*\.(.*?)\)', fileform)[-1]
            except IndexError:
                fileform = str(fileform)
            print('fileform,',fileform)
            if fileform == 'pdf':
                self.savePdf(fileName)
            elif fileform == 'csv':
                self.saveCsv(fileName)
            elif fileform == 'xls':
                self.saveXls(fileName)
            elif fileform == 'txt':
                self.saveTxt(fileName)
            elif fileform == 'html':
                self.saveHtml(fileName)
            else:
               self.saveFile(fileName)


        print(fileName)
        # pickle.dump(self.contacts, out_file)

import xlwt
class XlsWrite(object):
        """docstring for XlsWrite"""
        def __init__(self, fileName = 'test.xls', sheetName = 'Sheet1', xlsContain = (())):
                super(XlsWrite, self).__init__()
                self.fileName = fileName
                self.sheetName = sheetName
                self.workbook = xlwt.Workbook(encoding= 'utf-8')
                self.booksheet = self.workbook.add_sheet(self.sheetName, cell_overwrite_ok= True)
                self.xlsContain = xlsContain

        def runSave(self):
                # workbook.add_sheet('Sheet2')
                for i,row in enumerate(self.xlsContain):
                        for j,col in enumerate(row):
                                self.booksheet.write(i, j, col)
                self.workbook.save(self.fileName)

import csv
class CsvWrite(object):
    """docstring for CsvWrite"""
    def __init__(self, fileobj, row = list()):
        super(CsvWrite, self).__init__()
        self.row = row
        self.writer = csv.writer(fileobj)

    def runSave(self):
        for x in self.row:
            # print(x)
            self.writer.writerow(list(x[:2]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # PdfCreater().saveTxt('fileName.txt')
    app.exec_()
