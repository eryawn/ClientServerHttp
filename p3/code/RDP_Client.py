from socket import *
from datetime import *
import sys
import codecs

clientSocket=socket(AF_INET, SOCK_DGRAM)

address=(sys.argv[1],int(sys.argv[2]))

message=""
seq=0
ack=0
recvfile=sys.argv[4]
f=codecs.open(recvfile,"w",encoding="utf-8")
content=""

message="SYN "+str(seq)+" "+str(ack)
seq=seq+1
clientSocket.sendto(message.encode(),address)
clientSocket.settimeout(1)
while 1:
	try:
		data,addr=clientSocket.recvfrom(1024)
	except timeout as e:
		clientSocket.sendto(message.encode(),address)
		clientSocket.settimeout(1)
	else:
		break

data=data.decode()
ack=int(data.split()[1])
message="ACK "+str(seq)+" "+str(ack)
clientSocket.sendto(message.encode(),address)

message="GET "+str(seq)+" "+str(ack)+" "+str(len(sys.argv[3]))+" "+sys.argv[3]
clientSocket.sendto(message.encode(),address)
clientSocket.settimeout(1)
while 1:
	try:
		data,addr=clientSocket.recvfrom(1024)
	except timeout as e:
		message="ACK "+str(seq)+" "+str(ack)
		clientSocket.sendto(message.encode(),address)

		message="GET "+str(seq)+" "+str(ack)+" "+str(len(sys.argv[3]))+" "+sys.argv[3]
		clientSocket.sendto(message.encode(),address)
		clientSocket.settimeout(1)
	else:
		break
#fitst data segment
data=data.decode('utf-8')

payload=""
seq=seq+len(sys.argv[3])

while data.split()[0]!="FIN":
	payload=" ".join(data.split(" ")[4:])
	#deal with payload
	print(payload)
	content=content+payload
	ack=int(data.split()[1])+len(payload)
	message="ACK "+str(seq)+" "+str(ack)
	clientSocket.sendto(message.encode(),address)
	clientSocket.settimeout(1)
	while 1:
		try:
			data,addr=clientSocket.recvfrom(1024)
		except timeout as e:
			clientSocket.sendto(message.encode(),address)
			clientSocket.settimeout(1)
		else:
			break
	data=data.decode('utf-8')

f.write(content)
print(content)
f.close()


 
