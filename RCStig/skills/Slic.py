from .RCSkill import RCSkill

import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import argparse
import numpy as np

from skimage.data import astronaut
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

from skimage import data
from skimage import color
from skimage import morphology
from skimage import segmentation


from skimage.measure import regionprops

from sklearn.cluster import KMeans
from matplotlib.patches import Circle

class Slic(RCSkill):

    def __init__(self):
        self.img_height = 148
        self.img_width = 1080

    def getSteeringByCords(self, x, y):
        if x < ((self.img_width / 2) - 100):
            return -0.8
        elif x > ((self.img_width / 2) + 100):
            return 0.8
        else:
            return 0

    def go(self, frame):
        frame = img_as_float(frame)

        frame = frame[340:488, 100:1180]

        segments_slic = slic(frame, n_segments=3, compactness=10, sigma=1)
        segments_slic[segments_slic == 0] = 4


        #plt.figure(1)
        #plt.clf()
        #plt.axis('off')
        #plt.title('slic')
        #plt.imshow(frame)


        next_segment_val = segments_slic[146, 590]
        cx = 590
        cy = 590
        regions = regionprops(segments_slic)
        for props in regions:
            cy, cx = props.centroid
            cx = np.int32(cx)
            cy = np.int32(cy)
            if segments_slic[cy, cx] == next_segment_val:
                break

        print("x:", cx, "y:", cy)
        #fig = plt.figure(2)
        #plt.clf()
        #plt.axis('off')
        #plt.title('slic')
        #plt.imshow(segments_slic)
        #circ = Circle((cy,cx),15)
        #ax = fig.add_subplot(1, 1, 1)
        #ax.add_patch(circ)

        #plt.show()

        return {"steering": self.getSteeringByCords(cx, cy)}

