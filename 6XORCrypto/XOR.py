#python verion 3
from sys import stdin, stdout

#Grabs data from key file
with open ("key", "r+b") as f:
	key_file = f.read()

final = bytearray()
x = stdin.buffer.read().rstrip()
x = bytearray(x)

#XOR Conversion
for count in range(len(x)):
	keyLen = count % (len(key_file))
	XOR1 = x[count]
	XOR2 = key_file[keyLen]
	z = XOR1 ^ XOR2
	final.append(z)

stdout.buffer.write(final)

