import os
import sys

sys.path.append('../../src')
from edge import Edge
from vertex import Vertex


if __name__=='__main__':

    # make diagonal edge (should give error)
    #edge = Edge(0,0,1,1)
    
    # make example edge
    edge = Edge(0, 0, 5, 0)
    print(edge)
    
    # make other edges and check crossing
    edge2 = Edge(0, 1, 5, 1)
    edge3 = Edge(2, 0, 2, 3)
    edge4 = Edge(2, -1, 2, 3)
    print('Crossings:')
    print(edge.crosses(edge2))
    print(edge.crosses(edge3))
    print(edge.crosses(edge4))
    
    # check if points are contained in the edge
    print('Contains:')
    print(edge.contains(1,1))
    print(edge.contains(0,0))
    print(edge.contains(0,0,endpoints=True))
    print(edge.contains(2,0))
    
    # make vertices and check direction
    v1 = Vertex(0,0,1)
    v2 = Vertex(7,1,1)
    v3 = Vertex(2,1,1)
    print('Directions:')
    print(edge.direction(v1))
    print(edge.hasvertex(v1))
    print(edge.direction(v2))
    print(edge.direction(v3))