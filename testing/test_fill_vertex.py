import os
import sys

sys.path.append('../src')
from hashi import Hashi
import vertexsolver


if __name__=='__main__':

    # read input file
    inputfile = sys.argv[1]
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # fill vertices
    for v in h.vertices: vertexsolver.fill_vertex(h, v)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))
    print('Complete: {}'.format(h.complete))
