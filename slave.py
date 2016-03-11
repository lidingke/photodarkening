
import serial
from serial.tools import list_ports
import re
from model import Model



def main():


	devState={
		'comNum':'com3',
		'comState':'open',
		'seedState':'open',
		'1stState':'close',
		'1stValue':'0',
		'2stState':'close',
		'2stValue':'0'
		}


	port_list = list(list_ports.comports())
	port_serial = 'com13'
	model = Model()
	model.set_port(port_serial)

	model.begin()
	#model.start()

	sendmsg = model.get_msgDict()
	sendmsgrec = dict([(v,k) for k,v in sendmsg.items()])
	ser = model.get_ser()
	print(sendmsgrec)
	#ser = serial.Serial(port_serial,9600,timeout = 120)
	print('下位机模拟器启动')
	print("check which port was really used >",ser.name)

	#ser.write(b'\xEB\x90\x04\x05\x09\x07\x08\x09\x90\xEB')

	while True:
		#sertext=ser.read(7)
		sertext = b'\xEB\x90'+model.analysisbit()+b'\x90\xEB'
		print(sertext)
		print(sendmsgrec.get(sertext))
		# if sertext:
		# 	if sertext == sendmsg['hellocom']:
		# 		ser.write(b'back0'+sertext)
		# 		print('Com state is ',devState['comState'])
		# 	elif sertext == sendmsg['openseed']:
		# 		ser.write(b'back0'+sertext)
		# 		if devState['seedState'] == 'open':
		# 			ser.write(b'isopen000000000')
		# 			print('seed state is open')
		# 		else:
		# 			devState['seedState'] == 'open'
		# 			print('open the seed and pulse')
		# 	elif sertext == sendmsg['frequencyajust']:
		# 		ser.write(b'back0'+sertext)
		# 		if devState['seedState'] == 'open':
		# 			#ser.write(b'isopen000000000')
		# 			print('set frequency')
		# 		else:
		# 			print('seed is close')
		# 	elif sertext == sendmsg['pulsewidthajust']:
		# 		ser.write(b'back0'+sertext)
		# 		if devState['seedState'] == 'open':
		# 			#ser.write(b'isopen000000000')
		# 			print('set pulsewidth')
		# 		else:
		# 			print('seed is close')
		# 	elif sertext == sendmsg['open1st']:
		# 		if devState['1stState'] == 'open':
		# 			print('1stState is open')
		# 		else:
		# 			devState['1stState']='open'
		# 			print('open1st')
		# 	elif sertext == sendmsg['sendcurrent']:
		# 		print('sendcurrent')
		# 	elif sertext == sendmsg['open2sr']:
		# 		if devState['2stState'] == 'open':
		# 			print('2stState is open')
		# 		else:
		# 			devState['2stState']='open'
		# 			print('open1st')
		# 	else:
		# 		pass

	ser.close()

if __name__=='__main__':
	main()
