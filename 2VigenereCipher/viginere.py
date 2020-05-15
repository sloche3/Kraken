#!/usr/bin/env python2
#python2
import sys

#./vigenere -e MyKeY

alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


'''
Takes a key and decrypts text from stdin
'''
def dec(key):
	try:
		while(True):
			plainOut= []
			stripKey = key.replace(" ","")
			keyInd = 0
			cipIn = raw_input()

			for item in cipIn:

				if keyInd >= len(stripKey): #cycle through the key
					keyInd = 0

				if item.lower() not in alph: #appends special characters and numbers
					plainOut.append(item)
				else:
					if ord(item) > ord(item.upper()): #lower case
						plainOut.append(alph[(26 + (alph.index(item) - alph.index(stripKey[keyInd].lower()))) % 26])
					else:
						plainOut.append(alph[(26 + (alph.index(item.lower()) - alph.index(stripKey[keyInd].lower()))) % 26].upper())
					keyInd += 1

			print ''.join(plainOut)

	except (KeyboardInterrupt, SystemExit, EOFError): #Prevents python error from showing in stdout when doing ^c or ^d
		print(" ")
		sys.exit()

'''
Takes a key and encrypts text from stdin
'''
def enc(key):
	try:
		while(True):
			cipOut= []
			stripKey = key.replace(" ", "")
			keyInd = 0
			plain = raw_input()

			for item in plain:

				if keyInd >= len(stripKey): #cycle through key
					keyInd = 0

				if item.lower() not in alph: #appends special characters
					cipOut.append(item)
				else:
					if ord(item) > ord(item.upper()): #lower case
						cipOut.append(alph[(alph.index(item) + alph.index(stripKey[keyInd].lower())) % 26])
					else:
						cipOut.append(alph[(alph.index(item.lower()) + alph.index(stripKey[keyInd].lower())) % 26].upper())
					keyInd += 1

			print ''.join(cipOut)

	except (KeyboardInterrupt, SystemExit, EOFError): #Prevents python error from showing in stdout when doing ^c or ^d
		print(" ")
		sys.exit()



#______main_________________

if sys.argv[1] == '-e':
	enc(sys.argv[2])
elif sys.argv[1] == '-d':
	dec(sys.argv[2])
else:
	print("Use flag -d to decrypt and -e to encrypt")
