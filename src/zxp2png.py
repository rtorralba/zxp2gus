from pathlib import Path
from PIL import Image

def generateSpritesPng(inFile, outFolder):
    # Leer el archivo ZXP
    with open(inFile, 'r') as f:
        lines = f.readlines()

    # Separar las líneas de bits y las líneas de colores
    if len(lines) < 45:
        bit_lines = lines[2:34]
    else:
        bit_lines = lines[2:50]

    # Crear una nueva imagen en escala de grises con el tamaño correcto
    img = Image.new('RGB', (len(bit_lines[0])-1, len(bit_lines)))

    # Definir los colores 'paper' y 'ink' (cambiar estos según sea necesario)
    ink_color = (255, 255, 255)  # Blanco
    paper_color = (0, 0, 0)  # Negro

    # Rellenar la imagen con los datos del archivo ZXP
    for y, line in enumerate(bit_lines):
        for x, pixel in enumerate(line.strip()):
            # Elegir el color basado en el bit
            color = ink_color if pixel == '1' else paper_color
            img.putpixel((x, y), color)

    # Guardar la imagen como PNG
    img.save(str(Path(outFolder + "/sprites.png")))

def generateTilesPng(inFile, outFolder):
        # Leer el archivo ZXP
    with open(inFile, 'r') as f:
        lines = f.readlines()

    # Separar las líneas de bits y las líneas de colores
    bit_lines = lines[2:50]
    # coger el atributo que representa en hexadecimal flash, bright, paper y ink de cada caracter (8x8) de la imagen
    hexAttrs = []
    
    # guardar en color_lineas de la linea 52 a la 57
    color_lines = lines[51:58]

    # convertir cada valor de cada una de esas lineas que estan separados por un espacio de hexadecimal a decimal y guardarlo todo en el array attrs
    for line in color_lines:
        for color in line.strip().split(" "):
            if color:
                hexAttrs.append(int(color, 16))

    # Crear una nueva imagen en escala de grises con el tamaño correcto
    img = Image.new('RGB', (len(bit_lines[0])-1, len(bit_lines)))

    # Definir los colores 'paper' y 'ink' (cambiar estos según sea necesario)
    ink_color = (255, 255, 255)  # Blanco
    paper_color = (0, 0, 0)  # Negro

    # Rellenar la imagen con los datos del archivo ZXP
    for y, line in enumerate(bit_lines):
        for x, pixel in enumerate(line.strip()):
            # calcular en que caracter (8x8 bits) se encuentra el x,y actual
            linea = int(y/8)
            columna = int(x/8)
            celda = linea * 32 + columna

            colorEnHexadecimal = hexAttrs[celda]

            attributeBinary = bin(colorEnHexadecimal)[2:].zfill(8)

            bright = int(attributeBinary[1], 2)
            ink = int(attributeBinary[-3:], 2)
            paper = int(attributeBinary[2:5], 2)
            
            if pixel == '1':
                colorBinary = binaryToZxSpectrumColor(ink, bright)
            else:
                colorBinary = binaryToZxSpectrumColor(paper, bright)

            img.putpixel((x, y), colorBinary)

    # Guardar la imagen como PNG
    img.save(str(Path(outFolder + "/tiles.png")))

def binaryToZxSpectrumColor(colorInt, bright):
    zxSpectrumColorsToRgb = {
        0: ((0, 0, 0), (0, 0, 0)),       # Negro
        1: ((0, 0, 192), (0, 0, 255)),   # Azul
        2: ((192, 0, 0), (255, 0, 0)),   # Rojo
        3: ((192, 0, 192), (255, 0, 255)), # Magenta
        4: ((0, 192, 0), (0, 255, 0)),   # Verde
        5: ((0, 192, 192), (0, 255, 255)), # Cian
        6: ((192, 192, 0), (255, 255, 0)), # Amarillo
        7: ((192, 192, 192), (255, 255, 255)) # Blanco
    }

    return zxSpectrumColorsToRgb[colorInt][bright]