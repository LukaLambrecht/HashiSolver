# imports
import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.append(os.path.abspath('../src'))
from hashi import Hashi

from digitreco import digitreco


class HashiImageReader(object):
    ### class for reading a Hashi puzzle from an image
    # for now, only works on 'nice' images, i.e.:
    # - good and uniform lighting
    # - perfect portrait orientation and straight lines
    # - equal thickness of all lines
    # - digital written numbers
    # (main use case: screenshots from online puzzles)

    def __init__(self):
        self.image = None
        self.nrows = None
        self.ncols = None
    
    def loadimage(self, imagefile, targetsize=None):
        ### load an image and perform preprocessing.
        # preprocessing includes:
        # - convert to 2D grayscale array
        # - project values to 0 or 1
        #   (note: high values = white will be projected to 0,
        #    low values = black will be projected to 1!)
        # - type conversion to numpy uint8
        # - crop potential edges and extra space in between
        # - resizing (optional)
        self.image = cv2.imread(imagefile)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = np.where(self.image>128,0,1)
        self.image = self.image.astype(np.uint8)
        # remove whitespace
        self.image = self.image[~np.all(self.image==0, axis=1),:]
        self.image = self.image[:,~np.all(self.image==0, axis=0)]
        print('Loaded image {}'.format(imagefile))
        if targetsize is not None:
            self.image = cv2.resize(self.image, targetsize)
            self.image = np.where(self.image>128,0,1)
            print('Converted image to size {}'.format(targetsize))

    def drawimage(self, doplot=True, invert=True, title=None, ticks=False):
        ### draw the currently loaded image for visual inspection
        if self.image is None: raise Exception('Current image is None')
        image = np.copy(self.image)
        if invert: image = np.where(image>0.5,0,1)
        (fig,ax) = plt.subplots()
        ax.imshow(image, cmap='gray')
        if title is not None: ax.set_title(title)
        if not ticks:
            ax.set_xticks([])
            ax.set_yticks([])
        if doplot: plt.show(block=False)
        return (fig,ax)

    def findsize(self):
        # to do...
        pass

    def hashidict(self):
        if self.image is None: raise Exception('Current image is None')
        if self.nrows is None or self.ncols is None:
            #self.findsize()
            msg = 'ERROR in HashiImageReader.hashidict:'
            msg += ' for now, the expected size of the hashi must be set'
            msg += ' manually in the nrows and ncols attributes'
            msg += ' (automatic derivation of the size not yet implemented).'
            raise Exception(msg)
        # initialize output
        res = {}
        # read digit images
        dimages = {}
        for digit in [1,2,3,4,5,6,7,8]:
            abspath = os.path.abspath(os.path.dirname(__file__))
            dimage = '../res/number_{}.png'.format(digit)
            dimage = os.path.join(abspath,dimage)
            darray = cv2.imread(dimage)
            darray = cv2.cvtColor(darray, cv2.COLOR_BGR2GRAY)
            darray = np.where(darray>128,0,1)
            darray = darray.astype(np.uint8)
            dimages[digit] = darray
        # loop over individual cells
        # (i.e. potential vertex positions)
        cellheight = self.image.shape[0]/self.nrows
        cellwidth = self.image.shape[1]/self.ncols
        for i in range(self.nrows):
            for j in range(self.ncols):
                imgcell = self.image[int(i*cellheight):int((i+1)*cellheight),
                            int(j*cellwidth):int((j+1)*cellwidth)]
                # remove whitespace
                imgcell = imgcell[~np.all(imgcell==0, axis=1),:]
                imgcell = imgcell[:,~np.all(imgcell==0, axis=0)]
                if tuple(imgcell.shape)==(0,0): continue
                # check fraction of filled pixels
                fillfrac = np.sum(imgcell)/(imgcell.shape[0]*imgcell.shape[1])
                if np.sum(imgcell)==0 or fillfrac < 0.1: continue
                # apply a mask to suppress the circle edges
                Y, X = np.ogrid[:imgcell.shape[0], :imgcell.shape[1]]
                center = (imgcell.shape[0]/2, imgcell.shape[1]/2)
                dist = np.sqrt((X-center[0])**2 + (Y-center[1])**2)
                mask = dist <= center[0]*0.8
                imgcell = np.where(mask, imgcell, 0)
                # read digit
                n = digitreco(imgcell, references=dimages, doplot=False)
                if n is not None: res[(j, self.ncols-i-1)] = n
        return res


if __name__=='__main__':

    imfile = sys.argv[1]
    hsize = tuple([int(el) for el in sys.argv[2].split(',')])

    HIR = HashiImageReader()
    HIR.loadimage(imfile)
    #fig,ax = HIR.drawimage(doplot=False)

    HIR.nrows = hsize[0]
    HIR.ncols = hsize[1]
    vertices = HIR.hashidict()
    hashi = Hashi.from_dict(vertices)
    hashi.print()
    print(hashi.to_str())

    plt.show()
