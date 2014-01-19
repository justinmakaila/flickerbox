#!/usr/bin/env/python
import sys

from optparse import OptionParser
from extract import *
from encode import *

extract = extract()
encode = encode()

# Main function called to begin execution
def main(options):
    if options.extract is True:
        if extract.extractFile(options.inputFile) != -1:
            exit("Extracting complete!")
        else:
            exit("Error upon extraction")
    else:
        encode.encodeFile(options.inputFile, options.metaFile, options.gifFile, options.outputFile)
        exit("Encoding complete!")

# Exits the program
def fail(message):
    if message is not None:
        print message

    sys.exit()

parser = OptionParser()
parser.add_option("-e", "--encode", action="store_false", dest="extract", default=False, help="Flag set to encode the input file into destination")
parser.add_option("-g", "--gif", dest="gifFile", metavar="GIF", help="The gif to encode into")
parser.add_option("-i", "--input", dest="inputFile", metavar="INFILE", help="The file to use as input, either to encode or extract")
parser.add_option("-m", "--meta", dest="metaFile", metavar="META", help="The meta file to be encoded with the input file")
parser.add_option("-o", "--output", dest="outputFile", metavar="OUTFILE", help="The file to output to")
parser.add_option("-x", "--extract", action="store_true", dest="extract", default=True, help="Flag set to extract the file")

(options, args) = parser.parse_args()

main(options)