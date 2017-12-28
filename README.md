# Inkscape extension
Add files to inkscapes extensions folder. Please follow instructions on inkscape website.

Dependencies:
* [skimage](http://scikit-image.org/)


# image2halftoneDXF.py
Command line tool for converting images to halftone DXF for laser cutting or CNC milling etc.

Dependencies:
* [dxfwrite](http://pythonhosted.org/dxfwrite/index.html)
* [skimage](http://scikit-image.org/)


```shell
usage: image2halftoneDXF [-h] [--version] -s SOURCE [-w 200]
                         [--min-radius 0.0] [--max-radius 3.0] [--offset]
                         [-o OUTPUT]

Create a halftone DXF from image (worst name tool ever :)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s SOURCE, --source SOURCE
                        Path to source file
  -w 200, --target-width 200
                        Target width in mm
  --min-radius 0.0      Min radius of holes
  --max-radius 3.0      Max radius of holes
  --offset              Offset odd and even rows
  -o OUTPUT, --output OUTPUT
                        Path to save file
```
