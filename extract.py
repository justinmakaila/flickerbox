import re
import json

delimeterString = '!***!'

metaDataRegex = '(?<=!\*{3}!)\{.*\}(?=!\*{3}!)'
chunkDataRegex = '(?<=;!\*{3}!).*'

class extract:
    def __init__(self):
        self.chunks = None
        self.outfile = None

    def extractFile(self, inputFile):
        print "Extracting " + inputFile + '\n'

        with open(inputFile, "rb") as f:
            jsonDict, startLocation = self.extractMeta(f.read())

            self.outfile = open(jsonDict["filename"], 'w')

            self.logExtractInfo(startLocation, jsonDict, inputFile)

            fileStart = startLocation + len(delimeterString)
            outfileContents = self.readToEnd(f, fileStart)
            self.outfile.write(outfileContents)

        if self.chunks is not None:
            for chunk in self.chunks:
                with open(chunk, 'rb') as f:
                    startLocation = self.extractChunk(f.read())
                    fileStart = startLocation + len(delimeterString)
                    chunkBuffer = self.readToEnd(f, fileStart)
                    self.outfile.write(chunkBuffer)
                    f.close()

    def extractMeta(self, fileContents):
        matches = self.findMatches(metaDataRegex, fileContents)

        if len(matches) is not 0:
            match = matches[0]

            startIndex = fileContents.index(match)
            resultsLength = len(match) + startIndex

            jsonString = ''.join(match.split())
            jsonDict = json.loads(jsonString)

            return jsonDict, resultsLength
        else:
            return -1

    def readToEnd(self, f, startLocation):
        f.seek(startLocation, 0)
        return f.read()

    def extractChunk(self, fileContents):
        matches = self.findMatches(chunkDataRegex, fileContents)

        if len(matches) is not 0:
            match = matches[0]

            startIndex = fileContents.index(match)
            resultsLength = len(match) + startIndex

            return startIndex


    def findMatches(self, regex, searchString):
        regex = re.compile(regex, re.DOTALL)
        results = regex.findall(searchString)
        return results

    def logExtractInfo(self, startLocation, dictionary, inputFile):
        extractInfo = "Extracting a file named " + dictionary["filename"] + " starting at index " + str(startLocation) + ' in file ' + inputFile + '. '

        if "chunks" in dictionary:
            extractInfo += "Files located at:"
            self.chunks = dictionary["chunks"]
            for i in dictionary["chunks"]:
                extractInfo += '\n\t' + i

        print extractInfo