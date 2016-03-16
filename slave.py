
import serial
from serial.tools import list_ports
import re
from model import Model
import threading
import random
from time import sleep


class Slave(object):
	"""docstring for Slave"""
	def __init__(self):
		super(Slave, self).__init__()
		#self.arg = arg
		self.currentSendLive = True
		self.running = True

	def currentSend(self,ser):
		while self.currentSendLive is True:

			currentmsg = self.sendmsg['seedcurrentvaluegetreturn']
			cb = int(random.uniform(2,10)*100)
			cb = cb.to_bytes(2,'big')
			#print(currentmsg,':',cb)
			currentmsg = currentmsg.replace(b'\xFF\xFF',cb)
			#print(currentmsg)
			cp = 0
			print('发送电流：',currentmsg,': int ',cb,int().from_bytes(cb,'big'))

			ser.write(currentmsg)

			sleep(10)
			#return currentmsg

	def randomSend(self,ser):
		while self.currentSendLive is True:
			self.sendmsglist = [v for k,v in self.sendmsg.items()]
			rd = int(random.uniform(2,len(self.sendmsglist)))

			print('发送：',self.sendmsglist[rd])
			ser.write(self.sendmsglist[rd])
			sleep(60)
			#return currentmsg




	def process(self):

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

		self.sendmsg = model.get_msgDict()
		self.sendmsgrec = dict([(v,k) for k,v in self.sendmsg.items()])

		ser = model.get_ser()

		print('上位机信号包大小为：',len(self.sendmsgrec))
		#ser = serial.Serial(port_serial,9600,timeout = 120)
		print('下位机模拟器启动')
		print("check which port was really used >",ser.name)
		#threading.Thread()
		#ser.write(b'\xEB\x90\x04\x05\x09\x07\x08\x09\x90\xEB')
		#开个线程定时发送电流
		#threading.Thread(target=Slave.currentSend,args=(self,ser,)).start()
		#开个线程随机发送信号
		threading.Thread(target=Slave.randomSend,args=(self,ser,)).start()

		while True:
			sertext = model.analysisbit(ser)
			#sertext=ser.read(7)
			if len(sertext) > 0:
				sertext = b'\xEB\x90'+sertext+b'\x90\xEB'
				print('下位机接收：',sertext)
				#print(self.sendmsgrec.get(sertext))


		ser.close()

	# def analysisbit(self,ser):
	#         '''
	#                 return without package
	#         '''
	#         readlive = True
	#         # xebstatue = False
	#         # x90statue = False
	#         bitlist = list()
	#         while readlive and self.running:
	#             databit = self.readbit(ser)
	#             if databit == b'\xeb':
	#                 print(databit,'1')
	#                 databit = self.readbit(ser)
	#                 if databit == b'\x90':
	#                     while True:
	#                         print(databit,'2')
	#                         databit = self.readbit(ser)
	#                         if databit == b'\x90':
	#                             databit = self.readbit(ser)
	#                             data = b''.join(bitlist)
	#                             print(data)
	#                             return data
	#                         bitlist.append(databit)


	# def readbit(self,ser):
	#     sleep(0.1)
	#     try:
	#         data = ser.read(1)
	#     except Exception as e:
	#         raise e
	#     except portNotOpenError :
	#         sleep(1)
	#     return data




if __name__=='__main__':
		slave = Slave()
		slave.process()


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
