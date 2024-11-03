import argparse
import sys
import os.path
import cv2
import numpy

from . import zxlib

def validateArguments(argv):
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('-t', '--itype', type=str, help='Type of input')
    parser.add_argument('-i', '--input', type=str, help='Input file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-f', '--format', type=str, help='Format of the output')

    args = parser.parse_args(argv)

    result = {
        "type": args.itype,
        "input": args.input,
        "output": args.output,
        "format": args.format
    }

    return result

def getTiles(inFile, tileWidth, tileHeight):
    if not os.path.isfile(inFile):
        print("File '{}' does not exist. Exiting.".format(inFile))
        sys.exit(2)
    img = cv2.imread(inFile)
    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    imgHeight = rgbImg.shape[0]
    imgWidth = rgbImg.shape[1]

    tiles = []

    palettizedArray = numpy.full((imgHeight, imgWidth), 0)

    for y in range(imgHeight):
        for x in range(imgWidth):
            palettizedArray[y][x] = zxlib.getPaletteColor(rgbImg[y,x])

    for y in range(0, imgHeight, tileHeight):
        tiles.append([])
        for x in range(0, imgWidth, tileWidth):
            tiles[len(tiles) - 1].append(palettizedArray[y:y+tileHeight, x:x+tileWidth])

    return tiles