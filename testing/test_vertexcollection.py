import os
import sys

sys.path.append('../src')
from vertex import Vertex
from vertexcollection import VertexCollection


if __name__=='__main__':

    # read file
    inputfile = sys.argv[1]
    vc = VertexCollection.from_txt(inputfile)

    # basic printing
    print(vc)

    # add a connection
    vc.add_connection(0,2)
    print(vc)

    # add the same connection
    vc.add_connection(2,0)
    print(vc)

    # try to add the same connection once more
    #vc.add_connection(0,2)

    # try to add a not-allowed connection
    #vc.add_connection(0,1)
