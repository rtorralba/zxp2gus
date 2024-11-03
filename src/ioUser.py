import sys, getopt
import os.path
import cv2
import numpy

import zxlib

def printHelp():
    print("Usage: img2zxbasic.py -t <tiles/sprites> -i <inputfile> -o <outputfolder> -f <format>")
    print("Formats: png, bin")

def validateArguments(argv):
    result = {}
    try:
        options = getopt.getopt(argv, "?t:i:o:f:", ["help", "itype=", "input=", "output=", "format="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    for arg, val in options[0]:
        if arg in ("-?", "--help"):
            printHelp()
            sys.exit()
        elif arg in ("-t", "--itype"):
            result["type"] = val
        elif arg in ("-i", "--input"):
            result["input"] = val
        elif arg in ("-o", "--output"):
            result["output"] = val
        elif arg in ("-f", "--format"):
            result["format"] = val
        else:
            print("Unrecognized argument '{}' with value '{}'".format(arg, val))

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