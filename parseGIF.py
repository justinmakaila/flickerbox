import json
import re

gifTerminator = b'\x3b'
delimeter = b'\x21\x2a\x2a\x2a\x21\x0a'
print "Terminator:", gifTerminator
print "Delimeter:", delimeter

with open("test.gif", "rb") as f:
	regex = re.search("!*{3}!", f.read())
	print regex

	'''
	byte = f.read(1)

	while byte != "":
		if byte == ';':
			delimeter = f.read(6)
			if delimeter.encode("hex") == '212a2a2a210a':
				print "I found the delimeter! Parsing for JSON meta!"
				jsonString = str(f.read(1))

		byte = f.read(1)
	'''