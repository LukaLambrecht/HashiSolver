class Edge(object):
	# implementation of single edge object.
	# note: an Edge has no knowledge of any vertices or vertex collection
	#       it might belong to, it is only defined by the coordinates
	#       of its endpoints.
	# note: an Edge is only allowed to be vertical or horizontal,
	#       diagonal edges are not supported by this class.
	# note: the endpoints are by convention ordered from low to high coordinate values
	#       (and there is no ambiguity since edges are always vertical or horizontal).

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
		# determine orientation
        self.horizontal = (y2==y1)
        self.vertical = (x2==x1)
        if not (self.horizontal or self.vertical):
            msg = 'ERROR: only horizontal or vertical edges allowed,'
            msg += ' but found coordinates'
            msg += ' ({},{}) -> ({},{})'.format(self.x1, self.y1, self.x2, self.y2)
            raise Exception(msg)
		# order coordinates from low to high values
        if self.vertical and self.y1>self.y2: 
            self.y1,self.y2 = self.y2,self.y1
        if self.horizontal and self.x1>self.x2:
            self.x1,self.x2 = self.x2,self.x1

    def __str__(self):
        infostr = 'Edge(({},{}) -> ({},{}))'.format(
                    self.x1, self.y1, self.x2, self.y2)
        return infostr
    
    def copy(self):
        return Edge(self.x1, self.y1, self.x2, self.y2)

    def crosses(self, other):
        # whether an edge crosses another edge
        if( self.horizontal and other.vertical
            and other.y2>self.y1 and other.y1<self.y1
            and other.x1>self.x1 and other.x1<self.x2 ): return True
        if( self.vertical and other.horizontal
            and other.x2>self.x1 and other.x1<self.x1
            and other.y1>self.y1 and other.y1<self.y2 ): return True
        return False

    def contains(self, x, y, endpoints=False):
        # whether an edge contains a point (x,y)
        # note: endpoints not included by default, but can be enabled.
        if( self.horizontal and self.y1==y ):
            if( self.x1<x and self.x2>x ): return True
            if( endpoints and (self.x1<=x and self.x2>=x) ): return True
            return False
        if( self.vertical and self.x1==x ):
            if( self.y1<y and self.y2>y ): return True
            if( endpoints and (self.y1<=y and self.y2>=y) ): return True
            return False
        return False
    
    def connects(self, vertices):
        # check whether an edge connects two vertices in a provided list
        nmatch = 0
        for v in vertices:
            if self.hasvertex(v): nmatch += 1
        if( nmatch==0 or nmatch==1 ): return False
        if nmatch==2: return True
        else:
            msg = 'ERROR: found unexpected number of matches,'
            msg += ' check provided list of vertices (potentially duplicates?)'
            raise Exception(msg)
    
    def hasvertex(self, v):
        # check whether the given vertex is one of both endpoints
        if( self.x1==v.x and self.y1==v.y ): return True
        if( self.x2==v.x and self.y2==v.y ): return True
        return False

    def direction(self, v):
        # return direction of an edge with respect to a vertex
        # note: if the vertex is situated on the edge or if the relative
        #       positioning is diagonal, None is returned.
        if( self.horizontal and self.x1<v.x and self.x2>v.x ):
            if self.y1>v.y: return 0
            if self.y1<v.y: return 2
        if( self.vertical and self.y1<v.y and self.y2>v.y ):
            if self.x1>v.x: return 1
            if self.x1<v.x: return 3
        return None