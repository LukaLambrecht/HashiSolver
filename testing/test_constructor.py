import os
import sys

sys.path.append('../src')
from hashi import Hashi


if __name__=='__main__':

    # read file
    inputfile = sys.argv[1]
    h = Hashi.from_txt(inputfile)

    # basic printing
    print(h)
    for v in h.vertices: print(v)

    # fancy printing
    h.print()
