# text = {}


# print(xlsContain)

# import xlwt
# workbook = xlwt.Workbook(encoding= 'utf-8')
# booksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok= True)
# workbook.add_sheet('Sheet2')

# for i,row in enumerate(xlsContain):
#         for j,col in enumerate(row):
#                 booksheet.write(i, j, col)
#                 print(i,j,col)



# beginnum = i
# for i,row in enumerate(a):
#         for j,col in enumerate(row):
#                 booksheet.write(i+beginnum, j, col)
#                 print(i+beginnum,j,col)
# # booksheet.col(0).width = 10

# # booksheet.write(1,1,'lidingke')



# print('++\r\n',xlsContain+a)


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
                                # print(i,j,col)

if __name__ == '__main__':
        text = {}
        xlsContain =(
(text.get('title','')),
('日期：', text.get('date','')),
('操作人：', text.get('worker','')),
('光纤型号：', text.get('fibertype','')),
('生产厂家：', text.get('producer','')),
('光纤编号：', text.get('fiberNo','')),
(text.get('title1st','')),
('环境温度：', text.get('temperature','')),
('环境湿度：', text.get('humidity','')),
('信号光波长：', text.get('signalwavelength','')),
('信号光脉宽：', text.get('signalpulsewidth','')),
('信号光频率：', text.get('signalfrequence','')),
('二级泵浦光功率: ', text.get('secondpulsepower','')),
('光纤长度：', text.get('fiberlength','')),
('测试时长：', text.get('timelong','')),
(text.get('title2st','')),
('信号光功率最大值：', text.get('maxsignalpower','')),
('信号光功率最小值：', text.get('minsingalpower','')),
('信号光功率平均值：', text.get('averagesingalepower','')),
('功率稳定性：', text.get('powerstable',''))
)
        a = ((1,2),(3,4),(5,6))

        xw = XlsWrite(xlsContain= xlsContain + a).runSave()
