
from collections import MutableMapping
from model.toolkit import WRpickle


class MetaDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __str__(self):
        return  self.store.__str__()

class Singleton(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]
"""
#python2
class MyClass(BaseClass):
        __metaclass__ = Singleton
#python3
class MyClass(BaseClass, metaclass = Singleton):
"""

def singleton(class_):
    instance = {}
    def getinstance(*args,**kwargs):
        if class_ not in instance:
            instance[class_] = class_(*args,**kwargs)
        return instance[class_]
    return getinstance


@singleton
class PickContext(MetaDict):
    """docstring for PickContext"""
    def __init__(self, ):
        MetaDict.__init__(self)
        self.pickContext = self.store

        try:
            self.wrpick = WRpickle('data\\reportLast.pickle')
            self.pickContext.update(self.wrpick.loadPick())
        except FileNotFoundError:
            self.pickContext.update({
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
                'imgsrc':'plot.pdf'})

    def save_pick_file(self):
        self.wrpick.savePick(self.pickContext)

    # def getContext(self):
    #   return self.pickContext

    # def inputContext(self,context):
    #   self.pickContext = context

    def txtGet(self):
      text = self.pickContext
      title = text.get('title','')
      date = text.get('date','')
      worker = text.get('worker','')
      # print(worker)
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
      txtContext = '''
    {}
    日期：{}\r\n
    操作人：{}\r\n
    光纤型号：{}\r\n
    生产厂家：{}\r\n
    光纤编号：{}
    {}\r\n
    环境温度：{}\r\n
    环境湿度：{}\r\n
    信号光波长：{}\r\n
    信号光脉宽：{}\r\n
    信号光频率：{}\r\n
    二级泵浦光功率: {}\r\n
    光纤长度：{}\r\n
    测试时长：{}
    {}\r\n
    信号光功率最大值：{}\r\n
    信号光功率最小值：{}\r\n
    信号光功率平均值：{}\r\n
    功率稳定性：{}'''.format(title,date,worker,fibertype,producer,fiberNo,
      title1st,temperature,humidity,signalwavelength,signalpulsewidth,
      signalfrequence,secondpulsepower,fiberlength,timelong,title2st,
      maxsignalpower,minsingalpower,averagesingalepower,powerstable)
      return txtContext

    def xlsContainGet(self):
        text = self.pickContext
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
        return xlsContain

    def thtmlGet(self):
        text = self.pickContext
        print('HTML get:',text)
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

        thtml = '''
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <style>
    body {
        /*overflow-y:scroll;*/
        width: 45em;
        border: 1px solid #ddd;
        outline: 1300px solid #fff;
        margin: 16px auto;
        font-family: 'Microsoft YaHei', "Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif;

    }

    h1 {
        border-bottom: 1px solid #eee;
        margin-top: 1em;
        margin-bottom: 16px;
        margin-left: 30px;
        margin: 0.67em 0;
        padding-left: 8px;
        padding-bottom: 0.3em;
        font-size: 50px;
        font-weight: bold;
        color: #283c51;
    }

    h2 {
        border-bottom: 1px solid #eee;
        padding-bottom: 0.3em;
        margin-left: 30px;
        padding-left: 20px;
        font-size: 40px;
        font-weight: bold;
        color: #2EA9DF;

    }

    p {
        padding-left: 20px;
        /*margin-left: 45px;
        font-size: 20px;*/
    }

    img {
        -moz-box-sizing: border-box;
        box-sizing: border-box;

    }
    </style>
    <title>'''+title+'''</title>
</head>

<body>
    <h1 id="_1">'''+title+'''</h1>
    <p>日期：'''+date+'''
        <br /> 操作人：'''+worker+'''
        <br /> 光纤型号：'''+fibertype+'''
        <br /> 生产厂家：'''+producer+'''
        <br /> 光纤编号：'''+fiberNo+'''
    </p>
    <h2 id="_2">'''+title1st+'''</h2>
    <p>环境温度：'''+temperature+'''
        <br /> 环境湿度：'''+humidity+'''
        <br /> 信号光波长：'''+signalwavelength+'''
        <br /> 信号光脉宽：'''+signalpulsewidth+'''
        <br /> 信号光频率：'''+signalfrequence+'''
        <br /> 二级泵浦光功率: '''+secondpulsepower+'''
        <br /> 光纤长度：'''+fiberlength+'''
        <br /> 测试时长：'''+timelong+'''
    </p>
    <h2 id="_3">'''+title2st+'''</h2>
    <p>信号光功率最大值：'''+maxsignalpower+'''
        <br /> 信号光功率最小值：'''+minsingalpower+'''
        <br /> 信号光功率平均值：'''+averagesingalepower+'''
        <br /> 功率稳定性：'''+powerstable+'''
        <br />
    </p>
    <img src= "data/plot.svg">
</body>

</html>
    '''
        # print('worker',worker)
        print('thtml:',thtml)
        return thtml

    def __Power2str(self,data):
        if data > 0.1:
            return str(round(data,2))+'W'
        else:
            return str(round(data*1000,2)) + 'mW'




