import sqlite3
import pdb
import numpy as np
con = sqlite3.connect('data\\powerdata.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tableLst=cursor.fetchall()
print('lasttable',tableLst[-1])
tableName = tableLst[-1][0]
strEx='select * from '+tableName
cursor.execute(strEx)

data = cursor.fetchall()
print('lastdata', data[-1])
lit = []
for x in data:
    lit.append(x[1])

print('np.std',np.std(lit))
