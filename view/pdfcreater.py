import sys

from PyQt5.QtGui import QPagedPaintDevice, QPdfWriter, QTextDocument
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

# from PyQt5.QtPrintSupport import QPrinter
import re
from model.database import DataHand
from frame.singleton import PickContext

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

# class PdfContext(object):
#     """docstring for PdfContext"""
#     def __init__(self,pickContext = None):
#       super(PdfContext, self).__init__()
#       if pickContext:
#         self.pickContext = pickContext
#       else:
#         self.pickContext = {
#         'title': '掺镱光纤光子暗化测试报告',
#         'date': '2016/03/16 11:30',
#         'worker': 'XXX',
#         'fibertype': '10/130 DC-YDF',
#         'producer': 'YOFC',
#         'fiberNo': 'XXXXXXXX',

#         'title1st': '测试条件',
#         'temperature': '25℃',
#         'humidity': '30%',
#         'signalwavelength': '1064nm',
#         'signalpulsewidth': '26ns',
#         'signalpulsewidth': '100kHz',
#         'secondpulsepower': '6.20W',
#         'fiberlength': '4.5m',
#         'timelong': '10hr',

#         'title2st': '测试结果',
#         'maxsignalpower': '2.74W',
#         'minsingalpower': '2.68W',
#         'averagesingalepower': '2.71W',
#         'powerstable': '±1.1%',
#         'imgsrc':'plot.pdf'
#         }





#     def getContext(self):
#       return self.pickContext

#     def inputContext(self,context):
#       self.pickContext = context

#     def txtGet(self):
#       text = self.pickContext
#       title = text.get('title','')
#       date = text.get('date','')
#       worker = text.get('worker','')
#       # print(worker)
#       fibertype = text.get('fibertype','')
#       producer = text.get('producer','')
#       fiberNo = text.get('fiberNo','')
#       title1st = text.get('title1st','')
#       temperature = text.get('temperature','')
#       humidity = text.get('humidity','')
#       signalwavelength = text.get('signalwavelength','')
#       signalpulsewidth = text.get('signalpulsewidth','')
#       signalfrequence = text.get('signalfrequence','')
#       secondpulsepower = text.get('secondpulsepower','')
#       fiberlength = text.get('fiberlength','')
#       timelong = str(int(text.get('timelong','')))

#       title2st = text.get('title2st','')
#       maxsignalpower = self.__Power2str(text.get('maxsignalpower',''))
#       minsingalpower = self.__Power2str(text.get('minsingalpower',''))
#       averagesingalepower = self.__Power2str(text.get('averagesingalepower',''))
#       powerstable = self.__Power2str(text.get('powerstable',''))
#       txtContext = '''
#     {}
#     日期：{}\r\n
#     操作人：{}\r\n
#     光纤型号：{}\r\n
#     生产厂家：{}\r\n
#     光纤编号：{}
#     {}\r\n
#     环境温度：{}\r\n
#     环境湿度：{}\r\n
#     信号光波长：{}\r\n
#     信号光脉宽：{}\r\n
#     信号光频率：{}\r\n
#     二级泵浦光功率: {}\r\n
#     光纤长度：{}\r\n
#     测试时长：{}
#     {}\r\n
#     信号光功率最大值：{}\r\n
#     信号光功率最小值：{}\r\n
#     信号光功率平均值：{}\r\n
#     功率稳定性：{}'''.format(title,date,worker,fibertype,producer,fiberNo,
#       title1st,temperature,humidity,signalwavelength,signalpulsewidth,
#       signalfrequence,secondpulsepower,fiberlength,timelong,title2st,
#       maxsignalpower,minsingalpower,averagesingalepower,powerstable)
#       return txtContext

#     def xlsContainGet(self):
#         text = self.pickContext
#         xlsContain =(
#         (text.get('title','')),
#         ('日期：', text.get('date','')),
#         ('操作人：', text.get('worker','')),
#         ('光纤型号：', text.get('fibertype','')),
#         ('生产厂家：', text.get('producer','')),
#         ('光纤编号：', text.get('fiberNo','')),
#         (text.get('title1st','')),
#         ('环境温度：', text.get('temperature','')),
#         ('环境湿度：', text.get('humidity','')),
#         ('信号光波长：', text.get('signalwavelength','')),
#         ('信号光脉宽：', text.get('signalpulsewidth','')),
#         ('信号光频率：', text.get('signalfrequence','')),
#         ('二级泵浦光功率: ', text.get('secondpulsepower','')),
#         ('光纤长度：', text.get('fiberlength','')),
#         ('测试时长：', str(int(text.get('timelong','')))),
#         (text.get('title2st','')),
#         ('信号光功率最大值：', self.__Power2str(text.get('maxsignalpower',''))),
#         ('信号光功率最小值：', self.__Power2str(text.get('minsingalpower',''))),
#         ('信号光功率平均值：', self.__Power2str(text.get('averagesingalepower',''))),
#         ('功率稳定性：', self.__Power2str(text.get('powerstable','')))
#         )
#         return xlsContain

