# Name: Solomon Loche
# Date: 4/20/2020
# Description: Chat (Timing) Covert Channel

import socket
from sys import stdout
from time import time
from binascii import unhexlify

# CONSTANTS
ZERO = 0.025
ONE = 0.1

# enables debugging output
DEBUG = False

# set the server's IP address and port
ip = "138.47.102.67"
port = 21

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

# receive data until EOF
covert_bin = ""
data = s.recv(4096)
while (data.rstrip("\n") != "EOF"):
	# output the data
	stdout.write(data)
	stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096)
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	if (delta >= ONE):
		covert_bin += "1"
	else:
		covert_bin += "0"
	if (DEBUG):
		stdout.write(" {}\n".format(delta))
		stdout.flush()

# close the connection to the server
s.close()

# decode the binary string
covert = ""
i = 0
while (i < len(covert_bin)):
	# process one byte at a time
	b = covert_bin[i:i + 8]
	# convert it to ASCII
	n = int("0b{}".format(b), 2)
	try:
		covert += unhexlify("{0:x}".format(n))
	except TypeError:
		covert += "?"
	# stop at the string "EOF"
	if (covert[len(covert)-3:] == "EOF"):
		break
	# go to the next 8 bits
	i += 8

# outout the covert message
stdout.write("Covert message: {}\n".format(covert))
