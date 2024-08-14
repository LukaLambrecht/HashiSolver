import numpy as np
import cv2
import matplotlib.pyplot as plt


def digitreco(digit_image, references=None, doplot=False):
    # recognize a single digit

    # read reference images from disk if they are not provided,
    # or if they are provided, make a hard copy
    # (needed because they will be modified, e.g. cropped and resized).
    if references is None:
        # read digit images
        references = {}
        for digit in [1,2,3,4,5,6,7,8]:
            abspath = os.path.abspath(os.path.dirname(__file__))
            dimage = '../res/number_{}.png'.format(digit)
            dimage = os.path.join(abspath,dimage)
            darray = cv2.imread(dimage)
            darray = cv2.cvtColor(darray, cv2.COLOR_BGR2GRAY)
            darray = np.where(darray>128,0,1)
            darray = darray.astype(np.uint8)
            references[digit] = darray
    else:
        newreferences = {digit: np.copy(im) for digit,im in references.items()}
        references = newreferences

    # remove whitespace from both provided and reference images
    digit_image = digit_image[~np.all(digit_image==0, axis=1),:]
    digit_image = digit_image[:,~np.all(digit_image==0, axis=0)]
    if tuple(digit_image.shape)==(0,0):
        msg = 'WARNING in digitreco: empty image provided, returning None.'
        return None
    for digit, dimage in references.items():
        dimage = dimage[~np.all(dimage==0, axis=1),:]
        dimage = dimage[:,~np.all(dimage==0, axis=0)]
        references[digit] = dimage

    # resize references and calculate filled pixels
    filled = {}
    for digit, dimage in references.items():
        references[digit] = cv2.resize(dimage, (digit_image.shape[1], digit_image.shape[0]))
        filled[digit] = np.sum(references[digit])

    # calculate overlap
    overlaps = {}
    maxoverlap = 0
    res = None
    digit_filled = np.sum(digit_image)
    for digit, dimage in references.items():
        overlap = np.sum(np.multiply(digit_image, dimage))/(filled[digit]*digit_filled)
        overlaps[digit] = overlap
        if overlap > maxoverlap:
            maxoverlap = overlap
            res = digit

    # make a plot
    if doplot:
        fig,axs = plt.subplots(nrows=len(references), ncols=3, squeeze=False)
        for i,(digit, dimage) in enumerate(references.items()):
            axs[i,0].imshow(digit_image)
            axs[i,1].imshow(dimage)
            axs[i,2].imshow(np.multiply(digit_image,dimage))
        plt.show()

    # return best-fit digit
    return res
