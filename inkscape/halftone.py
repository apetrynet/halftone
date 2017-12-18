import sys
import inkex
import gettext
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert

inkex.localize()
_ = gettext.gettext


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
                                     default=1,
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

        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'halftone')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        #self.getselected()
        if self.selected:
            image = None
            for index in self.selected.keys():
                for k, v in self.selected[index].items():
                    if k.endswith('ref'):
                        image = v
                        break

                if image is None:
                    inkex.errormsg(_("Please select a bitmap image"))
                    return

                org_src = rgb2gray(invert(imread(image)))
                h, w = org_src.shape

                scale = self.options.target_w / float(w)
                img_max = org_src.max()
                tile_w = self.options.max_r * 2

                for ty in xrange(0, h, int(tile_w // scale) + 1):
                    offset = 0
                    if self.options.offset == 'true' and ty % 2:
                        offset = int(tile_w // scale) // 2

                    for tx in xrange(offset, w, int(tile_w // scale) + 1):
                        # Calculate size of dot
                        avg = org_src[ty:ty + int(tile_w),
                                      tx:tx + int(tile_w)
                                      ].mean()

                        dot_r = self.scale_r(avg, img_max)

                        # calculate x, y corrdinates
                        x = ((tx + tile_w) - tile_w // 2) * scale
                        y = ((ty + tile_w) - tile_w // 2) * scale

                        circ_attribs = {
                            'cx': str(x) + self.options.units,
                            'cy': str(y) + self.options.units,
                            'r': str(dot_r) + self.options.units,
                            inkex.addNS('label', 'inkscape'): 'dot',
                            'stroke': 'none',
                            'fill': self.options.fill
                            }

                        inkex.etree.SubElement(layer,
                                               inkex.addNS('circle', 'svg'),
                                               circ_attribs
                                               )

# Create effect instance and apply it.
effect = HalfToneEffect()
effect.affect()
