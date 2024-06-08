import os
import sys

sys.path.append('../src')
from hashi import Hashi


if __name__=='__main__':

    # read input file
    inputfile = sys.argv[1]
    h = Hashi.from_txt(inputfile)
    h.print()
    for v in h.vertices: print('  - {}'.format(v))

    # add edge
    h.add_edge(h.vertices[1], h.vertices[2])
    h.print()
    #for v in h.vertices: print('  - {}'.format(v))

    # add the same edge
    h.add_edge(h.vertices[1], h.vertices[2])
    h.print()

    # add another edge
    h.add_edge(h.vertices[0], h.vertices[3])
    h.print()

    # add the same edge
    h.add_edge(h.vertices[0], h.vertices[3])
    h.print()

    # print vertices
    for v in h.vertices: print('  - {}'.format(v))
