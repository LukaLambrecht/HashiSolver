import os
import sys

sys.path.append('../../src')
from hashi import Hashi
sys.path.append('../../solver')
import vertexsolver


if __name__=='__main__':

    # read input file
    #inputfile = sys.argv[1]
    inputfile = '../../fls/example1.txt'
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # fill vertices
    for v in h.vertices: vertexsolver.fill_vertex(h, v, verbose=True)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))
    print('Complete: {}'.format(h.complete))
    
    # second round
    # (some additional connections can be made)
    for v in h.vertices: vertexsolver.fill_vertex(h, v, verbose=True)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))
    print('Complete: {}'.format(h.complete))
    
    # third round
    # (no further improvement possible with only this solving method)
    for v in h.vertices: vertexsolver.fill_vertex(h, v, verbose=True)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))
    print('Complete: {}'.format(h.complete))