import sys
import numpy as np
from time import time
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.util import invert
from skimage.draw import circle

from dxfwrite import DXFEngine as dxf

#image = sys.argv[1]


def timeit(method):

    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()

        print 'func: %s, %2.2f sec' % (method.__name__, te - ts)
        return result

    return timed


#@timeit
def scale_r(value, max_v):

    return (value / max_v) * float(max_r)


@timeit
def scan_image(src, dest):
    h, w = src.shape
    img_max = src.max()

    dots = []
    for ty in range(0, h, int(tile_w // scale) + 1):
        for tx in range(0, w, int(tile_w // scale) + 1):
            # Calculate size of dot
            avg = src[ty:ty + tile_w, tx:tx + tile_w].mean()
            dot_r = scale_r(avg, img_max)

            # calculate x, y corrdinates
            x = ((tx + tile_w) - tile_w // 2) * scale
            y = ((ty + tile_w) - tile_w // 2) * scale

            # place dot in dest array
            #rr, cc = circle(y, x, dot_r)
            #dest[rr, cc] = (255, 0, 0)

            c = dxf.circle(radius=dot_r,
                           center=(x, (y * -1) + h * scale),
                           color=1,
                           layer='dots'
                           )
            dest.add(c)
            dots.append(dot_r)

    print max(dots)

image = 'images/saxophone.jpg'
image = 'images/rockwool.jpg'
image = 'images/maxresdefault.jpg'
image = 'images/biggie.jpeg'
image = 'images/biggie.png'
image = 'images/audry.jpg'
src = rgb2gray(invert(imread(image)))
h, w = src.shape

max_r = 3
tile_w = max_r * 2


target_w = 575
#target_h = 500

scale = target_w / float(w)
print h * scale
dwg = dxf.drawing('result.dxf')
dwg.add_layer('dots')
scan_image(src, dwg)
dwg.save()

#h, w = src.shape
#dest = np.zeros((h, w, 3), dtype=np.uint8)
#scan_image(src, dest)
#imsave('/local/dot.png', dest)
