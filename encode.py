import os
import sys
import json
import fileinput

delimeterString = '!***!'
MAX_FILE_SIZE = 209715200.0

class encode:
    # Encodes input file, preceeded by meta file into the source GIF,
    # without the output being saved to output file
    def encodeFile(self, inputFile, metaFile, sourceGif, outputFile):
        parts = self.getFileParts(inputFile, sourceGif)
        print "Encoding into", parts, "part(s)"

        work = self.generateWorkArray(sourceGif, inputFile, outputFile, parts)

        # If it's the first chunk, write source, delimeter, meta, delimeter, data
        # Else, write gif, delimeter, data
        for i in range(0, parts):
            outfileName = self.getOutFilename(outputFile, i)
            print "Writing part", i, "to", outfileName
            workDictionary = work[i]

            source = workDictionary["source"]
            chunk = workDictionary["chunk"]

            with open(outfileName, 'w') as outfile:
                outfile.write(source.read())
                source.seek(0)

                if "meta" in workDictionary:
                    outfile.write(delimeterString)
                    outfile.write(workDictionary["meta"])

                outfile.write(delimeterString)

                outfile.write(chunk.read())

                if chunk.name.split('.')[1] == 'bin':
                    self.cleanup(chunk)

                outfile.close()

    # Calculates the number of parts to split inputFile into
    def getFileParts(self, inputFile, gif):
        gifHandle = os.stat(gif)
        inputHandle = os.stat(inputFile)

        gifSize = gifHandle.st_size
        inputSize = inputHandle.st_size
        fileSize = gifSize + inputSize

        print "GIF of size", gifSize
        print "Input of size", inputSize
        print "Total file size:", fileSize
        
        parts = (fileSize / MAX_FILE_SIZE)
        if parts > int(parts):
            return int(parts + 1)
        elif parts > 1:
            return int(parts)
        else:
            return 1

    # Splits the input file into parts. Returns an array of file chunks and meta data to represent them
    def splitFile(self, inputFile, gifFile, parts):
        inputHandle = os.stat(inputFile)
        inputSize = inputHandle.st_size

        chunkSize = (inputSize / parts)
        print "Splitting file of size", inputSize, "into", parts, "parts,", chunkSize, "each"

        chunks = []
        position = 0
        index = 0
        # Open the file
        with open(inputFile, 'rb') as sourceFile:
            for i in range(0, parts):
                print i
                sourceFile.seek(position)
                outfilename = self.getOutFilename("chunk.bin", i)
                print "Splitting", outfilename

                with open(outfilename, 'wb') as outfile:
                    print i == parts - 1
                    fileContents = sourceFile.read(chunkSize) if i != (parts - 1) else sourceFile.read()

                    outfile.write(fileContents)
                    outfile.close()

                    chunks.append(outfilename)

                position += chunkSize

        return chunks

    def getOutFilename(self, filename, part):
        outfileName = filename.split('.')
        return outfileName[0] + str(part) + '.' + outfileName[1]

    def generateMetaJSON(self, filename, outputName, chunks=None):
        print "Generating meta JSON:"
        jsonString = '{"filename":' + "\"" + filename + "\""

        if chunks is not None:
            jsonString += ', "chunks": ['
            for i in range(1, len(chunks)):
                chunkName = self.getOutFilename(outputName, i)
                print chunkName

                if i == len(chunks) - 1:
                    jsonString += "\"" + chunkName + "\"" + ']'
                else:
                    jsonString += "\"" + chunkName + "\"" + ','

        jsonString  += '}'

        print jsonString
        return jsonString

    def generateWorkArray(self, sourceGif, inputFile, outputFile, partsCount):
        work = []
        sourceFile = open(sourceGif, 'r')

        if partsCount > 1:
            chunks = self.splitFile(inputFile, sourceGif, partsCount)
            metaJSON = self.generateMetaJSON(inputFile, outputFile, chunks)

            for i in range(0, len(chunks)):
                chunk = chunks[i]
                chunkFile = open(chunk, 'rb')

                if i == 0:
                    files = { "source": sourceFile, "meta": metaJSON, "chunk": chunkFile }
                else:
                    files = { "source": sourceFile, "chunk": chunkFile }

                work.append(files)
        else:
            metaJSON = self.generateMetaJSON(inputFile, outputFile, None)

            files = { "source": sourceFile, "meta": metaJSON, "chunk": open(inputFile, 'r') }

            work.append(files)

        return work

    # Closes the open file and removes it
    def cleanup(self, openFile):
        openFile.close()
        os.remove(openFile.name)