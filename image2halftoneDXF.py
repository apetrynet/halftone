#!/usr/bin/python

import sys
import argparse
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert
from dxfwrite import DXFEngine as dxf


__version__ = '1.1.0'


def parse_args():
    unicodize = lambda s: unicode(s, 'utf-8')

    description = 'Create a halftone DXF from image (worst named tool ever :)'
    prog = 'image2halftoneDXF'

    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
                '--version',
                action='version',
                version='%(prog)s' + __version__
                )

    parser.add_argument(
                '-s',
                '--source',
                dest='source',
                action='store',
                type=unicodize,
                default=None,
                help='Path to source file',
                required=True
                )

    parser.add_argument(
                '-w',
                '--target-width',
                dest='target_width',
                action='store',
                type=int,
                default=200,
                help='Target width in mm',
                metavar=200
                )

    parser.add_argument(
                '--min-radius',
                dest='min_radius',
                action='store',
                type=float,
                default=0.,
                help='Min radius of holes',
                metavar=0.
                )

    parser.add_argument(
                '--max-radius',
                dest='max_radius',
                action='store',
                type=float,
                default=3.,
                help='Max radius of holes',
                metavar=3.
                )

    parser.add_argument(
                '--offset',
                dest='offset',
                action='store_true',
                default=True,
                help='Offset odd and even rows'
                )

    parser.add_argument(
                '-o',
                '--output',
                dest='output',
                action='store',
                type=unicodize,
                default=None,
                help='Path to save file'
                )

    # Display help if no arguments are provided
    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    args = parser.parse_args()

    return args


def make_dxf(source=None,
             target_width=200,
             min_radius=0.,
             max_radius=3.,
             offset=True
             ):

    def scale_r(value, min_v, max_v, min_r, max_r):
        return (value - min_v) * (max_r - min_r) / (max_v - min_v) + min_r

    src = rgb2gray(invert(imread(source)))
    dwg = dxf.drawing()
    dwg.add_layer('dots')

    h, w = src.shape
    img_max = src.max()
    img_min = src.min()
    tile_w = max_radius * 2
    scale = target_width / float(w)

    for row, ty in enumerate(xrange(0, h, int(tile_w // scale) + 1)):
        offset_x = 0
        if offset and row % 2:
            offset_x = int(tile_w // scale) // 2

        for tx in xrange(offset_x, w, int(tile_w // scale) + 1):
            # Calculate size of dot
            avg = src[ty:ty + int(tile_w), tx:tx + int(tile_w)].mean()
            dot_r = scale_r(avg, img_min, img_max, min_radius, max_radius)

            # calculate x, y corrdinates
            x = ((tx + tile_w) - tile_w // 2) * scale
            y = ((ty + tile_w) - tile_w // 2) * scale

            c = dxf.circle(radius=dot_r,
                           center=(x, (y * -1) + h * scale),
                           color=1,
                           layer='dots'
                           )
            dwg.add(c)

    return dwg


if __name__ == '__main__':
    opts = parse_args()

    dwg = make_dxf(source=opts.source,
                   target_width=opts.target_width,
                   min_radius=opts.min_radius,
                   max_radius=opts.max_radius,
                   offset=opts.offset
                   )

    output = opts.output
    if output is None:
        output = '.'.join(opts.source.rsplit('.', 1)[:1] + ['dxf'])

    dwg.saveas(output)
