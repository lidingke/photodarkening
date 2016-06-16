
from PyQt5.QtWidgets import QDialog
from UI.reportDialogUI import Ui_Dialog
from lastlog import LastLog
from PyQt5.QtCore import pyqtSignal

class ReportDialog(QDialog):
    result = pyqtSignal(object)
    """docstring f or reportDialog"""
    def __init__(self,father):
        super(ReportDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.pick = father.pickContext
        self.father = father
        self.lastlog  = LastLog('data\\reportLast.pickle')
        self.setInitText()

    def setInitText(self):
        if self.pick == False:
            self.pick = self.lastlog.loadLast()
        self.setAllContext(self.pick)
        # else:


    # def saveLast(self,text):
    #     # if self.pick == False:
    #     last = self.lastlog
    #     pick = self.pick
    #     last.saveLast(pick)

    def setAllContext(self,text):
        # title = text.get('title','')
        date = text.get('date','')
        worker = text.get('worker','')
        fibertype = text.get('fibertype','')
        producer = text.get('producer','')
        fiberNo = text.get('fiberNo','')
        # title1st = text.get('title1st','')
        temperature = text.get('temperature','')
        humidity = text.get('humidity','')
        # signalwavelength = text.get('signalwavelength','')
        # signalpulsewidth = text.get('signalpulsewidth','')
        # signalfrequence = text.get('signalfrequence','')
        # secondpulsepower = text.get('secondpulsepower','')
        fiberlength = text.get('fiberlength','')
        # timelong = text.get('timelong','')
        self.ui.lineEditDate.setText(date)
        self.ui.lineEditWorker.setText(worker)
        self.ui.lineEditFibertype.setText(fibertype)
        self.ui.lineEditProducer.setText(producer)
        self.ui.lineEditFiberNo.setText(fiberNo)
        self.ui.lineEditTemperature.setText(temperature)
        self.ui.lineEditHumidity.setText(humidity)
        # self.ui.lineEditSignalwavelength.setText(signalwavelength)
        # self.ui.lineEditSignalpulsewidth.setText(signalpulsewidth)
        # self.ui.lineEditSignalfrequence.setText(signalfrequence)
        # self.ui.lineEditSecondpulsepower.setText(secondpulsepower)
        self.ui.lineEditFiberlength.setText(fiberlength)
        # self.ui.lineEditTimelong.setText(timelong)
        # self.ui.lineEdit

    def getAllcontext(self):
        text = dict()
        text['date'] = self.ui.lineEditDate.text()
        text['worker'] = self.ui.lineEditWorker.text()
        text['fibertype'] = self.ui.lineEditFibertype.text()
        text['producer'] = self.ui.lineEditProducer.text()
        text['fiberNo'] = self.ui.lineEditFiberNo.text()
        # title1st = text.get('title1st','')
        text['temperature'] =self.ui.lineEditTemperature.text()
        text['humidity'] =self.ui.lineEditHumidity.text()
        # text['signalwavelength'] = self.ui.lineEditSignalwavelength.text()
        # text['signalpulsewidth',] = self.ui.lineEditSignalpulsewidth.text()
        # text['signalfrequence'] = self.ui.lineEditSignalfrequence.text()
        # text['secondpulsepower'] = self.ui.lineEditSecondpulsepower.text()
        text['fiberlength'] = self.ui.lineEditFiberlength.text()
        # text['timelong'] = self.ui.lineEditTimelong.text()
        # print(text)
        return text


    def closeEvent(self,event):
        # print('reWrite closeEvent')
        text = self.getAllcontext()
        self.father.pickContext.update(text)
        # self.result.emit(text)
        # print(text['worker'])
        self.lastlog.saveLast(text)



if __name__ == '__main__':
    from pdfcreater import PdfContext
    pcontext = PdfContext()
    last = LastLog()
    pick = last.loadLast()
    report = pcontext.getContext()
    pick['reportConext'] = report
    last.saveLast(pick)
    # print(pick.keys())
