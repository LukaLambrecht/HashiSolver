import os
import sys

sys.path.append('../../src')
from hashi import Hashi


if __name__=='__main__':

    # read input file
    #inputfile = sys.argv[1]
    inputfile = '../../fls/example1.txt'
    h = Hashi.from_txt(inputfile)
    h.print()
    for vidx, v in enumerate(h.vertices): print('  - {}: {}'.format(vidx, v))

    # add edge
    h.add_edge(0, 1)
    h.print()
    #for v in h.vertices: print('  - {}'.format(v))

    # add the same edge
    #h.add_edge(0, 1)
    h.print()

    # add another edge
    h.add_edge(3, 5)
    h.print()

    # add the same edge
    h.add_edge(3, 5)
    h.print()

    # print vertices
    for v in h.vertices: print('  - {}'.format(v))
