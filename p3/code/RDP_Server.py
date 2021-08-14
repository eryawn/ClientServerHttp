import random
import sys
from socket import *
import math
import codecs

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((sys.argv[1],int(sys.argv[2])))



if True:
	seq=0
	ack=0
	message=""
	payload=""
	addr=0
	print("ready to serve ...")
	data,addr=serverSocket.recvfrom(1024)
	data=data.decode()
	splitData=data.split()
	ack=int(splitData[1])+1
	message="ACK "+str(seq)+" "+str(ack)
	serverSocket.sendto(message.encode(),addr)
	#print("keypoint 1")
	while True:
		data,addr=serverSocket.recvfrom(1024)
		#print("key2")
		data=data.decode()
		if data.split()[0]=="ACK":
			break
		elif data.split()[0]=="SYN":
			serverSocket.sendto(message.encode(),addr)
			#print("repeat\n")

	while True:
		data,addr=serverSocket.recvfrom(1024)
		data=data.decode()
		if data.split()[0]=="GET":
			break
	
	splitData=data.split()
	file=splitData[4]
	ack=int(splitData[1])+len(file)
	f=codecs.open(file,"r",encoding="utf-8")
	totalData=f.read()
	f.close()
	segCount=int(math.ceil(float(len(totalData))/992))
	for i in range(0,segCount-1):
		payload=totalData[0+i*992:992+i*992]
		
		message="DATA "+str(seq)+" "+str(ack)+" "+str(len(payload))+" "+payload
		#print(message+"\n")
		seq=seq+len(payload)
		serverSocket.sendto(message.encode('utf-8'),addr)
		data,addr=serverSocket.recvfrom(1024)
		data=data.decode()
		while int(data.split()[2])<seq:
			serverSocket.sendto(message.encode('utf-8'),addr)
			data,addr=serverSocket.recvfrom(1024)
			data=data.decode()

	
	payload=totalData[0+(segCount-1)*992:]
	message="DATA "+str(seq)+" "+str(ack)+" "+str(len(payload))+" "+payload
	seq=seq+len(payload)
	serverSocket.sendto(message.encode('utf-8'),addr)
	data,addr=serverSocket.recvfrom(1024)
	data=data.decode()
	while int(data.split()[2])<seq:
		serverSocket.sendto(message.encode(),addr)
		data,addr=serverSocket.recvfrom(1024)
		data=data.decode()

	message="FIN "+str(seq)+" "+str(ack)
	serverSocket.sendto(message.encode(),addr)
	serverSocket.settimeout(1)
	while 1:
		try:
			data,addr=serverSocket.recvfrom(1024)
		except timeout as e:
			break
		else:
			serverSocket.sendto(message.encode(),addr)
			serverSocket.settimeout(1)
	

	


