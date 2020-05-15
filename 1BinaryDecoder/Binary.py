##############################################
# Cody Holland
# 03/26/2020
# CSC 442 Gourd 
# Program 1 Binary Decoder 
# Python 2

# How to run: python Binary.py < binary.txt
# pdf: https://www.jeangourd.com/classes/csc442/assignments/Program1/01.pdf
##############################################

from sys import stdin

#turns binary in ASCII characters
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

binary = stdin.read().rstrip("\n")

# for seven bit binary 
if(len(binary)%7 == 0):
    print "7-bit:"
    print(decode(binary, 7))

# for eight bit binary
if(len(binary)%8 ==0):
    print "8-bit:"
    print(decode(binary, 8))

