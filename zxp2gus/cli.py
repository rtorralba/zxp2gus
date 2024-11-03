#!/usr/bin/env python3

import sys
import numpy
import tempfile

from . import ioUser
from . import zxbasic
from . import zxp2png

def generateCodedSprites(tile, inkColors, tileHeight, tileWidth, pValues):
    row = []
    for y in range(tileHeight):
        cx = 0
        cy = int(y/8)
        for x in range(0, tileWidth, 8):
            byteValue = 0
            for offsetX in range(8):
                byteValue = byteValue << 1
                pixColor = tile[y,x+offsetX]
                if(pixColor != pValues[cy,cx]):
                    byteValue = byteValue | 1
                    if inkColors[cy,cx] == -1:
                        inkColors[cy,cx] = pixColor
            row.append(byteValue)
            cx = cx + 1
    result = [row[0], row[2], row[4], row[6], row[8], row[10], row[12], row[14],
            row[16], row[18], row[20], row[22], row[24], row[26], row[28], row[30],
            row[1], row[3], row[5], row[7], row[9], row[11], row[13], row[15],
            row[17], row[19], row[21], row[23], row[25], row[27], row[29], row[31]]
    return result


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        args = ioUser.validateArguments(argv)
        type = args["type"]
        inFile = args["input"]
        outFolder = args["output"]
        format = args["format"]
        
        if type == "sprites":
            if format == "png":
                zxp2png.generateSpritesPng(inFile, outFolder)
            else:
                th = 16
                tw = 16

                tempDir = tempfile.gettempdir()
                spritesFile = tempDir + "/sprites.png"
                zxp2png.generateSpritesPng(inFile, tempDir)

                sprites = ioUser.getTiles(spritesFile, tw, th)

                codedSprites = []

                paperValues = numpy.array([[0]*32 for _ in range(6)])
                inkColors = numpy.full(paperValues.shape, -1)
                tileIdx = 0
                for tileY in range(len(sprites)):
                    for tileX in range(len(sprites[tileY])):
                        codedSprites.append(generateCodedSprites(sprites[tileY][tileX], inkColors, 16, 16, paperValues))
                        
                        tileIdx = tileIdx + 1    
                zxbasic.getSpritesBas(codedSprites, outFolder)
        else:
            if format == "png":
                zxp2png.generateTilesPng(inFile, outFolder)
            else:
                zxbasic.getTilesBas(inFile, outFolder)
    except Exception as e:
        print(f"Error: {e}")
        ioUser.validateArguments(['-h'])

if __name__ == "__main__":
   main(sys.argv[1:])
