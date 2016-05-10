import sqlite3
import time
import logging

class DataHand(object):
    """docstring for DataHand
    table: 'TM'+dateNow+'US'+self.username
    """
    def __init__(self, name = 'data\\data.db'):
        super(DataHand, self).__init__()
        self.name = name
        logging.basicConfig(filename = 'data\\databaselog.txt', filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')
        self.username = 'nobody'


    def initSqltabel(self,localTime,username):
        # localTime=time.localtime()
        localTime = str(int(localTime))
        sqlTableName='TM'+localTime+'US'+username
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='create table if not exists '+sqlTableName+\
            ' (time float(17), power float(10))'
            cursor.execute(strEx)
        except Exception as e:
            raise e
        cursor.close()
        conn.commit()
        conn.close()
        return sqlTableName

    def save2Sql(self,sqlTableName,localTime,power):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='insert into '+sqlTableName+'(time, power) values ('+str(localTime)+' , '+str(power)+' )'
            cursor.execute(strEx)
        except sqlite3.OperationalError:
                print('database is busy! data is not save')
        except Exception as e:
            logging.exception(e)
            self.closeConnect()
            raise e
        cursor.close()
        conn.commit()
        conn.close()

    def getTableData(self,tableName):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='select * from '+tableName
            cursor.execute(strEx)
        except sqlite3.OperationalError as e:
            print(e)

        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data

    def createPlot(self,data):
        print('plot:',len(data))




# if __name__ == '__main__':
#     dhand = DataHand()
#     tableName =
#     dhand.getTableData(tableName)
