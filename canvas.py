
import time
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import reportlab.pdfbase.ttfonts
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('微软雅黑', 'Fonts/msyh.ttc'))
import reportlab.lib.fonts

class pdfCreater(object):
    """docstring for pdfCreater"""
    def __init__(self):
        super(pdfCreater, self).__init__()
        #self.arg = arg
        self.firstList = list()
        self.fileName = "report.pdf"


    def context(self):
        self.title = u"掺镱光纤光子暗化测试报告"
        self.firstList.append(u"\n")
        self.firstList.append(u"日期:2016/03/16 11:30")
        self.firstList.append(u"操作人:XXX")
        self.firstList.append(u"光纤型号:10/130 DC-YDF")
        self.firstList.append(u"打印中文？")

    def create_pdf(self):
        #imputtxt = ['hello1','hello2','hello3']
        date = time.ctime()
        c = canvas.Canvas(self.fileName)
        c.setFont('微软雅黑', 10)
        textobject = c.beginText()

        textobject.setTextOrigin(inch, 11*inch)
        c.setStrokeColorRGB(0.2,0.5,0.3)
        textobject.textLines(self.title)
        #c.setFillColorRGB(0,0,0.77)
        for line in self.firstList:
            #line=line
            textobject.textLine(line.strip())
            print(line)
        a = c.drawText(textobject)
        c.drawImage('Image/example.png',50,100)
        c.showPage()
        c.save()
    #report = disk_report()
    #create_pdf()


if __name__ == '__main__':
    app = pdfCreater()
    app.context()
    app.create_pdf()

