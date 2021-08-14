#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket

serverSocket.bind((sys.argv[1], int(sys.argv[2])))
serverSocket.listen(1)

while True:
    print("Ready to serve...")
    connectionSocket, addr =  serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()               
        filename = message.split()[1]                 
        f = open(filename[1:], "r") 

        outputdata = f.read()                  
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK \r\n\r\n".encode())

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 NOT FOUND \r\n\r\n".encode())

        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data

####
