#import socket module
from socket import *
import sys # In order to terminate the program

c = socket(AF_INET, SOCK_STREAM)
c.connect((sys.argv[1], int(sys.argv[2])))
c.send(("GET /" + sys.argv[3] + " HTTP/1.1\r\n\r\n").encode())
d = c.recv(1024)
out = ""
while d:
    out += d.decode()
    d = c.recv(1024)
    
print(out)
c.close()

####