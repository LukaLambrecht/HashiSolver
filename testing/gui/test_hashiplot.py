import os
import sys
#from bokeh.io import show
import matplotlib as mpl
import matplotlib.pyplot as plt

sys.path.append('../../src')
from hashi import Hashi
sys.path.append('../../solver')
import hashisolver
#sys.path.append('../../gui-bokeh') # bokeh version
#from hashiplot import makehashiplot # bokeh version
sys.path.append('../../gui-pyqt5') # matplotlib version
from hashiplot import makehashiplot # matplotlib version


if __name__=='__main__':

    # read input file
    #inputfile = sys.argv[1]
    inputfile = '../../fls/example1.txt'
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # plot the hashi
    fig,ax = makehashiplot(h)
    fig.show()

    # solve the hashi
    hashisolver.solve(h)

    # and plot again
    fig,ax = makehashiplot(h)
    fig.show()
