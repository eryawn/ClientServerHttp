# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket 

????????????

# Assign IP address and port number to socket

?????????????

while True:
	
	# Receive the client packet along with the address it is coming from 
	???????

	# Generate random number in the range of 1 to 10 and if rand is less is than 4, we consider the packet lost and tell the client to retransmit
	rand = random.randint(1, 10)    
	if rand < 4:

		continue
	
	# Capitalize the message from the client and send the capilized version to the client
	?????
