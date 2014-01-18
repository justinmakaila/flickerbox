import json
import re
import sys
from optparse import OptionParser

delimeterRegex = '!\*{3}!'
delimeterString = '!***!'

'''
Updated meta object

{
  "_meta": {
    "version": 8,
    "nextImageId": 9
  },

  "_root": {
    "photos": {
      "cat.jpg": ["1", "2", "3"],
      "horse.png": "4",
      "dolphin.gif": "5"
    },
    "projects": {
      "api": {
        "app.js": "6",
        ".gitignore": "7",
        ".git": {
          "index": "8"
        }
      }
    }
  }
}
'''

fileNameKey = 'fileName'
sizeKey = 'size'
chunksKey = 'chunks'

# Main function called to begin execution
def main(options):
    if options.extract is True:
        extractFile(options.inputFile)
    else:
        encodeFile(options.inputFile, options.metaFile, options.gifFile, options.outputFile)

# Encodes input file, preceeded by meta file into the source GIF,
# withou the output being saved to output file
def encodeFile(inputFile, metaFile, sourceGif, outputFile):
    print "Encoding " + inputFile + " and " + metaFile + " into " + sourceGif + ". Outputting to " + outputFile
    print

    filenames = [sourceGif, metaFile, inputFile]
    with open(outputFile, 'w') as outfile:
        for i in range(0, 3):
            # Write the delimeter before and after the meta
            if i == 1 or i == 2:
                outfile.write(delimeterString)

            with open(filenames[i]) as infile:
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

        print "Saving a file named", jsonDict[fileNameKey], "of length", jsonDict[sizeKey], "starting at index", startLocation

        fileStart = startLocation + len(delimeterString)
        f.seek(fileStart, 0)

        outfileContents = f.read(jsonDict[sizeKey])

        out = open(jsonDict[fileNameKey], 'w+')
        out.write(outfileContents)

        out.close()
        f.close()

    exit("Extraction complete!")

# Extracts the JSON data hidden in the string, representing file contents
def getJSON(string):
    regexString = '(?<=' + delimeterRegex + ')\{.*\}(?=' + delimeterRegex + ')'
    regex = re.compile(regexString, re.DOTALL)
    results = regex.findall(string)

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

# flickrbox.py -e -i hiddenFile.txt -m meta.json -g ballin.gif -o output.gif
# flickrbox.py -x -i output.gif

(options, args) = parser.parse_args()

main(options)