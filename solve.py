import os
import sys

sys.path.append('./src')
from hashi import Hashi
sys.path.append('./solver')
import hashisolver


if __name__=='__main__':

    # read input file
    inputfile = sys.argv[1]
    h = Hashi.from_txt(inputfile)
    h.print()

    # solve the hashi
    hashisolver.solve(h)
    h.print()
    print('Complete: {}'.format(h.complete))
