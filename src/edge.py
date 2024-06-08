# external imports
import numpy as np

# local imports
from vertex import Vertex


class Edge(object):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if self.x1>self.x2: self.x1,self.x2 = self.x2,self.x1
        if self.y1>self.y2: self.y1,self.y2 = self.y2,self.y1
        self.horizontal = (y2==y1)
        self.vertical = (x2==x1)

    def __str__(self):
        infostr = 'Edge(({},{}) -> ({},{}))'.format(
                    self.x1, self.y1, self.x2, self.y2)
        return infostr

    def crosses(self, other):
        # whether an edge crosses another edge
        if( self.horizontal and other.vertical
            and other.y2>self.y1 and other.y1<self.y1
            and other.x1>self.x1 and other.x1<self.x2 ): return True
        if( self.vertical and other.horizontal
            and other.x2>self.x1 and other.x1<self.x1
            and other.y1>self.y1 and other.y1<self.y2 ): return True
        return False

    def contains(self, x, y):
        # whether an edge contains a point (x,y)
        # note: endpoints not included
        if( self.horizontal and self.y1==y
            and self.x1<x and self.x2>x ): return True
        if( self.vertical and self.x1==x
            and self.y1<y and self.y2>y ): return True
        return False

    def direction(self, v):
        # return direction of an edge with respect to a vertex
        # note: the vertex is situated on the edge or if the relative
        #       positioning is diagonal, None is returned.
        if( self.horizontal and self.x1<v.x and self.x2>v.x ):
            if self.y1>v.y: return 0
            if self.y1<v.y: return 2
        if( self.vertical and self.y1<v.y and self.y2>v.y ):
            if self.x1>v.x: return 1
            if self.x1<v.x: return 3
        return None
