import os
import sys

sys.path.append('../../src')
from hashi import Hashi
sys.path.append('../../solver')
import vertexsolver
import disjointsolver
import hashisolver


if __name__=='__main__':

    # read input file
    #inputfile = sys.argv[1]
    inputfile = '../../fls/example1.txt'
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # do some initial vertex solving to focus on interesting cases
    for v in h.vertices: vertexsolver.fill_vertex(h, v)
    for v in h.vertices: vertexsolver.fill_vertex(h, v)
    hashisolver.close_connections(h)
    h.print()
    
    # test disjoint solving methods
    disjointsolver.close_connections_disjoint(h, verbose=True)