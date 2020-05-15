#############################################################################
# Cody Holland
# CSC 442 Cyber Security
# Program 3 Covert Channel FTP Message
# 3/30/20

# Python 2
# How to run: change the globals (IP, PORT, FOLDER, and METHOD) to a vaild ftp server. Then run 'python fetch.py' on any other machine.
# fetches files from an FTP server and decodes the 7-bit or 10-bit covert message as specified from the pdfs
# pdf https://www.jeangourd.com/classes/csc442/assignments/Program3/03.pdf
# pdf https://www.jeangourd.com/classes/csc442/notes/04b.pdf

#############################################################################
from ftplib import FTP

# FTP method (7 or 10)
METHOD=7

# Globals (FTP specifics)
IP="192.168.0.0"
PORT=21
FOLDER="covert/7"

# file/folder contents
content=[]

# connect to FTP server and fetch file listing (using specific IP, PORT, and FOLDER)
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login()                             # user login anonymously
ftp.cwd(FOLDER)                         # cwd to folder we want
ftp.dir(content.append)                 # list directories
ftp.quit()                              # disconnect 

# Binary decoder function (7-bit or 8-bit)
def decode(binary, n):
    text =""
    i = 0
    while(i<len(binary)):
        byte = binary[i:i+n]
        byte = int(byte, 2)
        #detect backspace
        if(byte == 8 and len(text) > 0):
            # truncate the last char
            text = text[0:len(text)-1]
        else:
            text += chr(byte)
        i += n
    return text

# iterate through the folder's content, add just the permisions (drwxrwxrwx) to perms
perms=[]
for i in content:
    perms.append(i[:10])

# put all permissions that we will be decoded into a string, depending on the method
permString=""
if(METHOD == 7):
    for i in perms:
        # if one of the first 3 perms is occupied (drw), skip it
        if(i[0] != "-" or i[1] != "-" or i[2] != "-"):
            continue
        # track only these bits, and only the last 7 of them (disregard the first 3).
        else:
            permString += i[3:10]

elif(METHOD == 10):
    for i in perms:
        permString += i

# change from permissions (drwx or -) to bits (1 or 0).
bits=""
for i in permString:
    if(i == "-"):
        bits += "0"
    else:
        bits += "1"

# always output 7-bit format regardless of METHOD
if(METHOD == 7 or METHOD == 10):
    message = decode(bits, 7)
    print message

# also output 8-bit format for METHOD 10 (only one should be readable though).
if(METHOD == 10):
    message = decode(bits, 8)
    print message

