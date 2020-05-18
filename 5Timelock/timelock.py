#python version 2.7.17

#imports
from sys import stdin, stdout
from datetime import datetime
import pytz
from hashlib import md5

#debug mode
DEBUG = False
MANUAL_DATETIME = ""

#Stuff for cyberstorm
#ON_SERVER = F
#INTERVAL = 60

#epoch = stdin.read().rstrip("\n")
epoch = ""
if epoch == "":
    epoch = (datetime.utcnow()).strftime('%Y %m %d %H %M %S')
ld = ""
for x in range(1, 3):
	ld += epoch[-x]
	ld = ld[::-1]

#helper functions
def utc_convert(dt):
	native = datetime.strptime(dt, "%Y %m %d %H %M %S")
	local_timezone = pytz.timezone("America/Chicago")
	localize = local_timezone.localize(native, is_dst=None)
	utc_datetime = localize.astimezone(pytz.utc)
	return utc_datetime

def hash(data):
	encode = data.encode()
	hash = md5(encode)
	result = hash.hexdigest()
	return result

#converts to UTC
if (DEBUG):
	current_datetime = utc_convert(MANUAL_DATETIME)
else:
	current_datetime = datetime.now().strftime("%Y %m %d %H %M %S")
	current_datetime = utc_convert(current_datetime)
epoch = utc_convert(epoch)

#convert to seconds
seconds = int((current_datetime-epoch).total_seconds())
seconds = str(seconds)

#rolls back to last 60 second interval
cdstr = str(current_datetime)
cdld = ""
for x in range(7,9):
	cdld += cdstr[-x]
cdld = cdld[::-1]
ld = int(ld)
cdld = int(cdld)
if (cdld < ld):
	time = ((ld-cdld)*-1)-2
else:
	time = (ld-cdld)
seconds2 = (int((current_datetime-epoch).total_seconds())+time)
seconds2 = str(seconds2)

#Hashes the total seconds
md51 = hash(seconds2)
md52 = hash(md51)
print md52

#Creates code
code = ""
check = 0
for x in range(len(md52)):
	if(check < 2):
		char = md52[x]
		if (char.isalpha() == True):
			code += char
			check += 1

for x in range(len(md52)-1, 0, -1):
	if (check < 4):
		num = md52[x]
		if (num.isdigit() == True):
			code += num
			check += 1
code += md52[(len(md52)/2)]

#debug statements
if (DEBUG):
	print "Current (UTC): {}".format(current_datetime)
	print "Epoch (UTC): {}".format(epoch)
	print "Seconds: {}".format(seconds)
	print "Seconds: {}".format(seconds2)
	print "MD5 1: {}".format(md51)
	print "MD5 2: {}".format(md52)

#final code
code = code[:len(code)-1]
code += md52[len(md52)-1]
stdout.write(code + "\n")
