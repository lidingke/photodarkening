
import serial
from serial.tools import list_ports
import re

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

	sendmsg = {
            'sendcurrent':b'sendcurrent0000',
            'openlaser':b'openlaser000000',
            'closelaser':b'closelaser00000',
            'pulsewidthajust':b'pulsewidthajust',
            'frequencyajust':b'frequencyajust0',
            'hellocom':b'hellocom0000000',
            'openseed':b'openseed0000000',
            'open1st':b'open1st00000000',
            'open2sr':b'open2sr00000000',
            '1stajust':b'1stajust0000000',
            '2stajust':b'2stajust0000000'
            }

	port_list = list(list_ports.comports())
	port_serial = 'com13'


	ser = serial.Serial(port_serial,9600,timeout = 120)
	print('下位机模拟器启动')
	print("check which port was really used >",ser.name)

	#ser.write(b'\xEB\x90\x04\x05\x09\x07\x08\x09\x90\xEB')

	while True:
		sertext=ser.read(15)
		if sertext:
			if sertext == sendmsg['hellocom']:
				ser.write(b'back0'+sertext)
				print('Com state is ',devState['comState'])
			elif sertext == sendmsg['openseed']:
				ser.write(b'back0'+sertext)
				if devState['seedState'] == 'open':
					ser.write(b'isopen000000000')
					print('seed state is open')
				else:
					devState['seedState'] == 'open'
					print('open the seed and pulse')
			elif sertext == sendmsg['frequencyajust']:
				ser.write(b'back0'+sertext)
				if devState['seedState'] == 'open':
					#ser.write(b'isopen000000000')
					print('set frequency')
				else:
					print('seed is close')
			elif sertext == sendmsg['pulsewidthajust']:
				ser.write(b'back0'+sertext)
				if devState['seedState'] == 'open':
					#ser.write(b'isopen000000000')
					print('set pulsewidth')
				else:
					print('seed is close')
			elif sertext == sendmsg['open1st']:
				if devState['1stState'] == 'open':
					print('1stState is open')
				else:
					devState['1stState']='open'
					print('open1st')
			elif sertext == sendmsg['sendcurrent']:
				print('sendcurrent')
			elif sertext == sendmsg['open2sr']:
				if devState['2stState'] == 'open':
					print('2stState is open')
				else:
					devState['2stState']='open'
					print('open1st')
			else:
				pass

	ser.close()

if __name__=='__main__':
	main()
