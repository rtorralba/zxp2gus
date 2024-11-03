import os
from pathlib import Path

def prepareTiles(tiles):  
    result = []
    mirroredTiles = []
    counter = 0
    for i in range(0, 16):
        result.append(tiles[counter])
        counter += 1

    for i in range(16, 32):
        result.append(tiles[i])
        counter += 1
        if counter % 2 == 0:
            tile = tiles[i - 1]
            tile0HorizontalFlip = reorderArray([flip_byte(b) for b in tile])
            mirroredTiles.append(tile0HorizontalFlip)
            counter += 1

            tile = tiles[i]
            tile0HorizontalFlip = reorderArray([flip_byte(b) for b in tile])
            mirroredTiles.append(tile0HorizontalFlip)
            counter += 1
    
    result += mirroredTiles
    return result

def prepareTilesWithOutMirror(tiles):
    result = []
    counter = 0
    for i in range(0, 48):
        result.append(tiles[counter])
        counter += 1

    return result
    

def getSpritesBas(tiles, outFolder):
    if len(tiles) == 32:
        tiles = prepareTiles(tiles)
    else:
        tiles = prepareTilesWithOutMirror(tiles)

    with open(str(Path(outFolder + "/sprites.bin")), "wb") as f:
        for tile in tiles:
            f.write(bytearray(tile))

def flip_byte(b):
    return int('{:08b}'.format(b)[::-1], 2)

def reorderArray(sprite):
    return [sprite[16], sprite[17], sprite[18], sprite[19], sprite[20], sprite[21], sprite[22], sprite[23], sprite[24], sprite[25], sprite[26], sprite[27], sprite[28], sprite[29], sprite[30], sprite[31], sprite[0], sprite[1], sprite[2], sprite[3], sprite[4], sprite[5], sprite[6], sprite[7], sprite[8], sprite[9], sprite[10], sprite[11], sprite[12], sprite[13], sprite[14], sprite[15]]

def flipTile(tile):
    return [flip_byte(b) for b in tile]

# funcion para voltear un tile de 8x8 verticalmente
def flipTileVertical(tile):
    return tile[::-1]

# funcion para rotar un tile de 8x8 90 grados
def rotateTile90g(tile):
    rotated_tile = [0] * 8
    for i in range(8):
        for j in range(8):
            if tile[j] & (1 << i):
                rotated_tile[i] |= (1 << (7 - j))
    return rotated_tile

def getTilesBas(inFile, outFolder):
    with open(inFile, 'r') as f:
        lines = f.readlines()

    lines = lines[2:]

    # Separar las líneas de bits y las líneas de colores
    bit_lines = lines[:48]

    tiles = []
    # convertir el array de bits en tiles de 8x8 de spectrum
    for i in range(0, 48, 8):
        for j in range(0, 256, 8):
            tile = []
            for k in range(8):
                tile.append(int(bit_lines[i + k][j:j + 8], 2))
            tiles.append(tile)
    
    #setear el primer tile a 0s
    tiles[0] = [0] * 8

    # Guardar tiles en fichero bin para cargarlo desde basic
    with open(str(Path(outFolder + "/tiles.bin")), "wb+") as f:
        for tile in tiles:
            f.write(bytearray(tile))

        # voltear horizontalmente el segundo tile
        tile = tiles[1]
        tile0HorizontalFlip = flipTile(tile)

        f.write(bytearray(tile0HorizontalFlip))

        # girar 90 grados el segundo tile
        tile0Rotate90 = rotateTile90g(tile)
        f.write(bytearray(tile0Rotate90))

        # voltear verticalmente el tile rotado 90 grados
        tile0Rotate90VerticalFlip = flipTileVertical(tile0Rotate90)
        f.write(bytearray(tile0Rotate90VerticalFlip))

    attrs = []
    
    # guardar en color_lineas de la linea 52 a la 57
    color_lines = lines[49:56]

    # convertir cada valor de cada una de esas lineas que estan separados por un espacio de hexadecimal a decimal y guardarlo todo en el array attrs
    for line in color_lines:
        for color in line.strip().split(" "):
            if color:
                attrs.append(int(color, 16))
            
    # Guardar array de enteros de una dimension attrs en fichero binario para cargarlo desde basic
    attrs = [int(attr) for attr in attrs]

    with open(str(Path(outFolder + "/attrs.bin")), "wb+") as f:
        for attr in attrs:
            f.write(attr.to_bytes(1, byteorder='big'))