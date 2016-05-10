import sys
from PyQt5.QtGui import QPagedPaintDevice, QPdfWriter, QTextDocument
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
# from PyQt5.QtPrintSupport import QPrinter
import pdb
class PdfCreater(object):
    """docstring for PdfCreater"""
    def __init__(self,parentWidget,context = {}):
        super(PdfCreater, self).__init__()
        self.parent = parentWidget
        self.powerstable = '12'
        # self.htmlGet()
        pc = PdfContext()
        self.thtml = pc.thtmlGet()
        self.fileName = 'test.pdf'
        # self.context = context


    def run(self):
        # print(self.thtml[-100:])
        self.savePdf()

    def savePdf(self):
        pt = QPdfWriter(self.fileName)
        pt.logicalDpiX
        pt.setPageSize(QPagedPaintDevice.A4)

        textDocument = QTextDocument()
        textDocument.setHtml(self.thtml)
        textDocument.print_(pt)
        textDocument.end()
        print('pdf creat = ',self.fileName)

    def saveToFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self.parent, "Save Report",
                '', "Adoble PDF (*.pdf);;All Files (*)")
        # print('fileName',fileName)
        # pdb.set_trace()
        if not fileName:
            return
        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return
        out_file.close()
        self.fileName = fileName
        # print(self.fileName)
        # pickle.dump(self.contacts, out_file)

class PdfContext(object):
    """docstring for PdfContext"""
    def __init__(self):
      super(PdfContext, self).__init__()
      # self.arg = arg
      self.context = {
      'title': '掺镱光纤光子暗化测试报告',
      'date': '2016/03/16 11:30',
      'worker': 'XXX',
      'fibertype': '10/130 DC-YDF',
      'producer': 'YOFC',
      'fiberNo': 'XXXXXXXX',

      'title1st': '测试条件',
      'temperature': '25℃',
      'humidity': '30%',
      'signalwavelength': '1064nm',
      'signalpulsewidth': '26ns',
      'signalpulsewidth': '100kHz',
      'secondpulsepower': '6.20W',
      'fiberlength': '4.5m',
      'timelong': '10hr',

      'title2st': '测试结果',
      'maxsignalpower': '2.74W',
      'minsingalpower': '2.68W',
      'averagesingalepower': '2.71W',
      'powerstable': '±1.1%',
      'imgsrc':'recycle/Image/example.png'

      }

    def getContext(self):
      return self.context

    def inputContext(self,context):
      self.context = context

    def thtmlGet(self):
        text = self.context
        title = text.get('title','')
        date = text.get('date','')
        worker = text.get('worker','')
        fibertype = text.get('fibertype','')
        producer = text.get('producer','')
        fiberNo = text.get('fiberNo','')

        title1st = text.get('title1st','')
        temperature = text.get('temperature','')
        humidity = text.get('humidity','')
        signalwavelength = text.get('signalwavelength','')
        signalpulsewidth = text.get('signalpulsewidth','')
        signalfrequence = text.get('signalfrequence','')
        secondpulsepower = text.get('secondpulsepower','')
        fiberlength = text.get('fiberlength','')
        timelong = text.get('timelong','')

        title2st = text.get('title2st','')
        maxsignalpower = text.get('maxsignalpower','')
        minsingalpower = text.get('minsingalpower','')
        averagesingalepower = text.get('averagesingalepower','')
        powerstable = text.get('powerstable','')
        imgsrc = text.get('imgsrc','')



        thtml = '''
    <!DOCTYPE html><html><head><meta charset="utf-8"><style>body {
      width: 45em;
      border: 1px solid #ddd;
      outline: 1300px solid #fff;
      margin: 16px auto;
      font-family: 'Microsoft YaHei', "Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif;
      -webkit-text-size-adjust: 100%;
      word-wrap: break-word;
      overflow: hidden;
    }
    h1 {
      font-size: 2em;
      margin: 0.67em 0;
      color: #283c51;
      position: relative;
      margin-top: 1em;
      margin-bottom: 16px;
      font-weight: bold;

      padding-left: 8px;
      margin-left: 30px;
      padding-bottom: 0.3em;
      border-bottom: 1px solid #eee;
    /*
      line-height: 1.4;
    */
    }

    h2 {
      font-size: 30px;
      font-weight: bold;
      color: #2EA9DF;
      padding-bottom: 0.3em;
      border-bottom: 1px solid #eee;
      orphans: 3;
      widows: 3;
    /*  text-align:center;
      text-decoration: none;
      margin-top: 15px;
      margin-bottom: 15px;
      margin-left: 30px;
      position: relative;

      line-height: 1.4;
      display: inline-block;
      display: none;

      height: 1em;
    */  padding-left: 8px;


    }
    p {
      padding-left: 8px;
      margin-left: 45px;
    }
    img {
      border: 0;
      align:center
      max-width: 100%;
      -moz-box-sizing: border-box;
      box-sizing: border-box;
      page-break-inside: avoid;
    }
    </style><title>'''+title+'''</title></head><body>
    <h1 id="_1">'''+title+'''</h1>
    <p>日期：'''+date+'''<br />
    操作人：'''+worker+'''<br />
    光纤型号：'''+fibertype+'''<br />
    生产厂家：'''+producer+'''<br />
    光纤编号：'''+fiberNo+'''</p>
    <h2 id="_2">'''+title1st+'''</h2>
    <p>环境温度：'''+temperature+'''<br />
    环境湿度：'''+humidity+'''<br />
    信号光波长：'''+signalwavelength+'''<br />
    信号光脉宽：'''+signalpulsewidth+'''<br />
    信号光频率：'''+signalfrequence+'''<br />
    二级泵浦光功率: '''+secondpulsepower+'''<br />
    光纤长度：'''+fiberlength+'''<br />
    测试时长：'''+timelong+'''</p>
    <h2 id="_3">'''+title2st+'''</h2>
    <p>信号光功率最大值：'''+maxsignalpower+'''<br />
    信号光功率最小值：'''+minsingalpower+'''<br />
    信号光功率平均值：'''+averagesingalepower+'''<br />
    功率稳定性：'''+powerstable+'''</p>
    <img src="'''+imgsrc+'''">
    </body></html>
    '''
        return thtml


if __name__ == '__main__':
    app = QApplication(sys.argv)
    PdfCreater().run()
    app.exec_()
