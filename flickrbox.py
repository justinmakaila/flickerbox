#!/usr/bin/env/python
import json
import re
import sys
import fileinput
from optparse import OptionParser

delimeterRegex = '!\*{3}!'
delimeterString = '!***!'

fileNameKey = 'fileName'

# Main function called to begin execution
def main(options):
    if options.extract is True:
        extractFile(options.inputFile)
    else:
        metaFile = open(options.metaFile, 'r') if options.metaFile != '-' else sys.stdin
        encodeFile(open(options.inputFile, 'r'), metaFile, open(options.gifFile, 'r'), options.outputFile)

# Encodes input file, preceeded by meta file into the source GIF,
# withou the output being saved to output file
def encodeFile(inputFile, metaFile, sourceGif, outputFile):
    files = [sourceGif, metaFile, inputFile]
    with open(outputFile, 'w') as outfile:
        for i in range(0, 3):
            # Write the delimeter before and after the meta
            if i == 1 or i == 2:
                outfile.write(delimeterString)

            infile = files[i]

            outfile.write(infile.read())
            infile.close()

        outfile.close()

    exit("Encoding complete!")

# Extracts the hidden data from input file
def extractFile(inputFile):
    print "Extracting " + inputFile
    print

    with open(inputFile, "rb") as f:
        fileContents = f.read()
        jsonDict, startLocation = getJSON(fileContents)

        print "Extracting a file named", jsonDict[fileNameKey], "starting at index", startLocation

        # Seek to the file start
        fileStart = startLocation + len(delimeterString)
        f.seek(fileStart, 0)

        # Read to the end of the file
        outfileContents = f.read()

        # Output the read contents
        out = open(jsonDict[fileNameKey], 'w+')
        out.write(outfileContents)

        # Close the files
        out.close()
        f.close()

    exit("Extraction complete!")

# Extracts the JSON data hidden in the string, representing file contents
def getJSON(string):
    # Get the Regex matches
    regexString = '(?<=' + delimeterRegex + ')\{.*\}(?=' + delimeterRegex + ')'
    regex = re.compile(regexString, re.DOTALL)
    results = regex.findall(string)

    # If something came back, return a new JSON dictionary and the length of the file
    # else, fail with an error message
    if len(results) is not 0:
        match = results[0]

        startIndex = string.index(match)
        resultsLength = len(match) + startIndex

        jsonString = ''.join(match.split())
        jsonDict = json.loads(jsonString)

        return jsonDict, resultsLength
    else:
        fail("No JSON found")

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