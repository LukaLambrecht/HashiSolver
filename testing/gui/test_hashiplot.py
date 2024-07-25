import os
import sys
from bokeh.io import show

sys.path.append('../../src')
from hashi import Hashi
sys.path.append('../../solver')
import hashisolver
sys.path.append('../../gui')
from hashiplot import makehashiplot


if __name__=='__main__':

    # read input file
    inputfile = sys.argv[1]
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # plot the hashi
    fig = makehashiplot(h)
    show(fig)

    # solve the hashi
    hashisolver.solve(h)

    # and plot again
    fig = makehashiplot(h)
    show(fig)
