# Name: Solomon Loche
# Date: 4/20/2020
# Description: Chat (Timing) Covert Channel - Server

import socket
import time
#from time import sleep
from binascii import hexlify

# CONSTANTS
ZERO = 0.025
ONE = 0.1

# set the port for client connections
port = 1338

# create the socket and bind it to the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))

# listen for clients
# this is a blocking call
s.listen(0)

# a client has connected!
c, addr = s.accept()

# let's see what happens..
covert = "secret" + "EOF"
covert_bin = ""
for i in covert:
	# convert each character to a full byte
		# hexlify converts ASCII to hex
		# int converts the hex to a decimal integer
		# bin provides its binary representation (with a 0b
		# prefix that must be removed)
		# that's the [2:] (return the string from the third
		# character on)
		# zfill left-pads the bit string with 0s to ensure a
		# full byte
	covert_bin += bin(int(hexlify(i), 16))[2:].zfill(8)

# set the message
msg = "Some message is going to be displayed somewhere around here............................\n"
#msg = "Some message.............\n"

# send the message, one letter at a time
n = 0
for i in msg:
	c.send(i)
	if (covert_bin[n] == "0"):
		time.sleep(ZERO)
	else:
		time.sleep(ONE)
	n = (n + 1) % len(covert_bin)

# send EOF and close the connection to the client
c.send("EOF")
c.close()
