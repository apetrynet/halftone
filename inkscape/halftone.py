import os
import inkex
import gettext
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert

inkex.localize()
_ = gettext.gettext

__version__ = '1.0.0'


class HalfToneEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-r',
                                     '--max_r',
                                     action='store',
                                     type='float',
                                     dest='max_r',
                                     default=3,
                                     help='Maximum radios of holes'
                                     )

        self.OptionParser.add_option('-f',
                                     '--fill',
                                     action='store',
                                     type='string',
                                     dest='fill',
                                     default='000000ff',
                                     help='Fill color'
                                     )

        self.OptionParser.add_option('-o',
                                     '--offset',
                                     action='store',
                                     dest='offset',
                                     default='true',
                                     help='Offset odd and even holes'
                                     )

        self.OptionParser.add_option('-u',
                                     '--units',
                                     action='store',
                                     type='choice',
                                     choices=['mm', 'in'],
                                     dest='units',
                                     default='mm',
                                     help='Units to determine size of holes and\
width of image'
                                     )

        self.OptionParser.add_option('-w',
                                     '--target_w',
                                     action='store',
                                     type='int',
                                     dest='target_w',
                                     default=500,
                                     help='Target width'
                                     )

    def scale_r(self, value, max_v):
        return (value / max_v) * float(self.options.max_r)

    def effect(self):
        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        self.getselected()
        if self.selected:

            image = None
            for index in self.selected.keys():

                # Get path to image (hacky galore)
                for k, v in self.selected[index].items():
                    if k.endswith('ref'):
                        image = v
                        break

                # Create a new layer.
                layername = '{layer}'.format(layer=os.path.basename(image))
                layer = inkex.etree.SubElement(svg, 'g')
                layer.set(inkex.addNS('label', 'inkscape'), layername)
                layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

                # Convert selected image to an inverted grayscale ndarray
                org_src = rgb2gray(invert(imread(image)))

                # Original image dimensions
                h, w = org_src.shape

                # Calculate scale factor
                scale = self.options.target_w / float(w)

                # get highest "color" value of image to determine range
                img_max = org_src.max()

                # Calculate size of each seacrh
                tile_w = self.options.max_r * 2

                # Iterate over rows
                for row, ty in enumerate(xrange(0, h, int(tile_w // scale) + 1)):

                    # Offset odd rows if offset checkbox is set
                    offset = 0
                    if self.options.offset == 'true' and row % 2:
                        offset = int(tile_w // scale) // 2

                    # Iterate over columns
                    for tx in xrange(offset, w, int(tile_w // scale) + 1):
                        # Get average average value of tile
                        avg = org_src[ty:ty + int(tile_w),
                                      tx:tx + int(tile_w)
                                      ].mean()

                        # Calculate size of dot
                        dot_r = self.scale_r(avg, img_max)

                        # calculate x, y corrdinates
                        x = ((tx + tile_w) - tile_w // 2) * scale
                        y = ((ty + tile_w) - tile_w // 2) * scale

                        # Circle attributes
                        circ_attribs = {
                            'cx': str(x) + self.options.units,
                            'cy': str(y) + self.options.units,
                            'r': str(dot_r) + self.options.units,
                            inkex.addNS('label', 'inkscape'): 'dot',
                            'stroke': 'none',
                            'fill': self.options.fill
                            }

                        # Draw circle
                        inkex.etree.SubElement(layer,
                                               inkex.addNS('circle', 'svg'),
                                               circ_attribs
                                               )

# Create effect instance and apply it.
effect = HalfToneEffect()
effect.affect()
