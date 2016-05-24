
from database import DataHand
from modelpump import TempDetector

# datahand = DataHand()
# data = datahand.getTableData('TEST123')
tDt = TempDetector()
phex = '9a66089a0e9b040500ff0fa9'
power =tDt.hex2power(b''.fromhex(phex))
print(power)
# print(len(data))
