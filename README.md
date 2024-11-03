# zxp2gus

Simple command to convert ZX Paintbrush Images (zxp) into basic file for [Boriel's ZX Basic](https://zxbasic.readthedocs.io/en/docs/) and [GuSprites](https://github.com/gusmanb/GuSprites) sprite library

## Install

pip install zxp2gus

## Run

```bash
usage: zxp2gus [-h] [-t ITYPE] [-i INPUT] [-o OUTPUT_FOLDER] [-f FORMAT]

Process some arguments.

options:
  -h, --help            show this help message and exit
  -t ITYPE, --itype ITYPE
                        Type of input
  -i INPUT, --input INPUT
                        Input file
  -o OUTPUT_FOLDER, --output OUTPUT
                        Output file
  -f FORMAT, --format FORMAT
                        Format of the output
```

You can convert zxp of type tiles or sprites to bin form import into ZX Basic program or PNG to use it in other programas like Tiled for example

### Examples:

#### Bin

```bash
zxp2gus -t tiles -i assets/map/tiles.zxp -o output -f bin
```

```bash
zxp2gus -t sprites -i assets/map/sprites.zxp -o output -f bin
```

### PNG

```bash
zxp2gus -t tiles -i assets/map/tiles.zxp -o assets/map/ -f png
```

```bash
zxp2gus -t sprites -i assets/map/sprites.zxp -o assets/map/ -f png
```