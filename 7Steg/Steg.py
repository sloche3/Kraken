################################################################################
# Name: Alexis McCarthy 
# Date: 2020 05 08
# Code: Program # 7 Steg - used python 2.7
################################################################################

import binascii
import math
import sys
import argparse
import os

sentinel = '00ff0000ff00'
sentinelHex = binascii.hexlify(sentinel)

sentinelHex = map(''.join, zip(sentinelHex[::2], sentinelHex[1::2]))  

# turns the sentineal, wrapper file and hidden file into
# A list of hexacdemail values for easy extraction
def byteMethodStore(wrapperFileHex, interval, hiddenFileHex, offset):
    o = offset
    i = 0
    while i < len(hiddenFileHex):
        wrapperFileHex[o] = hiddenFileHex[i]
        o += interval
        i += 1

    i = 0
    while i < len(sentinelHex):
        wrapperFileHex[o] = sentinelHex[i]
        o += interval
        i += 1

    return "".join(wrapperFileHex).decode("hex")

# the method in which the file is to be stored based on user input
def bitMethodStore(wrapperFileHex, interval, hiddenFileHex, offset):
    i = offset
    j = 0
    returnString = ""
    ##Hbyte means hidden file byte
    # wByte means wrapper file byte

    # split up storing, so first it will hide the file and then add the sentinel
    while j < len(hiddenFileHex):
        hByte = int(hiddenFileHex[j], 16)
        for k in range(8):
            wByte = int(wrapperFileHex[i], 16)
            wByte &= 11111110
            wByte |= ((hByte & 10000000) >> 7)
            wrapperFileHex[i] = binascii.hexlify('%x' % wByte)
            if (k != 7):
                hByte = hByte << 1
            i += interval
        j += 1

    n = 0
    while n < len(sentinelHex):
        sByte = int(sentinelHex[n], 16)
        for k in range(8):
            wByte = int(wrapperFileHex[i], 16)
            wByte &= 11111110
            wByte |= ((sByte & 10000000) >> 7)
            wrapperFileHex[i] = binascii.hexlify('%x' % wByte)
            if (k != 7):
                sByte = sByte << 1
            i += interval
        n += 1

    returnString += "".join(wrapperFileHex)
    return returnString.decode("hex")

# the mothod in which the file is to be retreaved based on user input
def byteMethodRetreive(wrapperFileHex, interval, offset):
    returnString = ""

    i = offset

    # Since this is a wrapper file hex list, one can just retrive the byte needed at i
    while i < len(wrapperFileHex):
        t = wrapperFileHex[i]
        returnString += chr(t)

        i += interval
    return returnString


def bitMethodRetreive(wrapperFileHex, interval, offset):
    i = offset
    returnString = ""

    try:
        while i < len(wrapperFileHex):
            byte = 00000000
            for k in range(8):
                wByte = wrapperFileHex[i]
                bit = wByte & 00000001
                byte |= bit
                if (k != 7):
                    byte = byte << 1
                i += interval

            returnString += chr(byte)
    except:
        return returnString


    return returnString

# This helps parse the command line
parser = argparse.ArgumentParser(description="Arguments for Steg", add_help=False)
parser.add_argument('-b', '--bit', default=False, action='store_true')
parser.add_argument('-B', '--byte', default=False, action='store_true')
parser.add_argument('-s', '--store', default=False, action='store_true')
parser.add_argument('-r', '--retrieve', default=False, action='store_true')
parser.add_argument('-o', '--offset', type=int)
parser.add_argument('-i', '--interval', type=int)
parser.add_argument('-w', '--wrapperFile', type=str)
parser.add_argument('-h', '--hiddenFile', type=str)
args = parser.parse_args()

# holds all the returned values and outputs the needed infomation
def main():
    # all prompt the user to settup how to store or retrive a hidden file
    if (args.bit == False and args.byte == False) or (args.bit == True and args.byte == True):
        print("please choose either the byte or bit method")
        sys.exit()
    elif (args.store == False and args.retrieve == False) or (args.store == True and args.retrieve == True):
        print("please choose to either store or retrieve a hidden file")
        sys.exit()
    elif (args.offset == None):
        print("Please specify an offset")
        sys.exit()
    elif (args.wrapperFile == None):
        print("Specify a Wrapper File")
        sys.exit()
    elif (args.store == True and args.hiddenFile == None):
        print("In order to store, specify a file to hide")
        sys.exit()

    wrapperFileHex = bytearray(open(args.wrapperFile, "rb").read())
    #wrapperFileHex = map(''.join, zip(wrapperFileHex[::2], wrapperFileHex[1::2]))

    if args.bit == True and args.store == True:
        hiddenFileHex = binascii.hexlify(open(args.hiddenFile, "rb").read())
        hiddenFileHex = map(''.join, zip(hiddenFileHex[::2], hiddenFileHex[1::2]))
        if (args.interval == None):
            interval = 1
        else:
            interval = args.interval
        return (bitMethodStore(wrapperFileHex, interval, hiddenFileHex, args.offset))

    if args.bit == True and args.retrieve == True:
        if (args.interval == None):
            interval = 1
        else:
            interval = args.interval

        returnString =(bitMethodRetreive(wrapperFileHex, interval, args.offset))
        indexOfSentinel = returnString.find(sentinel.decode("hex"))
        if (indexOfSentinel != -1):
            return returnString[:indexOfSentinel]
        return "Did not find"

    if args.byte == True and args.store == True:
        hiddenFileHex = binascii.hexlify(open(args.hiddenFile, "rb").read())
        hiddenFileHex = map(''.join, zip(hiddenFileHex[::2], hiddenFileHex[1::2]))
        if (args.interval == None):
            interval = math.floor((len(wrapperFileHex) - args.offset) / (len(hiddenFileHex) + 6))
        else:
            interval = args.interval
        return (byteMethodStore(wrapperFileHex, interval, hiddenFileHex, args.offset))

    if args.byte == True and args.retrieve == True:
        returnString = (byteMethodRetreive(wrapperFileHex, args.interval, args.offset))
        indexOfSentinel = returnString.find(sentinel.decode("hex"))
        if (indexOfSentinel != -1):
            return returnString[:indexOfSentinel]
        return "Did not find"

# wrapperFile = open("stegged-bit.bmp", "rb")
# wrapperFileSize = os.stat("stegged-bit.bmp")
print main()
# hexlist = map(''.join,zip(hexdata[::2],hexdata[1::2]))
# sys.stdout.write(byteMethodRetreive(hexlist, 8, 1024, wrapperFileSize.st_size))