#     def thtmlGet(self):
#         text = self.pickContext
#         title = text.get('title','')
#         date = text.get('date','')
#         worker = text.get('worker','')
#         print(worker)
#         fibertype = text.get('fibertype','')
#         producer = text.get('producer','')
#         fiberNo = text.get('fiberNo','')

#         title1st = text.get('title1st','')
#         temperature = text.get('temperature','')
#         humidity = text.get('humidity','')
#         signalwavelength = text.get('signalwavelength','')
#         signalpulsewidth = text.get('signalpulsewidth','')
#         signalfrequence = text.get('signalfrequence','')
#         secondpulsepower = text.get('secondpulsepower','')
#         fiberlength = text.get('fiberlength','')
#         timelong = str(int(text.get('timelong','')))

#         title2st = text.get('title2st','')
#         maxsignalpower = self.__Power2str(text.get('maxsignalpower',''))
#         minsingalpower = self.__Power2str(text.get('minsingalpower',''))
#         averagesingalepower = self.__Power2str(text.get('averagesingalepower',''))
#         powerstable = self.__Power2str(text.get('powerstable',''))
#         # imgsrc = text.get('imgsrc','')



#         thtml = '''
#     <!DOCTYPE html><html><head><meta charset="utf-8"><style>body {
#       width: 45em;
#       border: 1px solid #ddd;
#       outline: 1300px solid #fff;
#       margin: 16px auto;
#       font-family: 'Microsoft YaHei', "Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif;
#       -webkit-text-size-adjust: 100%;
#       word-wrap: break-word;
#       overflow: hidden;
#     }
#     h1 {
#       font-size: 2em;
#       margin: 0.67em 0;
#       color: #283c51;
#       position: relative;
#       margin-top: 1em;
#       margin-bottom: 16px;
#       font-weight: bold;

#       padding-left: 8px;
#       margin-left: 30px;
#       padding-bottom: 0.3em;
#       border-bottom: 1px solid #eee;
#     /*
#       line-height: 1.4;
#     */
#     }

#     h2 {
#       font-size: 30px;
#       font-weight: bold;
#       color: #2EA9DF;
#       padding-bottom: 0.3em;
#       border-bottom: 1px solid #eee;
#       orphans: 3;
#       widows: 3;
#     /*  text-align:center;
#       text-decoration: none;
#       margin-top: 15px;
#       margin-bottom: 15px;
#       margin-left: 30px;
#       position: relative;

#       line-height: 1.4;
#       display: inline-block;
#       display: none;

#       height: 1em;
#     */  padding-left: 8px;


#     }
#     p {
#       padding-left: 8px;
#       margin-left: 45px;
#     }
#     img {
#       border: 0;
#       align:center
#       max-width: 100%;
#       -moz-box-sizing: border-box;
#       box-sizing: border-box;
#       page-break-inside: avoid;
#     }
#     </style><title>'''+title+'''</title></head><body>
#     <h1 id="_1">'''+title+'''</h1>
#     <p>日期：'''+date+'''<br />
#     操作人：'''+worker+'''<br />
#     光纤型号：'''+fibertype+'''<br />
#     生产厂家：'''+producer+'''<br />
#     光纤编号：'''+fiberNo+'''</p>
#     <h2 id="_2">'''+title1st+'''</h2>
#     <p>环境温度：'''+temperature+'''<br />
#     环境湿度：'''+humidity+'''<br />
#     信号光波长：'''+signalwavelength+'''<br />
#     信号光脉宽：'''+signalpulsewidth+'''<br />
#     信号光频率：'''+signalfrequence+'''<br />
#     二级泵浦光功率: '''+secondpulsepower+'''<br />
#     光纤长度：'''+fiberlength+'''<br />
#     测试时长：'''+timelong+'''</p>
#     <h2 id="_3">'''+title2st+'''</h2>
#     <p>信号光功率最大值：'''+maxsignalpower+'''<br />
#     信号光功率最小值：'''+minsingalpower+'''<br />
#     信号光功率平均值：'''+averagesingalepower+'''<br />
#     功率稳定性：'''+powerstable+'''<br /></p>
#     <img src= "data/plot.svg">
#     </body></html>
#     '''
#         # print('worker',worker)
#         return thtml

#     def __Power2str(self,data):
#         if data > 0.1:
#             return str(round(data,2))+'W'
#         else:
#             return str(round(data*1000,2)) + 'mW'

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
