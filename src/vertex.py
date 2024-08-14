import numpy as np

class Vertex(object):
    # implementation of single vertex object.
    # note: a Vertex has no knowledge of any topology or collection it might belong to,
    #       it is only defined by its coordinates and local connections.

    def __init__(self, x, y, n, multiplicity=2, connections=None):
        # copy attributes
        self.x = x
        self.y = y
        self.n = n
        self.multiplicity = multiplicity
        # set vertex completion to false
        self.complete = False
        # initialize list of connections
        # note: convention is [u1,u2,r1,r2,d1,d2,l1,12]
        # note: 0 = no connection, but connection allowed
        #       1 = established connection
        #       -1 = no connection allowed
        if connections is not None:
            # special case: connections are provided as argument
            # (e.g. when copying an already partially solved vertex)
            self.connections = connections.astype(int)
            # check completion
            if np.sum(self.connections==1)==self.n:
                self.complete = True
                # close all remaining connections for this vertex
                self.connections = np.where(self.connections==0, -1, self.connections)
        else:
            # default case: all connections are initialized to 0 (allowed connection)
            self.connections = np.zeros(4*multiplicity).astype(int)

    def __str__(self):
        infostr = 'Vertex (x: {}, y: {}, n: {}'.format(self.x, self.y, self.n)
        infostr += ', complete: {}, connections: {})'.format(self.complete, self.connections)
        return infostr
    
    def copy(self):
        return Vertex(self.x, self.y, self.n, multiplicity=self.multiplicity, connections=np.copy(self.connections))

    def get_connections(self, direction):
        return self.connections[self.multiplicity*direction : self.multiplicity*(direction+1)]

    def n_established_connections(self, direction):
        # count number of established connections in a given direction
        connections = self.get_connections(direction)
        return np.sum(connections==1)

    def has_established_connection(self, direction):
        # check if at least one connection in a given direction is established
        return (self.n_established_connections(direction)>0)

    def n_potential_connections(self, direction):
        # cound number of potential connections in a given direction
        connections = self.get_connections(direction)
        return np.sum(connections==0)

    def has_potential_connection(self, direction):
        # check if at least one connection in a given direction is possible
        return (self.n_potential_connections(direction)>0)

    def n_closed_connections(self, direction):
        # cound number of closed connections in a given direction
        connections = self.get_connections(direction)
        return np.sum(connections==-1)

    def has_closed_connection(self, direction):
        # check if at least one connection in a given direction is closed
        return (self.n_closed_connections(direction)>0)
    
    def n_missing_connections(self):
        # check how many connections are still missing for this vertex
        return self.n - np.sum(self.connections==1)

    def directions_with_established_connection(self):
        return [d for d in [0,1,2,3] if self.has_established_connection(d)]

    def directions_with_potential_connection(self):
        return [d for d in [0,1,2,3] if self.has_potential_connection(d)]

    def directions_with_closed_connection(self):
        return [d for d in [0,1,2,3] if self.has_closed_connection(d)]

    def add_connection(self, direction):
        # add a connections in a given direction
        n = 0
        while n < self.multiplicity:
            if self.connections[self.multiplicity*direction+n]==0:
                self.connections[self.multiplicity*direction+n] = 1
                break
            else: n += 1
        if n==self.multiplicity: raise Exception('ERROR: connection not allowed.')
        # check if this makes the vertex complete
        if np.sum(self.connections==1)==self.n:
            self.complete = True
            # close all remaining connections for this vertex
            self.connections = np.where(self.connections==0, -1, self.connections)

    def close_connection(self, direction, n, suppress_warnings=False):
        # close a potential connection in a given direction
        # note: usually only used as auxiliary function to close_connections
        if self.connections[self.multiplicity*direction+n]==1:
            raise Exception('ERROR: trying to close an already established connection.')
        elif self.connections[self.multiplicity*direction+n]==-1 and not suppress_warnings:
            print('WARNING: trying to close an already closed connection.')
        # close the connection
        self.connections[self.multiplicity*direction+n] = -1
        # check if this makes the vertex complete
        if np.sum(self.connections==1)==self.n: self.complete = True

    def close_connections(self, direction, suppress_warnings=False):
        # close all potential connections in a given direction
        for n in range(self.multiplicity): self.close_connection(direction, n, suppress_warnings=suppress_warnings)

    def close_n_connections(self, direction, n, suppress_warnings=False):
        # close a given number of connections in a given direction
        n_closed = 0
        for idx in range(self.multiplicity):
            if self.connections[self.multiplicity*direction+idx]==0:
                self.close_connection(direction, idx, suppress_warnings=suppress_warnings)
                n_closed += 1
                if n_closed == n: break
        if n_closed < n and not suppress_warnings:
            print('WARNING: could not find enough connections to close.')

    def direction(self, other):
        # get direction of self w.r.t. other
        # self above other
        if( self.x==other.x and self.y>other.y ): return 0
        # self right from other
        if( self.x>other.x and self.y==other.y ): return 1
        # self below other
        if( self.x==other.x and self.y<other.y ): return 2
        # self left from other
        if( self.x<other.x and self.y==other.y ): return 3
        # none of the above
        return -1

    def is_in_direction(self, other, direction):
        # check if self is in a given direction w.r.t. other
        if direction==self.direction(other): return True
        return False

    def find_closest(self, others, direction):
        # find closest vertex among provided others in a given direction
        # note: returns None if no vertices in the given direction were found
        candidates = [v for v in others if v.is_in_direction(self, direction)]
        if len(candidates)==0: return None
        distances = [np.sqrt((v.x-self.x)**2 + (v.y-self.y)**2) for v in candidates]
        idx = np.argmin(distances)
        return candidates[idx]
