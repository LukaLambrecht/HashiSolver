# imports
import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

    def findsize(self, verbose=False):
        if self.image is None: raise Exception('Current image is None')
        # find connected components using cv2
        img = np.copy(self.image)
        img = np.ascontiguousarray(img, dtype=np.uint8)
        n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)
        if len(stats)==0:
            msg = 'ERROR in HashiImageReader.findsize:'
            msg += ' no centroids could be found in the input image.'
            raise Exception(msg)
        # make image for debugging
        if verbose:
            fig,ax = self.drawimage(doplot=False)
            for i in range(1, n_labels):
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                rectangle = Rectangle((x, y), w, h,
                        fill=False, edgecolor='r', linewidth=2,
                        clip_on=False)
                ax.add_patch(rectangle)
            ax.text(0.02, 1.02, 'Connected components before filtering',
                    ha='left', va='bottom', transform=ax.transAxes,
                    fontsize=13)
            plt.show(block=False)
        # filter clusters based on shape and size
        ws = np.array([stats[i, cv2.CC_STAT_WIDTH] for i in range(len(stats))])
        hs = np.array([stats[i, cv2.CC_STAT_HEIGHT] for i in range(len(stats))])
        mask = np.ones(len(stats)).astype(bool)
        mask = mask & (ws < img.shape[1]*0.9) & (hs < img.shape[0]*0.9)
        aspect_ratio = np.divide(ws, hs)
        mask = mask & (aspect_ratio>0.9) & (aspect_ratio<1.1)
        maxw = np.max(ws[mask])
        maxh = np.max(hs[mask])
        mask = mask & (ws/maxw > 0.9) & (hs/maxh > 0.9)
        centroids = centroids[mask]
        # make image for debugging
        if verbose:
            fig,ax = self.drawimage(doplot=False)
            indices = np.array(list(range(n_labels)))[mask]
            for i in indices:
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                rectangle = Rectangle((x, y), w, h,
                        fill=False, edgecolor='r', linewidth=2,
                        clip_on=False)
                ax.add_patch(rectangle)
            ax.text(0.02, 1.02, 'Connected components after filtering',
                    ha='left', va='bottom', transform=ax.transAxes,
                    fontsize=13)
            plt.show(block=False)
        # check if any connected components remain
        if len(centroids)==0:
            msg = 'ERROR in HashiImageReader.findsize:'
            msg += ' no centroids remain after filtering.'
            raise Exception(msg)
        # determine row height and column width from centroids
        centroids_x = sorted(centroids[:,0])
        centroids_y = sorted(centroids[:,1])
        diff_x = np.diff(centroids_x)
        diff_y = np.diff(centroids_y)
        width_x = np.mean(diff_x[diff_x>5])
        width_y = np.mean(diff_y[diff_y>5])
        # determine number of rows and columns
        self.nrows = int(round(img.shape[0]/width_x))
        self.ncols = int(round(img.shape[1]/width_y))
        # do printout
        if verbose:
            msg = 'INFO in HashiImageReader.findsize:\n'
            msg += '  number of rows:\n'
            msg += '    mean difference between centroids: {}\n'.format(width_x)
            msg += '    total image height: {}\n'.format(img.shape[0])
            msg += '    -> number of rows: {}\n'.format(self.nrows)
            msg += '  number of columns:\n'
            msg += '    mean difference between centroids: {}\n'.format(width_y)
            msg += '    total image width: {}\n'.format(img.shape[1])
            msg += '    -> number of columns: {}'.format(self.ncols)
            print(msg)

    def hashidict(self, verbose=False):
        if self.image is None: raise Exception('Current image is None')
        if self.nrows is None or self.ncols is None: self.findsize(verbose=verbose)
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
                n = digitreco(imgcell, references=dimages, doplot=verbose)
                if n is not None: res[(j, self.ncols-i-1)] = n
        return res


if __name__=='__main__':

    imfile = sys.argv[1]

    HIR = HashiImageReader()
    HIR.loadimage(imfile)
    fig,ax = HIR.drawimage(doplot=False)
    HIR.findsize(verbose=True)
    vertices = HIR.hashidict(verbose=True)
    hashi = Hashi.from_dict(vertices)
    hashi.print()
    print(hashi.to_str())

    plt.show(block=True)
