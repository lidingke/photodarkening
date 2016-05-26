import sqlite3
import time
import logging
import pdb

class DataHand(object):
    """docstring for DataHand
    table: 'TM'+dateNow+'US'+self.username
    """
    def __init__(self, name = 'data\\powerdata.db'):
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
            ' (time float(17), power float(10), data varchar(10))'
            cursor.execute(strEx)
        except Exception as e:
            raise e
        cursor.close()
        conn.commit()
        conn.close()
        return sqlTableName

    def save2Sql(self,sqlTableName,localTime,power,data):

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='insert into '+sqlTableName+'(time, power,data) values ('+str(localTime)+' , '+str(power)+', \''+data+'\')'
            print(strEx)
            cursor.execute(strEx)

        except sqlite3.OperationalError as e :
            raise e

            print('database is busy! data is not save')
        except Exception as e:
            logging.exception(e)
            self.closeConnect()
            raise e
        cursor.close()
        conn.commit()
        conn.close()

    def getTable(self):
        con = sqlite3.connect(self.name)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tableLst=cursor.fetchall()
        return tableLst


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


    def save2SqlAll(self,sqlTableName,datalist):
        # pdb.set_trace()
        print('start database log',self.name)
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='create table if not exists '+sqlTableName+\
            ' (time float(17), power float(10), data varchar(10))'
            cursor.execute(strEx)
        except Exception as e:
            raise e
        for da in datalist:
        #     pass
        # while datalist:
        #     # pass
            # da = datalist.pop()
            try:
                strEx='insert into '+sqlTableName+' (time, power,data) values ('+str(da[0])+' , '+str(0)+', \''+da[1].hex()+'\')'
                # print(strEx)
                cursor.execute(strEx)
            except sqlite3.OperationalError as e :
                raise e

                print('database is busy! data is not save')
            except Exception as e:
                logging.exception(e)
                # self.closeConnect()
                raise e
        datalist.clear()
        cursor.close()
        conn.commit()
        conn.close()
        print('datasave done',self.name)



# if __name__ == '__main__':
#     dhand = DataHand()
#     tableName =
#     dhand.getTableData(tableName)
